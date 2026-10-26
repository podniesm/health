---
name: wizyta
description: Przygotowanie do wizyty lekarskiej – zwięzłe streszczenie stanu zdrowia i istotnych danych dla danego specjalisty oraz lista pytań do zadania. Np. "/wizyta endokrynolog", "/wizyta lekarz rodzinny", "/wizyta kardiolog – kontrola ciśnienia".
---

# Przygotowanie do wizyty

Specjalista / cel: `$ARGUMENTS`

1. Przeczytaj `profile/profile.md`, `profile/medications.md`, `data/log/journal.md` oraz CSV istotne dla tej specjalizacji:
   - **lekarz rodzinny / internista** – wszystko, ostatni rok;
   - **endokrynolog** – TSH, fT3, fT4, anty-TPO, kortyzol, testosteron, prolaktyna, glukoza/insulina, witamina D, waga, sen, energia z dziennika;
   - **kardiolog** – ciśnienie (wszystkie pomiary), tętno spoczynkowe, lipidy, glukoza/HbA1c, CRP, treningi (tętno max, objętość), historia rodzinna;
   - **hematolog** – morfologia, ferrytyna, żelazo, B12, foliany, CRP;
   - **gastrolog / hepatolog** – ALT, AST, GGTP, bilirubina, morfologia, dieta, objawy z dziennika;
   - **ortopeda / fizjoterapeuta** – kontuzje z dziennika, obciążenie treningowe ostatnich 8 tyg., witamina D;
   - **dietetyk** – waga, skład ciała, lipidy, glukoza, ferrytyna, witaminy, log żywieniowy, treningi;
   - inny – dobierz sensownie.
2. Przygotuj plik `reports/YYYY-MM-DD_wizyta_<specjalista>.md`:
   - **Kim jestem** (3 linijki): wiek, płeć, aktywność, choroby, leki – z profilu.
   - **Powód wizyty / co mnie niepokoi** – z dziennika i argumentu.
   - **Istotne wyniki** – tabela: marker | ostatnia wartość (data) | poprzednia (data) | norma | trend. Tylko markery istotne dla specjalisty. Wyróżnij poza normą.
   - **Pomiary domowe** – np. ciśnienie: średnia, zakres, liczba pomiarów, wykres, jeśli >10 pomiarów.
   - **Leki i suplementy** – aktualna lista z dawkami.
   - **Pytania do lekarza** – 5–8 konkretnych pytań wynikających z danych (o wyniki graniczne, trendy, interakcje, czy coś powtórzyć, jakie badania rozważyć). Nie sugeruj lekarzowi diagnozy – formułuj jako pytania.
   - **Do zabrania** – które PDF-y z `archive/` warto mieć.
3. Raport ma się zmieścić na 1–2 stronach A4 – lekarz ma minutę na przeczytanie. W czacie pokaż tylko pytania i ścieżkę do pliku.
