"""Pobiera świeże dane z Garmin Connect i zapisuje je do data/.

Co pobiera:
  - treningi (z butami/rowerem z Garmina)    → data/training/activities.csv
  - sen (fazy, score, drzemki)              → data/body/sleep.csv
  - tętno spoczynkowe, HRV, średni stres,
    VO2max, kalorie dzienne (łączne i
    aktywne; bez dzisiejszego, niepełnego
    dnia), waga, % tkanki tłuszczowej,
    masa mięśni                             → data/body/measurements.csv (jeden wiersz Garmina
                                              na dzień; time = godzina ważenia, jeśli było)

Po synchronizacji wypisuje tabelę kalibracji RPE dla treningów z pobranego
zakresu: RPE obok % HRmax (śr. tętno / najwyższe tętno z 12 mies.) i TE.

Użycie:
  python scripts/garmin_sync.py                    # od ostatnich danych w CSV
  python scripts/garmin_sync.py --since 2026-09-01 # od podanej daty
  python scripts/garmin_sync.py --dry-run          # pokaż zmiany bez zapisu

Ostatnie dni pobiera ponownie: Garmin uzupełnia je z opóźnieniem (np. stres
z niepełnego dnia). Wiersze z source=garmin są wtedy aktualizowane, a wiersze
wpisane ręcznie zostają bez zmian. Buty przypisane w Garminie później (lub
zmienione) trafiają do istniejących wierszy treningów z tego zakresu.

Logowanie: przy pierwszym uruchomieniu e-mail i hasło (albo zmienne
GARMIN_EMAIL / GARMIN_PASSWORD), ewentualnie kod MFA. Tokeny trafiają do
~/.garminconnect (poza folderem health/), więc kolejne uruchomienia nie
pytają o hasło. Wymaga: pip install garminconnect
"""
from __future__ import annotations

import argparse
import csv
import getpass
import os
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
DATA = ROOT / "data"
ACTIVITIES = DATA / "training" / "activities.csv"
SLEEP = DATA / "body" / "sleep.csv"
MEASUREMENTS = DATA / "body" / "measurements.csv"

TOKENSTORE = os.getenv("GARMINTOKENS", str(Path.home() / ".garminconnect"))
SOURCE = "garmin"
OVERLAP_DAYS = 2  # ile ostatnich dni pobrać ponownie
DAILY_FIELDS = ["resting_hr", "hrv_ms", "stress_avg", "vo2max", "kcal_total", "kcal_active"]
SLEEP_FIELDS = ["bedtime", "wake_time", "duration_h", "deep_h", "rem_h", "light_h", "awake_h", "score", "notes"]
SKIP_TYPES = {"breathwork", "meditation"}  # nie są treningiem
SKIP_WEIGHT_SOURCES = {"USER_SETTING", "CHANGE_LOG"}  # waga z ustawień profilu, nie ważenie


# ---------- formatowanie ----------

def fmt(x, nd: int = 0) -> str:
    """Liczba → tekst bez zbędnych zer (82.0 → '82', 7.633 → '7.63'). None → ''."""
    if x is None or x == "":
        return ""
    s = f"{round(float(x), nd):.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def local_ms(ms) -> datetime | None:
    """Znacznik Garmina '...Local' (ms, czas lokalny zapisany jak UTC) → datetime."""
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(tzinfo=None)


def gear_name(g: dict) -> str:
    """Sprzęt Garmina → nazwa jak w aplikacji, np. 'EVO SL Black 1'.

    displayName, bo customMakeModel bywa różny w API i w eksporcie ZIP ('adidas' vs 'adidas Adizero EVO SL').
    """
    return (g.get("displayName") or g.get("customMakeModel") or "").strip()


