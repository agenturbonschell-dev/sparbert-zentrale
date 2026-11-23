# Zweitprüfung ALDI SÜD, KW48 (23.–28.11.2026)

Quelle: Prospekt "Gutes für Alle." (kaufda 2501333886, 35 Seiten), Seiten 0, 6, 7, 8, 10, 11 gelesen. Daten: `data/KW48/aldi_sued_products.json` (ohne Rückgriff auf `pruefung_aldi_sued.md`). Seitenkopf aller Fundstellen: "Mo. 23.11. – Sa. 28.11." (Titelseite: "Gültig von Mo. 23.11. – Sa. 28.11."; Entenbrust zusätzlich "ab Mo. 23.11.").

| # | Produkt | Preis | Altpreis (Quelle: durchgestrichen) | Rabatt | Menge | Tage | Seite | Ergebnis |
|---|---|---|---|---|---|---|---|---|
| 1 | Gourmet Gebackene Entenbrust | 1,11 | 1,99 | -44% | 80 g, gekühlt | Mo.–Sa. | 0, 8 | ok |
| 2 | Dr. Oetker Die Ofenfrische | 1,88 | 3,69 | -49% | 390/410 g, TK | Mo.–Sa. | 6 | ok |
| 3 | Barilla Pesto | 1,69 | 3,49 | -51% | 190/200 g | Mo.–Sa. | 6 | ok |
| 4 | Milsani Käse für den Ofen | 1,79 | 2,49 | -28% | 180 g, gekühlt | Mo.–Sa. | 10 | ok |
| 5 | Jack's Farm Chicken Stripes | 2,99 | 3,99 | -25% | 400 g, TK | Mo.–Sa. | 11 | ok |
| 6 | Bellasan Vitareform Margarine | 0,59 | 0,79 | -25% | 250 g | Mo.–Sa. | 10 | ok |
| 7 | Coca-Cola/Fanta/Sprite/MezzoMix | 0,88 | keiner (Quelle: nur "Aktion") | keiner | 1,25-l-Flasche | Mo.–Sa. | 6 | ok, Pfand 0,25 im JSON/Vorlage ("zzgl. 0,25 € Pfand"), kein Altpreis erfunden |
| 8 | Westminster Ingwer-Tee | 0,89 | 1,19 | -25% | 25 Beutel (45 g) | Mo.–Sa. | 10 | ok |
| 9 | Haribo Fruchtgummi | 0,65 | 1,19 | -45% | 160/175 g | Mo.–Sa. | 7 | ok |
| 10 | LU/Oreo Mikado oder Kekse | 1,29 | 2,19 | -41% | 75/176 g | Mo.–Sa. | 7 | ok |
| 11 | Ferrero Kinder Country | 2,39 | 3,29 | -27% | 10 × 23,5 g = 235 g, 1 Riegel gratis | Mo.–Sa. | 7 | ok |
| 12 | Sun Snacks Salzbrezeln | 0,69 | 0,89 | -22% | 250 g | Mo.–Sa. | 11 | ok |

## Behaupte-nichts-Prüfung
- Alle 11 Altpreise und Rabatte stehen im Prospekt (durchgestrichener Preis, Rabattplakette). Die Vorlage beschriftet den Altpreis mit "statt" (Quelle nennt kein Label, zeigt nur Durchstreichung): sachlich ok, kein UVP-Anspruch.
- Cola: kein Altpreis, kein Rabatt im JSON und in der Vorlage. ok.
- Vorlage `templates/angebote_aldi_sued.html` stimmt für alle 12 Produkte (Preis, Alt, Rabatt) mit dem JSON überein; keine App-/Karten-Plakette (CARDNAME leer). Prospekt: "Günstig ohne Bonus-App", also korrekt.
- Mengenlimit: nur der allgemeine Prospekt-Hinweis "nur in begrenzter Anzahl, teils vorzeitig ausverkauft", kein produktbezogenes Limit. Nichts zu zeigen.
- Prospekt-Sternchen an den Preisen: Fußnote dazu nicht gefunden/gelesen, ohne Auswirkung auf die Zahlen.

## Beschreibung (`python3 auto/caption.py aldi_sued data/KW48/aldi_sued_products.json 0`)
- "Unbezahlte Werbung / Kostenlose Werbung für @aldisuedde": ja (Handle = `retailers.json`).
- Gültigkeit 23.11. bis 28.11.: ja, korrekt.
- "Preise können je Markt abweichen": ja.
- Hashtags: 5 (#aldi #aldisued #angebote #angebotederwoche #sparen): ok.
- Preise der 6 genannten Produkte stimmen mit Quelle.
- **Abweichung:** Der Satz "Angebote teils nur mit App/Karte oder an bestimmten Tagen." behauptet eine Bedingung, die es bei ALDI SÜD nicht gibt (alle Angebote Mo.–Sa., keine App/Karte, Prospekt wirbt ausdrücklich "ohne Bonus-App"). Das ist eine nicht belegte Behauptung. Vorschlag: für Aldi diesen Satz weglassen (oder "Pfand extra" nur bei Getränken). Danach freigabefähig.

FREIGABE: nein – Beschreibung (caption.py) enthält unbelegten Satz "teils nur mit App/Karte oder an bestimmten Tagen"; alle 12 Produktdaten stimmen mit der Quelle, nach Korrektur des Satzes wäre Freigabe ja.
