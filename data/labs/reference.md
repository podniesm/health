# Słownik markerów laboratoryjnych

Kanoniczne nazwy używane w kolumnie `test` w `results.csv`. Laboratoria nazywają to samo różnie – kolumna „Aliasy” służy do mapowania przy imporcie. Kolumna „Zakres optymalny” to orientacyjne wartości uznawane za korzystne u zdrowych, aktywnych dorosłych – **nie są** normą laboratoryjną i asystent musi to zaznaczać. Normę lab zapisujemy przy każdym wyniku w `ref_low`/`ref_high`.

Przy imporcie nowego markera, którego tu nie ma – dodaj wiersz.

## Morfologia

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny (orientacyjnie) | Uwagi |
|---|---|---|---|---|
| hemoglobina | HGB, Hb | g/dL | M 14–17, K 12.5–15.5 | |
| hematokryt | HCT | % | | |
| erytrocyty | RBC | mln/µL | | |
| MCV | | fL | 82–95 | niskie → podejrzenie niedoboru żelaza |
| MCH | | pg | | |
| MCHC | | g/dL | | |
| RDW | RDW-CV | % | | |
| leukocyty | WBC | tys/µL | 4–8 | |
| neutrofile | NEUT, NEU | tys/µL | | |
| limfocyty | LYMPH, LYM | tys/µL | | |
| monocyty | MONO | tys/µL | | |
| eozynofile | EOS | tys/µL | | |
| bazofile | BASO | tys/µL | | |
| płytki | PLT, trombocyty | tys/µL | 150–400 | |
| MPV | | fL | | |
| PDW | | fL | | |
| P-LCR | | % | | odsetek dużych płytek |
| PCT | płytkokryt | % | | |
| RDW-SD | | fL | | |
| IG | niedojrzałe granulocyty | tys/µL | | |
| NRBC | erytroblasty | tys/µL | | |
| neutrofile % | NEUT% | % | | odsetek; bezwzględne → `neutrofile` |
| limfocyty % | LYMPH% | % | | |
| monocyty % | MONO% | % | | |
| eozynofile % | EOS% | % | | |
| bazofile % | BASO% | % | | |
| IG % | | % | | |
| NRBC % | | % | | |

## Gospodarka żelazem

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| ferrytyna | | ng/mL | M 50–150, sportowcy ≥50 | rośnie przy zapaleniu – patrz CRP |
| żelazo | Fe | µg/dL | | zmienne dobowo |
| transferyna | | mg/dL | | |
| TIBC | | µg/dL | | |
| saturacja transferyny | TSAT, wysycenie transferyny | % | 25–45 | |

## Lipidy

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| cholesterol całkowity | CHOL, TC | mg/dL | <190 | |
| LDL | LDL-C | mg/dL | <115 (niskie ryzyko), <100 jeśli czynniki ryzyka | |
| HDL | HDL-C | mg/dL | M >40, K >45 | |
| trójglicerydy | TG | mg/dL | <150, optymalnie <100 | na czczo |
| nie-HDL | non-HDL | mg/dL | <145 | |
| ApoB | apolipoproteina B | mg/dL | <90 | |
| Lp(a) | lipoproteina a | nmol/L lub mg/dL | <75 nmol/L (<30 mg/dL) | genetyczne, badać raz |

## Glukoza i metabolizm

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| glukoza | glukoza na czczo | mg/dL | 70–95 | |
| HbA1c | hemoglobina glikowana | % | <5.5 | |
| insulina | insulina na czczo | µIU/mL | 3–8 | |
| HOMA-IR | | | <1.5 | wyliczany: glukoza×insulina/405 |
| kwas moczowy | | mg/dL | M 3.5–6, K 2.5–5.5 | |

## Nerki i elektrolity

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| kreatynina | | mg/dL | | wyższa u umięśnionych, po treningu |
| eGFR | GFR | mL/min/1.73m² | >90 | |
| mocznik | urea | mg/dL | | |
| sód | Na | mmol/L | 137–143 | |
| potas | K | mmol/L | 4.0–4.8 | |
| magnez | Mg | mg/dL | 2.0–2.4 | |
| wapń | Ca | mg/dL | | |
| fosfor | P | mg/dL | | |

## Wątroba

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| ALT | ALAT, GPT | U/L | <30 | rośnie po ciężkim treningu |
| AST | AspAT, GOT | U/L | <30 | rośnie po ciężkim treningu |
| GGTP | GGT | U/L | <30 | |
| bilirubina całkowita | | mg/dL | | |
| ALP | fosfataza zasadowa | U/L | | |
| albumina | | g/dL | 4.2–5.0 | |
| białko całkowite | | g/dL | | |