def map_type(type_key: str) -> str | None:
    k = type_key.lower()
    if k in SKIP_TYPES:
        return None
    if "run" in k:
        return "bieg"
    if "cycl" in k or "biking" in k or "ride" in k:
        return "rower"
    if "swim" in k:
        return "pływanie"
    if "strength" in k:
        return "siłownia"
    if "walk" in k:
        return "spacer"
    if "hik" in k or "mountaineering" in k:
        return "wędrówka"
    if "ski" in k or "snowboard" in k:
        return "narty"
    return "inne"


# ---------- CSV ----------

def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, header: list[str], rows: list[dict]) -> None:
    rows.sort(key=lambda r: (r["date"], r.get("time", "")))  # stabilnie: kolejność w dniu zostaje
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def last_garmin_date(rows: list[dict]) -> date | None:
    dates = [r["date"] for r in rows if r.get("source") == SOURCE]
    return date.fromisoformat(max(dates)) if dates else None


def merge_fields(row: dict, new: dict, fields: list[str]) -> bool:
    """Nadpisuje pola wartościami z Garmina; puste nowe wartości nie kasują starych."""
    changed = False
    for k in fields:
        if new.get(k) and row.get(k) != new[k]:
            row[k] = new[k]
            changed = True
    return changed


# ---------- logowanie ----------

def login():
    try:
        from garminconnect import Garmin, GarminConnectAuthenticationError
    except ImportError:
        sys.exit("Brak biblioteki: pip install garminconnect")

    try:
        api = Garmin()
        api.login(TOKENSTORE)
        return api
    except GarminConnectAuthenticationError:
        pass  # brak lub wygasłe tokeny – logowanie hasłem

    if not sys.stdin.isatty() and not (os.getenv("GARMIN_EMAIL") and os.getenv("GARMIN_PASSWORD")):
        sys.exit("Brak zapisanych tokenów. Uruchom skrypt raz w zwykłym terminalu, żeby się zalogować.")
    email = os.getenv("GARMIN_EMAIL") or input("Garmin e-mail: ")
    password = os.getenv("GARMIN_PASSWORD") or getpass.getpass("Garmin hasło: ")
    api = Garmin(email, password, prompt_mfa=lambda: input("Kod MFA: "))
    api.login(TOKENSTORE)
    print(f"Zalogowano, tokeny zapisane w {TOKENSTORE}")
    return api


# ---------- pobieranie ----------

def fetch_activities(api, start: str, end: str) -> list[dict]:
    rows = []
    acts = api.get_activities_by_date(start, end, sortorder="asc") or []
    for a in acts:
        type_key = (a.get("activityType") or {}).get("typeKey", "")
        typ = map_type(type_key)
        if typ is None or not a.get("startTimeLocal") or not a.get("duration"):
            continue
        notes = [type_key] if typ == "inne" else []
        if a.get("aerobicTrainingEffect"):
            notes.append(f"TE {fmt(a['aerobicTrainingEffect'], 1)}")
        distance = a.get("distance") or 0
        # RPE (10–100) nie ma na liście aktywności – jest tylko w szczegółach treningu
        rpe = a.get("workoutRpe") or a.get("directWorkoutRpe")
        if not rpe and a.get("activityId"):
            rpe = ((api.get_activity(a["activityId"]) or {}).get("summaryDTO") or {}).get("directWorkoutRpe")
        gear = api.get_activity_gear(a["activityId"]) if a.get("activityId") else []
        rows.append({
            "date": a["startTimeLocal"][:10],
            "type": typ,
            "duration_min": fmt(a["duration"] / 60, 1),
            "distance_km": fmt(distance / 1000, 2) if distance else "",
            "avg_hr": fmt(a.get("averageHR")),
            "max_hr": fmt(a.get("maxHR")),
            "elevation_m": fmt(a.get("elevationGain")),
            "calories": fmt(a.get("calories")),
            "training_load": fmt(a.get("activityTrainingLoad"), 1),
            "rpe": fmt(rpe / 10) if rpe else "",
            "gear": "; ".join(sorted({gear_name(g) for g in gear or []} - {""})),
            "notes": "; ".join(notes),
            "source": SOURCE,
        })
    return rows


