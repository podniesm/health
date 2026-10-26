---
name: pomiar
description: Szybki zapis pomiaru ciała lub snu z tekstu potocznego – waga, tłuszcz, obwód pasa, ciśnienie, tętno spoczynkowe, HRV, sen. Np. "/pomiar waga 82.3 ciśnienie 125/80 tętno 54" lub "/pomiar spałem 7h20, score 78". Używaj też, gdy użytkownik bez komendy podaje pomiar.
---

# Zapis pomiaru

Tekst: `$ARGUMENTS`

1. Rozpoznaj wartości:
   - waga → `weight_kg`; tłuszcz/% → `body_fat_pct`; mięśnie → `muscle_kg`; pas/talia → `waist_cm`;
   - ciśnienie `S/D` → `bp_sys`/`bp_dia`; tętno/puls/RHR → `resting_hr`; HRV → `hrv_ms`; stres → `stress_avg`; VO2max → `vo2max`;
   - sen: czas („7h20”, „7:20”, „7.3h”) → `duration_h` (dziesiętnie, 7h20 = 7.33), score, godziny położenia/wstania.
2. Data: dziś, chyba że podano inną („wczoraj”, „20.09”). Czas: jeśli podano („rano”, „7:30”) – wpisz, inaczej puste.
3. Pomiary ciała → dopisz **jeden** wiersz do `data/body/measurements.csv` (pola nierozpoznane puste, `source=manual`). Sen → wiersz do `data/body/sleep.csv`.
4. Wolny komentarz („źle spałem”, „po treningu”) → `notes`.
5. Potwierdź jednym zdaniem, co i pod jaką datą zapisałeś. Jeśli wartość jest nietypowa (waga ±3 kg vs. ostatni pomiar, ciśnienie >140/90 lub <90/60, tętno spoczynkowe ±10 vs. średnia) – zwróć na to uwagę i zapytaj, czy na pewno dobrze odczytałeś.
