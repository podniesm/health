# Mój asystent zdrowia

Prywatna baza danych zdrowotnych + asystent AI (Claude Code). Uruchom `claude` w tym folderze i rozmawiaj.

## Jak zacząć

1. Uzupełnij `profile/profile.md` i `profile/medications.md` (albo powiedz asystentowi, a on wpisze).
2. Wrzuć surowe pliki do `inbox/`: PDF-y badań, zdjęcia wyników, eksporty z Garmina/Strava, wagi itp.
3. Wpisz `/import` – asystent odczyta pliki, pokaże, co znalazł, i po potwierdzeniu zapisze dane do `data/`.
4. Pytaj: „jak zmieniała się ferrytyna?”, „ile biegałem w sierpniu?”, „przygotuj mnie do wizyty u endokrynologa”.

## Skille

| Komenda | Co robi |
|---|---|
| `/import` | Przetwarza wszystko z `inbox/` i archiwizuje źródła |
| `/badania <marker>` | Trend markera w czasie, porównanie z normą i zakresem optymalnym |
| `/trening [okres]` | Analiza obciążenia treningowego, objętości, tętna, regeneracji |
| `/pomiar <tekst>` | Szybki zapis pomiaru: `/pomiar waga 82.3 ciśnienie 125/80` |
| `/dziennik <tekst>` | Wpis do dziennika objawów/samopoczucia |
| `/raport [miesiąc]` | Przegląd okresu: badania, trening, ciało, sen → `reports/` |
| `/wizyta <specjalista>` | Streszczenie + lista pytań przed wizytą lekarską |

## Skrypty pomocnicze

- `python scripts/validate.py` – sprawdza poprawność wszystkich CSV (nagłówki, daty, liczby, duplikaty).
- `python scripts/garmin_sync.py` – synchronizacja z Garmin Connect (`--dry-run` = podgląd, `--since YYYY-MM-DD` = od daty).
- `python scripts/trend.py ferrytyna` – tabela + wykres trendu markera (`reports/img/`).

## Eksport danych ze źródeł

- **Garmin (na bieżąco)**: `python scripts/garmin_sync.py` – pobiera treningi, sen, tętno spoczynkowe, HRV, stres, VO2max i wagę/skład ciała od ostatniej synchronizacji. Pierwsze uruchomienie w zwykłym terminalu (login, hasło, kod MFA); potem bez hasła. Wymaga `pip install garminconnect`.
- **Garmin (eksport ręczny)**: Garmin Connect (web) → Aktywności → Wszystkie aktywności → „Eksportuj CSV”. Pełny eksport konta: garmin.com/account → Zarządzaj danymi → Eksportuj dane.
- **Strava**: Ustawienia → Moje konto → Pobierz lub usuń konto → „Poproś o archiwum” → w paczce plik `activities.csv`.
- **Polar**: flow.polar.com → Ustawienia → Prywatność → Pobierz dane.
- **Apple Health**: iPhone → Zdrowie → zdjęcie profilowe → Eksportuj wszystkie dane (XML – duży, asystent przetworzy Pythonem).
- **Badania**: PDF z laboratorium (Diagnostyka, ALAB, Synevo udostępniają w panelu pacjenta) lub zdjęcie wydruku.

## Uwagi

- To są dane medyczne. Folder jest na Google Drive – nie udostępniaj go i nie wrzucaj do publicznego repozytorium.
- Asystent nie zastępuje lekarza. Służy do porządkowania danych i przygotowania do rozmowy ze specjalistą.
