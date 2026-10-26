---
name: raport
description: Okresowy raport zdrowia (miesiąc, kwartał, rok) łączący badania, trening, pomiary ciała, sen, dziennik i leki. Zapisuje do reports/. Np. "/raport wrzesień 2026", "/raport Q3", "/raport" (ostatnie 30 dni).
---

# Raport okresowy

Okres: `$ARGUMENTS` (domyślnie ostatnie 30 dni). Ustal dokładny zakres dat i podaj go w raporcie.

## Zbierz dane
Przeczytaj `profile/*.md`, wczytaj wszystkie CSV z `data/` i `journal.md`. Liczenie i wykresy – Pythonem (pandas/matplotlib), obrazy do `reports/img/`.

## Struktura raportu (`reports/YYYY-MM-raport.md` lub `reports/YYYY-Qn-raport.md`)

1. **Podsumowanie w 5 zdaniach** – najważniejsze rzeczy, które warto wiedzieć.
2. **Badania** – co zbadano w okresie, co poza normą, jak zmieniło się vs. poprzednie pomiary; markery, które według celów warto zbadać, a nie były.
3. **Ciało** – waga (start/koniec/średnia/trend), skład ciała, ciśnienie (średnia, ile pomiarów >140/90), tętno spoczynkowe, HRV. Wykres wagi + RHR.
4. **Trening** – łączna objętość, rozkład po typach, tygodniowa progresja, tętno, najdłuższa/najintensywniejsza jednostka, porównanie z poprzednim okresem. Wykres tygodniowy.
5. **Sen** – średnia długość, odsetek nocy <7h, score, powiązanie z treningiem/samopoczuciem, jeśli dane pozwalają.
6. **Dieta / suplementy / leki** – co się zmieniło, konsekwencja w przyjmowaniu (jeśli logowane).
7. **Dziennik** – powtarzające się objawy, dni gorszego samopoczucia, ich korelacja z resztą danych.
8. **Cele z profilu** – status każdego celu: postęp / stagnacja / regres, z liczbami.
9. **Rekomendacje na kolejny okres** – max 5 punktów, konkretne i mierzalne. Osobno: „do omówienia z lekarzem”, jeśli coś się kwalifikuje.

Zasady: każda liczba z danych, każda interpretacja oznaczona jako interpretacja. Jeśli w danym obszarze brak danych – jedno zdanie o tym i propozycja, jak to zacząć logować. Na końcu w czacie podaj streszczenie i ścieżkę do pliku.
