---
name: dziennik
description: Wpis do dziennika zdrowia (data/log/journal.md) – samopoczucie, energia, objawy, stres, choroba, kontuzja, notatki z wizyt. Np. "/dziennik od rana ból głowy, energia 4/10". Używaj też, gdy użytkownik opisuje, jak się czuje.
---

# Wpis do dziennika

Tekst: `$ARGUMENTS`

1. Data: dziś, chyba że podano inną.
2. Otwórz `data/log/journal.md`. Jeśli jest już sekcja `## <data>` – dopisz punkty pod nią; jeśli nie – dodaj nową sekcję **na końcu pliku** (chronologia, najnowsze na dole).
3. Ustrukturyzuj wpis w punkty: `samopoczucie: X/10`, `energia: X/10`, `objawy: ...`, `notatki: ...` – używaj tylko tych, które wynikają z tekstu. Nie wymyślaj ocen, których użytkownik nie podał.
4. Jeśli wpis zawiera też pomiar (waga, ciśnienie) lub trening – zapisz je dodatkowo do właściwego CSV (jak `/pomiar`, `/trening`).
5. Jeśli wpis zawiera zmianę leku/suplementu → zaktualizuj `profile/medications.md` i powiedz o tym.
6. Potwierdź jednym zdaniem. Jeśli objaw jest alarmowy (ból w klatce, duszność, omdlenie, nagłe zaburzenia widzenia/mowy, silny ból głowy „najgorszy w życiu”, krew w stolcu/moczu) – powiedz wprost, że to wymaga pilnej konsultacji.