def fetch_sleep(api, d: str) -> dict | None:
    dto = (api.get_sleep_data(d) or {}).get("dailySleepDTO") or {}
    if not dto.get("sleepTimeSeconds"):
        return None
    hours = lambda key: fmt((dto.get(key) or 0) / 3600, 2)
    start, end = local_ms(dto.get("sleepStartTimestampLocal")), local_ms(dto.get("sleepEndTimestampLocal"))
    nap_min = round((dto.get("napTimeSeconds") or 0) / 60)
    score = ((dto.get("sleepScores") or {}).get("overall") or {}).get("value")
    return {
        "date": d,
        "bedtime": start.strftime("%H:%M") if start else "",
        "wake_time": end.strftime("%H:%M") if end else "",
        "duration_h": hours("sleepTimeSeconds"),
        "deep_h": hours("deepSleepSeconds"),
        "rem_h": hours("remSleepSeconds"),
        "light_h": hours("lightSleepSeconds"),
        "awake_h": hours("awakeSleepSeconds"),
        "score": fmt(score),
        "notes": f"drzemka {nap_min} min" if nap_min else "",
        "source": SOURCE,
    }


def fetch_daily(api, d: str) -> dict:
    summary = api.get_user_summary(d) or {}
    hrv = (api.get_hrv_data(d) or {}).get("hrvSummary") or {}
    stress = summary.get("averageStressLevel")
    return {
        "resting_hr": fmt(summary.get("restingHeartRate")),
        "hrv_ms": fmt(hrv.get("lastNightAvg")),
        "stress_avg": fmt(stress) if stress is not None and stress >= 0 else "",  # <0 = za mało danych
    }


def fetch_vo2max(api, start: str, end: str) -> dict[str, str]:
    out = {}
    for item in api.get_max_metrics_range(start, end) or []:
        generic = item.get("generic") or {}
        if generic.get("calendarDate") and generic.get("vo2MaxValue"):
            out[generic["calendarDate"]] = fmt(generic["vo2MaxValue"])
    return out


def fetch_weights(api, start: str, end: str) -> list[dict]:
    rows = []
    for w in (api.get_body_composition(start, end) or {}).get("dateWeightList") or []:
        ts = local_ms(w.get("date"))
        if not ts or not w.get("weight") or w.get("sourceType") in SKIP_WEIGHT_SOURCES:
            continue
        rows.append({
            "date": ts.strftime("%Y-%m-%d"),
            "time": ts.strftime("%H:%M"),
            "weight_kg": fmt(w["weight"] / 1000, 1),
            "body_fat_pct": fmt(w["bodyFat"], 1) if w.get("bodyFat") else "",  # 0 = brak pomiaru
            "muscle_kg": fmt(w["muscleMass"] / 1000, 1) if w.get("muscleMass") else "",
            "source": SOURCE,
        })
    return rows


def fetch_calories(api, start: str, end: str) -> dict[str, dict]:
    """Kalorie dzienne (aktywne + spoczynkowe/BMR) dla zakresu – jedno zapytanie."""
    return {
        c["calendarDate"]: {"kcal_total": fmt(c["total"]), "kcal_active": fmt(c["active"])}
        for c in api.get_calories_daily(start, end) or []
        if c.get("total")
    }


# ---------- scalanie ----------

def merge_activities(rows: list[dict], new: list[dict]) -> tuple[int, int, int]:
    added = rpe_filled = gear_set = 0
    for n in new:
        dup = next((
            r for r in rows
            if r["date"] == n["date"] and r["type"] == n["type"]
            and abs(float(r["duration_min"] or 0) - float(n["duration_min"])) <= 1
        ), None)
        if dup is None:
            rows.append(n)
            added += 1
        elif dup.get("source") == SOURCE and n["rpe"] and dup.get("rpe") != n["rpe"]:
            dup["rpe"] = n["rpe"]  # RPE wpisane lub poprawione w Garminie po poprzedniej synchronizacji
            rpe_filled += 1
        if dup is not None and dup.get("source") == SOURCE and n["gear"] and dup.get("gear") != n["gear"]:
            dup["gear"] = n["gear"]  # buty dopisane lub zmienione w Garminie po synchronizacji
            gear_set += 1
    return added, rpe_filled, gear_set


