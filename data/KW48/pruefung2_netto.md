# Prüfung 2 (unabhängig): Netto Marken-Discount, KW48 (23.–28.11.2026)

Quelle: kaufda-Prospekt "Aktuelle Angebote" ID 2501339273 (76 Seiten). Offer-API `content-viewer-be.kaufda.de/v1/brochures/2501339273/pages` live abgerufen (Preise, Deals, Bedingungen) und zusätzlich die Seitenbilder (Seiten 1, 2, 23, 32, 37, 44, 54, 55; Nummerierung ab 0: 0, 1, 22, 31, 36, 43, 53, 54) gelesen. Nicht auf pruefung_netto.md gestützt.

Gültigkeit laut Prospekt: Seiten mit Mo. 23.11. – Sa. 28.11.26; Seiten 54/55 "Donnerstag 26.11. – Samstag 28.11.26".

| # | Produkt | Preis (JSON) | App-Preis (JSON) | Alt (JSON) | Save | Quelle (API + Seitenbild) | Tage | Pfand/Limit | Ergebnis |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Melitta Auslese 500 g | 4,99 | 4,49 (+APP) | 8,49 Normalpreis | -47% | 4,49 +APP (-47%), 4,99 (-41%), 8,49 REGULAR; "max. Abgabemenge 4 Packungen" | Mo.–Sa. | Limit steht in unit | ok |
| 2 | Müller Joghurt mit der Ecke 113–150 g | 0,33 | 0,29 (+APP) | 0,89 UVP | -67% | 0,29 +APP (-67%), 0,33 (-62%), UVP 0,89 | Mo.–Sa. | – | ok |
| 3 | Clementinen 2,3-kg-Kiste XXL | 3,49 | – | 4,99 UVP | -30% | 3,49, UVP 4,99, -30%, XXL | Mo.–Sa. | – | ok |
| 4 | Frau Antje Beste Butter 250 g | 0,99 | – | 2,99 UVP | -66% | 0,99, UVP 2,99, -66% (S. 54) | Do.–Sa. | – | ok |
| 5 | iglo Schlemmer Filet 380 g | 2,79 | – | 4,89 Normalpreis | -42% | 2,79, 4,89 (ohne UVP-Label, API REGULAR_PRICE), -42% | Mo.–Sa. | – | ok |
| 6 | Dr. Oetker Ristorante Pizza 640–820 g Doppelpack | 3,49 | – | 6,98 UVP | -50% | 3,49, UVP 6,98, -50%, Doppelpack | Do.–Sa. | – | ok |
| 7 | Volvic Naturelle 1,5 l | 0,69 | – | 1,35 Normalpreis | -48% | 0,69, 1,35 (ohne UVP-Label, REGULAR_PRICE), -48% | Do.–Sa. | zzgl. 0,25 Pfand, steht in note | ok |
| 8 | Hohes C 1 l | 1,79 | – | 2,89 UVP | -38% | 1,79, UVP 2,89, -38% | Mo.–Sa. | zzgl. 0,25 Pfand, steht in note | ok |
| 9 | Meßmer Ländertee 40–50 g | 1,49 | 1,29 (+APP) | 2,39 UVP | -46% | 1,29 +APP (-46%), 1,49 (-37%), UVP 2,39 | Mo.–Sa. | – | ok |
| 10 | Nutella 350–500 g | 2,99 | – | 3,99 UVP | -25% | 2,99, UVP 3,99, -25% | Mo.–Sa. | – | ok |
| 11 | Milka Schokolade 85–110 g | 0,99 | – | 1,99 UVP | -50% | 0,99, UVP 1,99, -50% | Mo.–Sa. | – | ok |
| 12 | Kinder Riegel 327–420 g | 4,44 | 3,99 (+APP) | 5,39 UVP | -25% | 3,99 +APP (-25%), 4,44 (-17%), UVP 5,39 | Do.–Sa. | – | ok |
| 13 | Regina Toilettenpapier Kamille 16 × 150 | 4,99 | – | 6,79 UVP | -26% | 4,99, UVP 6,79, -26% | Mo.–Sa. | – | ok |
| 14 | Palmolive Spülmittel 500–750 ml | 1,29 | – | 1,79 Normalpreis | -27% | 1,29, 1,79 (ohne UVP-Label, REGULAR_PRICE), -27% | Mo.–Sa. | – | ok |

Tage: Die Do.–Sa.-Produkte (Butter, Pizza, Volvic, Kinder Riegel) stehen im JSON mit "Do. 26. – Sa. 28.11."; alle anderen Mo.–Sa. Stimmt mit den Seitenköpfen überein.

## Abweichungen
Keine Abweichung bei Preis, App-Preis, Altpreis, Altpreis-Label, Rabatt, Menge, Tagen, Pfand oder Mengenlimit.

Hinweise (keine Sperre):
- Rabattangaben (-47%, -67%, -46%, -25% bei Kinder Riegel) beziehen sich im Prospekt auf den App-Preis, der im JSON als Hauptpreis (card) steht. Passt zur Regel "App-Preis ist Hauptpreis".
- Mengenlimit Melitta: Quelle "max. Abgabemenge 4 Packungen", JSON "max. 4 pro Kunde". Sinngemäß gleich.
- Prozente beim Rundungsfall (Butter -66%, iglo -42%, Palmolive -27%) entsprechen exakt dem Aufdruck im Prospekt.

## Behaupte-nichts-Prüfung
Kein Altpreis, Rabatt oder Label im JSON, das die Quelle nicht zeigt. Label "UVP" nur dort, wo der Prospekt/die API UVP zeigt; "Normalpreis" nur dort, wo die API REGULAR_PRICE ohne UVP-Aufdruck liefert (Melitta, iglo, Volvic Naturelle, Palmolive).

## Beschreibung (auto/caption.py netto data/KW48/netto_products.json 0)
- "Unbezahlte Werbung / Kostenlose Werbung für @netto_marken_discount": ja; Handle stimmt mit auto/retailers.json (handle_ig) überein.
- Gültigkeit "23.11. bis 28.11.": ja, stimmt mit Prospekt.
- "Preise können je Markt abweichen": ja.
- Hashtags: 5 (#netto #angebote #angebotederwoche #sparen #prospekt), höchstens 5 erfüllt.
- Bedingungen bei genannten Produkten: Melitta 4,49 € mit Netto-App, max. 4 pro Kunde; Müller 0,29 € mit Netto-App; Butter und Pizza mit Do. 26. – Sa. 28.11; Clementinen und iglo ohne Bedingung (stimmt). Zusatzzeile "Angebote teils nur mit App/Karte oder an bestimmten Tagen" vorhanden.
- Preise in der Beschreibung entsprechen der Quelle.

Laufzeit am Postag (23.11.): noch 5 Tage, Regel "mindestens 2 Tage" erfüllt (Do.-Sa.-Angebote starten erst 26.11.; Video zeigt Tage je Produkt).

FREIGABE: ja
