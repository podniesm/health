---
name: trening
description: Analiza danych treningowych – objętość tygodniowa, rozkład typów aktywności, tętno, obciążenie, progresja, regeneracja (tętno spoczynkowe, HRV, sen). Też ręczne zapisanie treningu z opisu tekstowego. Używaj przy pytaniach o trening, formę, przetrenowanie, ile biegałem.
---

# Trening

Argument: `$ARGUMENTS` – okres („ostatnie 4 tygodnie”, „sierpień”, „2026”), typ („bieg”), albo opis treningu do zapisania („bieg 10 km 52 min tętno 152”).

## Jeśli argument wygląda jak opis treningu → zapis
Wyciągnij: data (domyślnie dziś), typ (kanoniczny), czas w minutach, dystans km, tętno śr./max, RPE, buty (`gear` – nazwa jak w istniejących wierszach, sprawdź `python scripts/gear.py`), notatki. Dopisz do `data/training/activities.csv` z `source=manual`. Potwierdź jednym zdaniem. Jeśli brakuje czasu lub typu – dopytaj krótko.

## W przeciwnym razie → analiza
1. Przeczytaj `profile/profile.md` (cele!), wczytaj `data/training/activities.csv`, `data/body/measurements.csv`, `data/body/sleep.csv`, `data/log/journal.md`. Domyślny okres: ostatnie 8 tygodni.
2. Do liczenia użyj Pythona (pandas) – nie sumuj w głowie. Przydatne agregaty:
   - tygodniowo: łączny czas, dystans, liczba jednostek, rozkład po typach, średnie tętno, suma `training_load`;
   - tydzień do tygodnia: zmiana objętości w % (skok >20–30% = ryzyko przeciążenia);
   - dla biegu/roweru: tempo/prędkość vs. tętno w porównywalnych jednostkach (efektywność aerobowa);
   - regeneracja: tętno spoczynkowe i HRV z `measurements.csv` (7-dniowa średnia i odchylenie od bazy), długość i jakość snu z `sleep.csv`, waga.
3. Wykres do `reports/img/` (matplotlib): objętość tygodniowa jako słupki po typach + linia tętna spoczynkowego lub HRV, jeśli dane są.
4. Wnioski: co idzie dobrze, gdzie sygnały ostrzegawcze (rosnące tętno spoczynkowe + spadający HRV + gorszy sen + wzrost objętości = przetrenowanie/choroba), jak to się ma do celów z profilu. 2–4 konkretne rekomendacje na najbliższy tydzień. Zaznacz, jeśli dane są zbyt skąpe, by coś wnioskować.