def merge_sleep(rows: list[dict], new: list[dict]) -> tuple[int, int]:
    by_date = {r["date"]: r for r in rows}
    added = updated = 0
    for n in new:
        r = by_date.get(n["date"])
        if r is None:
            rows.append(n)
            by_date[n["date"]] = n
            added += 1
        elif r.get("source") == SOURCE and merge_fields(r, n, SLEEP_FIELDS):
            updated += 1
    return added, updated


def merge_daily(rows: list[dict], header: list[str], new: dict[str, dict]) -> tuple[int, int]:
    """Parametry dzienne trafiają do pierwszego wiersza Garmina z danej daty (także tego z ważeniem)."""
    daily: dict[str, dict] = {}
    for r in rows:
        if r.get("source") == SOURCE:
            daily.setdefault(r["date"], r)
    added = updated = 0
    for d, values in sorted(new.items()):
        if not any(values.values()):
            continue
        r = daily.get(d)
        if r is None:
            r = {k: "" for k in header} | {"date": d, "source": SOURCE}
            merge_fields(r, values, DAILY_FIELDS)
            rows.append(r)
            daily[d] = r
            added += 1
        elif merge_fields(r, values, DAILY_FIELDS):
            updated += 1
    return added, updated


def merge_weights(rows: list[dict], header: list[str], new: list[dict]) -> int:
    added = 0
    for n in new:
        dup = any(
            r["date"] == n["date"] and r["weight_kg"]
            and (r["time"] == n["time"] or abs(float(r["weight_kg"]) - float(n["weight_kg"])) < 0.05)
            for r in rows
        )
        if dup:
            continue
        # pierwsze ważenie dnia → do wiersza dziennego Garmina; kolejne → osobny wiersz
        day_row = next((r for r in rows if r["date"] == n["date"] and r.get("source") == SOURCE and not r["weight_kg"]), None)
        if day_row is not None:
            day_row.update({k: v for k, v in n.items() if v})
        else:
            rows.append({k: "" for k in header} | n)
        added += 1
    return added


# ---------- kalibracja RPE ----------

HR_TYPES = {"bieg", "rower", "pływanie"}  # przy siłowni tętno nie oddaje wysiłku
RPE_BANDS = [(60, "1"), (70, "2"), (80, "3–4"), (87, "5–6"), (92, "7–8"), (999, "9–10")]  # % HRmax (śr. HR) → RPE


def hr_max(rows: list[dict], today: date) -> tuple[int, str] | None:
    """Najwyższe tętno z treningów cardio z ostatnich 12 miesięcy (a jeśli brak – z całej historii).

    Siłownia pominięta: optyczny czujnik daje tam fałszywe skoki (np. 209 przy śr. 106).
    """
    with_hr = [r for r in rows if r.get("max_hr") and r["type"] in HR_TYPES]
    recent = [r for r in with_hr if r["date"] >= (today - timedelta(days=365)).isoformat()]
    best = max(recent or with_hr, key=lambda r: float(r["max_hr"]), default=None)
    return (round(float(best["max_hr"])), best["date"]) if best else None