## Tarczyca

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| TSH | | µIU/mL | 0.5–2.5 | |
| fT4 | FT4, wolna tyroksyna | ng/dL lub pmol/L | środek/górna połowa normy | uwaga na jednostki |
| fT3 | FT3, wolna trijodotyronina | pg/mL lub pmol/L | górna połowa normy | |
| anty-TPO | aTPO | IU/mL | ujemne | |
| anty-TG | aTG | IU/mL | ujemne | |

## Hormony

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| testosteron całkowity | testosteron | ng/mL lub ng/dL | M 5–9 ng/mL | rano, na czczo |
| testosteron wolny | | pg/mL | | |
| SHBG | | nmol/L | | |
| estradiol | E2 | pg/mL | | |
| kortyzol | | µg/dL | | rano; zależny od pory |
| prolaktyna | PRL | ng/mL | | |
| DHEA-S | | µg/dL | | |
| IGF-1 | | ng/mL | | |
| FSH | folitropina | mIU/mL | | |
| LH | lutropina | mIU/mL | | |
| GH | hormon wzrostu | ng/mL | | wydzielanie pulsacyjne – pojedynczy pomiar mało wartościowy |

## Witaminy

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| witamina D | 25-OH-D, 25(OH)D | ng/mL | 40–60 | |
| witamina B12 | B12, kobalamina | pg/mL | >500 | |
| kwas foliowy | folian, B9 | ng/mL | >6 | |
| homocysteina | | µmol/L | <9 | |

## Zapalenie i inne

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| CRP | hs-CRP, białko C-reaktywne | mg/L | <1 | |
| OB | ESR | mm/h | | |
| CK | kinaza kreatynowa | U/L | | bardzo wysokie po treningu – interpretować z datą treningu |
| LDH | | U/L | | |
| PSA | | ng/mL | | |
| TSH-ekstra | | | | |

## Koagulologia

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| APTT | czas częściowej tromboplastyny po aktywacji, czas kaolinowo-kefalinowy | s | | |
| PT | czas protrombinowy | s | | |
| INR | | | | wyliczany z PT |
| wskaźnik protrombinowy | WSK, wskaźnik Quicka | % | | |
| TT | czas trombinowy | s | | |
| fibrynogen | FIBR | mg/dL | | białko ostrej fazy – rośnie w stanie zapalnym |

## Infekcje i serologia

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| HBsAg | antygen HBs, WZW B | | niereaktywny | jakościowe |
| anty-HCV | przeciwciała anty-HCV, WZW C | | niereaktywny | jakościowe |
| borelioza IgG | Borrelia burgdorferi IgG | AU/mL | ujemny | progi zależne od testu – w `notes` |
| borelioza IgM | Borrelia burgdorferi IgM | AU/mL | ujemny | |
| krztusiec IgA | Bordetella pertussis IgA | IU/mL | ujemny | |
| wymaz – posiew mykologiczny | badanie mykologiczne | | brak wzrostu | jakościowe; miejsce pobrania w `notes` |

## Alergologia (IgE swoiste)

| Kanoniczna | Aliasy | Jednostka | Zakres optymalny | Uwagi |
|---|---|---|---|---|
| sIgE D1 D. pteronyssinus | D01 | kU/L | <0.35 (klasa 0) | klasy: 0 <0.35, 1 0.35–0.7, 2 0.7–3.5, 3 3.5–17.5, 4 17.5–50 |
| sIgE D2 D. farinae | D02 | kU/L | <0.35 | |
| sIgE Der p 1 | D202 | kU/L | <0.35 | komponent główny roztocza |
| sIgE Der p 2 | D203 | kU/L | <0.35 | komponent główny roztocza |
| sIgE Der p 10 | D205 | kU/L | <0.35 | tropomiozyna – reakcje krzyżowe (skorupiaki) |
| sIgE Der p 23 | D209 | kU/L | <0.35 | |
| sIgE CCD | marker CCD | kU/L | <0.35 | reaktywność krzyżowa węglowodanowa |

## Mocz (badanie ogólne)

| Kanoniczna | Aliasy | Jednostka | Uwagi |
|---|---|---|---|
| mocz – ciężar właściwy | SG | g/mL | |
| mocz – pH | | | |
| mocz – białko | | | jakościowe: ujemny/ślad/+ |
| mocz – glukoza | | | jakościowe |
| mocz – ketony | | | jakościowe |
| mocz – erytrocyty | | /µL | |
| mocz – leukocyty | | /µL | |
| mocz – przejrzystość | | | jakościowe |
| mocz – barwa | | | jakościowe |
| mocz – urobilinogen | | mg/dL | |
| mocz – bilirubina | | | jakościowe |
| mocz – krew | | | jakościowe (paskowe); ilościowe → `mocz – erytrocyty` |
| mocz – azotyny | | | jakościowe |
