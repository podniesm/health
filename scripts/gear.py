"""Przebieg butów i innego sprzętu na podstawie kolumny gear w activities.csv.

Użycie:  python scripts/gear.py
Liczy tylko treningi zapisane w CSV (bez kilometrów startowych wpisanych w Garminie).
"""
from __future__ import annotations

import csv
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ACTIVITIES = ROOT / "data" / "training" / "activities.csv"


def main() -> int:
    since_30 = (date.today() - timedelta(days=30)).isoformat()
    stats: dict[str, dict] = {}
    with ACTIVITIES.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            for g in filter(None, (x.strip() for x in r.get("gear", "").split(";"))):
                s = stats.setdefault(g, {"n": 0, "km": 0.0, "km30": 0.0, "first": r["date"], "last": r["date"]})
                km = float(r["distance_km"] or 0)
                s["n"] += 1
                s["km"] += km
                if r["date"] >= since_30:
                    s["km30"] += km
                s["first"], s["last"] = min(s["first"], r["date"]), max(s["last"], r["date"])
    if not stats:
        print("Brak treningów z przypisanym sprzętem.")
        return 0
    width = max(len(g) for g in stats)
    print(f"{'sprzęt':<{width}}  {'tren.':>5}  {'km':>7}  {'km 30d':>6}  od          do")
    for g, s in sorted(stats.items(), key=lambda kv: kv[1]["last"], reverse=True):
        print(f"{g:<{width}}  {s['n']:>5}  {s['km']:>7.1f}  {s['km30']:>6.1f}  {s['first']}  {s['last']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