def print_rpe_calibration(rows: list[dict], start: str, end: str, today: date, limit: int = 10) -> None:
    acts = [r for r in rows if start <= r["date"] <= end and r.get("avg_hr")][-limit:]
    hm = hr_max(rows, today)
    if not acts or not hm:
        return
    print(f"\nKalibracja RPE (HRmax {hm[0]} = najwyższe tętno z treningów cardio, {hm[1]}):")
    print(f"  {'data':<10}  {'typ':<9} {'czas':>7} {'śr.HR':>5} {'%HRmax':>6} {'TE':>4} {'obciąż.':>7} {'RPE':>4}  orient. RPE wg tętna")
    for r in acts:
        pct = float(r["avg_hr"]) / hm[0] * 100
        te = next((p[3:] for p in r.get("notes", "").split("; ") if p.startswith("TE ")), "")
        hint = next(rpe for limit_pct, rpe in RPE_BANDS if pct < limit_pct) if r["type"] in HR_TYPES else "–"
        print(f"  {r['date']:<10}  {r['type']:<9} {fmt(r['duration_min']):>3} min {r['avg_hr']:>5} {pct:>5.0f}% "
              f"{te:>4} {r.get('training_load', ''):>7} {r.get('rpe') or 'brak':>4}  {hint}")
    print("  Orientacyjne RPE dotyczy biegów spokojnych i ciągłych. Długi trening (>75 min) lub interwały → zwykle +1–2.")


# ---------- main ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronizacja danych z Garmin Connect")
    parser.add_argument("--since", type=date.fromisoformat, help="data początkowa YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="nie zapisuj, tylko pokaż podsumowanie")
    args = parser.parse_args()

    act_header, act_rows = read_csv(ACTIVITIES)
    sleep_header, sleep_rows = read_csv(SLEEP)
    meas_header, meas_rows = read_csv(MEASUREMENTS)

    today = date.today()
    if args.since:
        start = args.since
    else:
        last = [d for d in (last_garmin_date(act_rows), last_garmin_date(sleep_rows), last_garmin_date(meas_rows)) if d]
        start = (min(last) if last else today - timedelta(days=30)) - timedelta(days=OVERLAP_DAYS)
    days = [(start + timedelta(days=i)).isoformat() for i in range((today - start).days + 1)]
    s, e = days[0], days[-1]
    print(f"Zakres: {s} → {e} ({len(days)} dni)")

    api = login()

    new_acts = fetch_activities(api, s, e)
    vo2 = fetch_vo2max(api, s, e)
    weights = fetch_weights(api, s, e)
    yesterday = (today - timedelta(days=1)).isoformat()
    kcal = fetch_calories(api, s, yesterday) if s <= yesterday else {}  # dzisiejszy dzień jest niepełny
    new_sleep, daily = [], {}
    for d in days:
        print(f"  {d}", end="\r")
        if (row := fetch_sleep(api, d)):
            new_sleep.append(row)
        daily[d] = fetch_daily(api, d) | {"vo2max": vo2.get(d, "")} | kcal.get(d, {})
    print()

    a_added, a_rpe, a_gear = merge_activities(act_rows, new_acts)
    s_added, s_updated = merge_sleep(sleep_rows, new_sleep)
    d_added, d_updated = merge_daily(meas_rows, meas_header, daily)
    w_added = merge_weights(meas_rows, meas_header, weights)

    print(f"Treningi:           +{a_added} (pobrano {len(new_acts)}, reszta to duplikaty; uzupełnione RPE: {a_rpe}, buty: {a_gear})")
    print(f"Sen:                +{s_added}, zaktualizowano {s_updated}")
    print(f"Dzienne parametry:  +{d_added}, zaktualizowano {d_updated} (tętno spocz., HRV, stres, kcal: {len(kcal)} dni, VO2max: {len(vo2)} dni)")
    print(f"Ważenia:            +{w_added} (pobrano {len(weights)})")
    print_rpe_calibration(act_rows, s, e, today)

    if args.dry_run:
        print("--dry-run: nic nie zapisano.")
        return 0
    write_csv(ACTIVITIES, act_header, act_rows)
    write_csv(SLEEP, sleep_header, sleep_rows)
    write_csv(MEASUREMENTS, meas_header, meas_rows)
    return subprocess.call([sys.executable, str(ROOT / "scripts" / "validate.py")])


if __name__ == "__main__":
    sys.exit(main())
