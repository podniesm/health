---
name: import
description: Przetwarza wszystkie pliki z inbox/ (PDF i zdjęcia badań, eksporty CSV z Garmin/Strava/Polar, eksporty wagi i snu, dokumenty lekarskie) do ustrukturyzowanych plików w data/ i archiwizuje źródła. Używaj, gdy użytkownik wrzucił nowe pliki lub pisze "zaimportuj", "przetwórz inbox", "dodaj wyniki".
---

# Import z inbox/

Postępuj zgodnie z sekcją „Jak pracować z inbox/” w CLAUDE.md. Poniżej szczegóły.

## Krok 0 – kontekst
Przeczytaj `profile/profile.md`, `profile/medications.md` i `data/labs/reference.md`. Wylistuj `inbox/` (pomiń `README.md`). Jeśli pusto – powiedz to i zakończ.

## Krok 1 – rozpoznanie plików
Dla każdego pliku odczytaj zawartość (Read obsługuje PDF, obrazy, CSV). Zaklasyfikuj: `badania` / `trening` / `pomiary` / `sen` / `dokument` / `nieznany`. Przy `nieznany` zapytaj użytkownika.

## Krok 2 – badania laboratoryjne (PDF/zdjęcie)
1. Wyciągnij: data pobrania (nie data wydruku!), laboratorium, listę markerów: nazwa z dokumentu → kanoniczna wg `reference.md`, wartość, jednostka, norma (ref_low, ref_high), flaga.
2. Uwagi:
   - Normy typu „< 5.0” → `ref_low` puste, `ref_high` 5.0. Normy „> 40” → odwrotnie.
   - Wyniki jakościowe („ujemny”, „nie wykryto”) → `value` jako tekst.
   - Jeśli laboratorium podaje inną jednostkę niż w `reference.md` – zapisz jednostkę z dokumentu, nie przeliczaj po cichu; odnotuj w `notes`.
   - Marker bez wpisu w słowniku → dodaj do `reference.md` w odpowiedniej sekcji.
3. **Pokaż tabelę do potwierdzenia** (data, marker, wartość, jednostka, norma, flaga). Poczekaj na OK / poprawki.
4. Po potwierdzeniu dopisz wiersze do `data/labs/results.csv` (bez usuwania istniejących). Sprawdź, czy nie ma już wyników z tej daty i tego laboratorium – jeśli są, zapytaj, czy to duplikat.
5. Przenieś plik do `archive/labs/<rok>/`, nadając nazwę `YYYY-MM-DD_<laboratorium>_<oryginalna-nazwa>`. Wpisz tę nazwę w `source_file`.

## Krok 3 – eksporty treningowe (CSV)
Rozpoznaj format po nagłówku:
- **Garmin Connect** (Activities.csv): kolumny `Activity Type, Date, Title, Distance, Calories, Time, Avg HR, Max HR, Total Ascent, Training Stress Score®/Aerobic TE, ...`. Czas w `hh:mm:ss`, dystans w km (zależy od ustawień – sprawdź wielkości).
- **Strava** (activities.csv z archiwum): `Activity Date, Activity Name, Activity Type, Elapsed Time (s), Distance (km), Moving Time (s), Max Heart Rate, Average Heart Rate, Elevation Gain, Calories, ...`. Użyj Moving Time. Kolumnę `Activity Gear` (jeśli jest) wpisz do `gear`.
- **Polar Flow**: `Date, Start time, Duration, Sport, Distance (km), Average heart rate (bpm), Max HR, Calories, ...`.
Mapowanie typów na kanoniczne: Running/Trail Running/Treadmill → `bieg`; Cycling/Virtual Ride/Indoor Cycling → `rower`; Swimming/Open Water → `pływanie`; Strength Training/Weight Training → `siłownia`; Walking → `spacer`; Hiking → `wędrówka`; Skiing → `narty`; reszta → `inne` (oryginał do `notes`).

Dla plików powyżej ~30 wierszy napisz skrypt Python (pandas) w scratchpadzie, zamiast przepisywać ręcznie. Zdeduplikuj wobec istniejących `activities.csv` (date + type + duration_min ±1). Pokaż podsumowanie (ile nowych, ile duplikatów, zakres dat, suma km/min po typie) i po OK dopisz. Archiwizuj do `archive/training/<rok>/`.

## Krok 4 – waga, skład ciała, sen
Zmapuj na `measurements.csv` / `sleep.csv`. Withings/Garmin Index eksportują wagę i tłuszcz w osobnych wierszach lub kolumnach – złącz po dacie. Sen: `date` = poranek. Archiwum: `archive/body/<rok>/`.

## Krok 5 – dokumenty lekarskie
Streść w `data/log/journal.md` pod datą dokumentu (rozpoznanie, zalecenia, zmiany leków). Jeśli zmieniają się leki/diagnozy → zaktualizuj `profile/medications.md` / `profile/profile.md` (pokaż zmianę przed zapisem). Oryginał → `archive/docs/<rok>/`.

## Krok 6 – walidacja i podsumowanie
Uruchom `python scripts/validate.py`, napraw błędy. Podsumuj: co dodano (liczby), co wymagało decyzji, co wygląda niepokojąco (wyniki poza normą, duże zmiany vs. poprzednie pomiary) – z zaleceniem, czy warto skonsultować z lekarzem.
