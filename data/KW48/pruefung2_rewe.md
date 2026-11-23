# Prüfung 2 (unabhängig): REWE KW48, 23.–28.11.2026

Quelle: REWE-Prospekt "Dein Markt" (kaufda contentId 97b809a0-3ee6-4d53-855a-0cb0a7207449, 24 Seiten). Seitenbilder S. 0, 3, 11, 12, 13, 17 gelesen. Gültigkeit: Titelseite "Gültig ab 23.11.2026", Ende aus API-Metadaten (endDate 28.11.2026 22:00 UTC = Ende Sa. 28.11.). Das Seitenbild nennt kein Enddatum. Ohne Rückgriff auf pruefung_rewe.md.

| # | Produkt (JSON) | Prospekt | Preis | Menge/Einheit | Tage | Pfand | Altpreis/Label | Ergebnis |
|---|---|---|---|---|---|---|---|---|
| 1 | Milka Weihnachtsmann | S.0: 0,99, "1,89*" Letzter Verkaufspreis | ok | 45 g, versch. Sorten (Alpenmilch) ok | Mo–Sa ok | – | 1,89 "zuletzt" ok | ok |
| 2 | Kinder Country | S.0: Kinder Bueno 6×21,5 g oder Country 9×23,5 g, 1,99, "3,29*" | ok | 9×23,5 g, "auch Bueno" ok | ok | – | 3,29 "zuletzt" ok | ok |
| 3 | Milram Gewürzquark | S.0: 0,99, versch. Sorten, 185 g | ok | ok | ok | – | Prospekt zeigt 1,45 (Letzter Verkaufspreis), JSON zeigt keinen: nur Auslassung, nichts Falsches | ok |
| 4 | Ehrmann Almighurt | S.11: 0,44, versch. Sorten, 150 g | ok | ok | ok | – | keiner im Prospekt | ok |
| 5 | Kerrygold Original Irische Butter | S.11: 1,59, Original oder Extra, versch. Sorten, 250 g | ok | ok | ok | – | keiner | ok |
| 6 | Müller Milchreis | S.3: 0,49, versch. Sorten, 200 g | ok | ok | ok | – | keiner | ok |
| 7 | Maggi Ravioli in Tomatensauce | S.12: 1,99, 800-g-Dose | ok | ok | ok | – | keiner | ok |
| 8 | Coca-Cola/Fanta/Sprite/Mezzo Mix | S.0: 11,99, "16,99*" Letzter Verkaufspreis, 12×1 l Kasten | ok | ok | ok | zzgl. 3,30 € ok | Prospekt zeigt 16,99, JSON keinen: nur Auslassung | ok |
| 9 | Pepsi Cola 1,25 l | S.13: 0,69, versch. Sorten, 1,25-l-Fl. | ok | ok | ok | zzgl. 0,25 € ok | Der Altpreis 0,89 auf S.13 gehört zur 0,33-l-Dose, nicht zur 1,25-l-Flasche; JSON zeigt keinen: korrekt | ok |
| 10 | Volvic Touch oder Tee | S.13: 1,19, versch. Sorten, auch als Zero, 1,5 l | ok | ok | ok | zzgl. 0,25 € ok | keiner | ok |
| 11 | Snickers oder Twix | S.17: 1,79, "3,59*" Letzter Verkaufspreis, 5×50 g | ok | ok | ok | – | Prospekt zeigt 3,59, JSON keinen: nur Auslassung | ok |
| 12 | Funny-frisch Chipsfrisch ungarisch | S.17: 1,99, 215 g | ok | ok | ok | – | keiner | ok |
| 13 | Lindt Lindor Milch | S.17: 4,99, 200 g | ok | ok | ok | – | keiner | ok |
| 14 | Pringles Sour Cream & Onion | S.17: 1,49, Santa's Secret 165 g oder Sour Cream & Onion 200 g | ok | 200 g ok | ok | – | keiner | ok |
| 15 | Persil Color Kraft-Gel | S.12: 4,99, 20 WL (oder Megaperls 16 WL, gleicher Preis) | ok | 20 WL ok | ok | – | keiner | ok |

## Altpreise, Rabatt, Bedingungen
- Nur bei Milka (1,89) und Country (3,29) steht ein Altpreis mit Label "zuletzt". Beide Werte stehen so im Prospekt ("Letzter Verkaufspreis", Fußnote: niedrigster Preis der letzten 30 Tage). Bei den übrigen Produkten steht kein Altpreis. Es wird also nichts behauptet, was der Prospekt nicht zeigt. Der Prospekt zeigt bei Milram, Cola-Kasten und Snickers/Twix zusätzlich einen Altpreis, der fehlt. Das ist nur eine Auslassung.
- `save` ist bei allen 15 leer. Die Vorlage zeigt einen Burst nur, wenn `save` gesetzt ist, und berechnet keinen Prozentsatz selbst. Es wird kein Rabatt-Prozentsatz behauptet. Der Altpreis erscheint nur bei gesetztem `old` mit Label (`oldLabel` || "statt"), also hier "zuletzt".
- Prospekt zeigt bei Milram (0,10 €), Cola-Kasten (2,00 €), Almighurt (0,10 €) und Kerrygold (0,10 €) "REWE Bonus" (Guthaben über die App). Das ist keine Preisbedingung: der Regalpreis bleibt der gezeigte Preis. Kein Mangel.
- Mengenlimit: im Prospekt nicht zu erkennen.

## Sorten
Country/Bueno: Prospekt "Bueno oder Country", JSON "auch Bueno" passt. Milka, Milram, Almighurt, Kerrygold, Müller, Volvic und Pepsi stehen mit "versch. Sorten" bzw. dem Prospekttext. Hinweis ohne Mangel: Prospekt nennt bei Cola und Pepsi "koffeinhaltig"; das fehlt im JSON.

## Beschreibung (`auto/caption.py rewe data/KW48/rewe_products.json 0`)
- Enthält "Unbezahlte Werbung / Kostenlose Werbung für REWE", ohne @handle (REWE-Handle ist `null`, nichts erfunden).
- Gültigkeit "23.11. bis 28.11." und "Preise können je Markt abweichen" vorhanden.
- 5 Hashtags (#rewe #angebote #angebotederwoche #sparen #prospekt), also nicht mehr als 5.
- Nennt 6 Produkte, alle mit korrektem Preis.

## Regionale Ausgaben
Die IDs 2501337586 und 2501337929 habe ich nicht geprüft. Unterschiede kann ich dazu nicht nennen.

FREIGABE: ja
