---
name: badania
description: Analiza wyników badań laboratoryjnych – trend konkretnego markera w czasie (np. /badania ferrytyna), przegląd całego panelu z danej daty, albo ogólny przegląd wszystkiego, co jest poza normą. Używaj przy pytaniach o wyniki krwi, normy, zmiany wartości.
---

# Analiza badań

Argument: `$ARGUMENTS` – nazwa markera (może być alias, np. „Hb”, „witamina D”), data (`2026-05`), albo puste.

## Przygotowanie
1. Przeczytaj `profile/profile.md`, `profile/medications.md`, `data/labs/reference.md`.
2. Wczytaj `data/labs/results.csv`. Jeśli plik ma tylko nagłówek – powiedz, że baza jest pusta i zaproponuj `/import`.

## Tryb A – konkretny marker
1. Zmapuj argument na kanoniczną nazwę (aliasy w `reference.md`). Uruchom `python scripts/trend.py <marker>` – da tabelę, statystyki i wykres w `reports/img/`.
2. Pokaż tabelę: data | wartość | jednostka | norma lab | flaga | laboratorium.
3. Oceń:
   - kierunek i tempo zmian; czy w normie laboratoryjnej; jak wygląda na tle zakresu optymalnego z `reference.md` (**zaznacz, że to orientacyjne**);
   - co mogło wpłynąć: sprawdź w `medications.md` (suplementy/leki w danym okresie), `journal.md` (choroba, stres), `activities.csv` (ciężki trening 1–3 dni przed pobraniem – istotne dla CK, kreatyniny, ALT/AST, leukocytów, ferrytyny), inne markery z tej samej daty (np. ferrytyna + CRP, TSH + fT4);
   - czy różne laboratoria używały różnych metod/jednostek – jeśli tak, ostrzeż przed porównywaniem wprost.
4. Zakończ: 2–4 konkretne wnioski i co dalej (kiedy powtórzyć, o co zapytać lekarza). Bez diagnoz.

## Tryb B – data / panel
Pokaż wszystkie wyniki z tej daty pogrupowane wg sekcji `reference.md`, z wyróżnieniem tych poza normą i tych blisko granicy. Porównaj z poprzednim pomiarem każdego markera (Δ). Zwróć uwagę na wzorce między markerami (np. niskie MCV + niska ferrytyna).

## Tryb C – bez argumentu
Przegląd: (1) markery z flagą L/H w ostatnim pomiarze, (2) markery z wyraźnym trendem (>15% zmiany między dwoma ostatnimi pomiarami lub konsekwentny kierunek w 3+ pomiarach), (3) markery dawno niebadane, które warto powtórzyć w świetle celów z profilu. Zaproponuj, na co patrzyć przy następnym badaniu.
