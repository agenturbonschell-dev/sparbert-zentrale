# Prüfung Instagram-Karussells KW48 (23.–28.11.2026)

Prüfabteilung (unabhängig). Geprüft: je 5 Kacheln (alle angesehen), caption.txt, sources.md gegen `data/KW48/*_products.json`, `kaufland_raw.json`, `auto/retailers.json`, `pruefung_*.md`.
Grundpreise selbst nachgerechnet (Preis / Menge x 1000). Prospektseiten selbst nicht neu gelesen, Abgleich mit den bereits geprüften JSONs.

## A: Lidl Top 3 (Nutella, Mövenpick, Landliebe)

| Prüfpunkt | Ergebnis |
|---|---|
| Nutella 450 g: 1,99 € mit Lidl Plus, Normalpreis 3,99 €, -50 %, nur Mo. 23.–Mi. 25.11., max. 3 pro Kunde | stimmt mit JSON und Kachel; Bedingungen stehen auf der Kachel |
| Mövenpick Eis 800–900 ml: 1,79 €, UVP 3,99 €, -55 %, nur Do. 26.–Sa. 28.11. | stimmt |
| Landliebe Joghurt 500 g: 1,11 €, UVP 2,29 €, -51 %, Mo. 23.–Sa. 28.11. | stimmt (1 - 1,11/2,29 = 51,5 %, Prospekt-Aufdruck -51 %) |
| Übersichtskachel 5 | Preise und Tage wie Kacheln 2–4 |
| Kachel 1: „Unbezahlte Werbung / Kostenlose Werbung für @lidlde“ | ja, oben, gut lesbar; Handle laut retailers.json |
| Caption: Kennzeichnung, Gültigkeit, „Preise können je Markt abweichen“, Bedingungen, 5 Hashtags, keine fremden Zeichen | in Ordnung |
| **ABWEICHUNG: Rangbehauptung „Top 3 der Woche“** (Kachel 1 und Caption) | Die Daten geben keinen Rang her. Die Auswahl war nach eigenem Quellen-Vermerk Rabatt plus Bedingungen. Im selben Lidl-Datensatz gibt es höhere Rabatte: Bayernkrone Butter -60 %, Müller Milchreis -52 % (mehr als Nutella -50 % und Landliebe -51 %). „Top 3“ ist damit nicht belegt. |
| Korrektur | Titel ohne Rang, z. B. „3 Lidl-Angebote der Woche“ oder „3 starke Rabatte“, in Kachel 1 und Caption. Danach freigabefähig. |

FREIGABE A: nein – „Top 3“ behauptet einen Rang, den die Daten nicht hergeben (Butter -60 % und Milchreis -52 % liegen vor Nutella/Landliebe); Titel in Kachel 1 und Caption ändern, Preise und Bedingungen sind in Ordnung.

## B: Butter-Preischeck (Lidl, Netto, Kaufland)

Grundpreise: Lidl 0,99/250 g = 3,96 €/kg; Netto 0,99/250 g = 3,96 €/kg; Kaufland 1,15/250 g = 4,60 €/kg (ohne Card 1,29 = 5,16 €/kg, entspricht Kaufland-Angabe 4.60 / 5.16); REWE Kerrygold 1,59/250 g = 6,36 €/kg. Alle Rechnungen stimmen mit den Kacheln.

| Prüfpunkt | Ergebnis |
|---|---|
| Lidl Bayernkrone 0,99 €, UVP 2,49 €, -60 %, Mo.–Sa. | stimmt |
| Netto Frau Antje 0,99 €, UVP 2,99 €, -66 %, nur Do. 26.–Sa. 28.11. | stimmt; Kachel 3 zeigt „Nur Do. 26. – Sa. 28.11.“ rot, Übersicht (Kachel 5) zeigt „nur Do. 26. – Sa. 28.11.“ |
| Kaufland Weihenstephan: Card 1,15 €, ohne Card 1,29 €, statt 2,99 €, -61 % (Card-Rabatt, `loyaltyDiscount` 61), bis Sa. 28.11. | stimmt mit `kaufland_raw.json`; Hauptpreis mit Card, Preis ohne steht dabei |
| Händlerauswahl | Vollständig innerhalb der Daten: Butter finden sich nur bei Lidl, Netto, Kaufland, REWE. Penny, Edeka, Aldi Nord: kein Butterangebot in den JSONs. Aldi Süd: nur Vitareform Margarine (keine Butter). REWE (Kerrygold, Platz 4, 6,36 €/kg) fehlt zu Recht, kein Konto (`null`) und letzter Platz. Hinweis: „vollständig“ gilt nur für die vorliegenden Prospektdaten. |
| Platzierung Lidl/Netto „Platz 1“ beide | vertretbar: gleicher Grundpreis (3,96), Netto-Bedingung (nur Do.–Sa.) steht auf Kachel 3 und in Kachel 5, in der Caption ebenfalls. Lidl gilt die ganze Woche, das ist erkennbar. Kaufland Platz 3 stimmt auch ohne Card (5,16 €/kg). |
| Kaufland „Butter oder Die Streichzarte“ | Quelle: Ein Preis für beide, Menge 250 g, Kaufland-Beschreibung „mildgesäuert, Die Streichzarte auch gesalzen“, Kategorie Molkereiprodukte/Fette. Ob die Streichzarte rechtlich reine Butter ist, steht nicht in den Daten. Die Kachel nennt den vollen Namen und behauptet nichts darüber hinaus; Platz 3 bliebe in jedem Fall (Preis ist so oder so höher als bei Lidl/Netto). Bei Platz 3 ohne Folgen für den Sieger: vertretbar, nur Hinweis. |
| Kachel 1: „Unbezahlte Werbung“ | ja, mit @lidlde, @netto_marken_discount, @kaufland (alle in retailers.json) |
| Caption: Gültigkeit (inkl. Netto Do.–Sa.), „Preise können je Markt abweichen“, 5 Hashtags, keine fremden Zeichen | in Ordnung |
| **ABWEICHUNG: Caption-Zeile „Kaufland nur mit Kaufland Card“** | falsch formuliert: Das Angebot gilt auch ohne Card (1,29 €), nur der günstigere Preis 1,15 € braucht die Card. Die Kachel ist richtig, die Caption nicht. |
| Korrektur | Caption: „Kaufland: 1,15 € mit Kaufland Card (1,29 € ohne).“ Danach freigabefähig. |
| Hinweis Posttag | Netto-Butter läuft erst ab Do. 26.11.; Regel 8 (mind. 2 Tage Restlaufzeit, spätester Postag Do. 26.11.) beachten. Vor Do. posten ist möglich, die Caption nennt den Starttag. |

FREIGABE B: nein – Caption-Zeile „Kaufland nur mit Kaufland Card“ ist falsch (Preis auch ohne Card 1,29 €); nach Korrektur ist B in Ordnung. Kacheln, Grundpreise, Platzierung und Händlerauswahl stimmen.

## C: Schokolade-Preischeck (Kaufland, Netto, Penny)

Grundpreise: Kaufland 2,59/300 g = 8,63, /250 g = 10,36 €/kg; Netto 0,99/110 g = 9,00, /85 g = 11,65 €/kg; Penny 0,99/100 g = 9,90 €/kg (ohne App 1,11 = 11,10 €/kg). Alle stimmen.

| Prüfpunkt | Ergebnis |
|---|---|
| Kaufland Milka 250–300 g: 2,59 €, statt 4,99 €, -48 %, bis Sa. 28.11., kein Kartenpreis | stimmt. Kleiner Hinweis: Kaufland druckt 8,64 € statt 8,63 € (2,59/0,3 = 8,633); die Kachel rechnet mathematisch richtig mit 8,63, Abweichung 1 Cent nur durch Aufrundung der Quelle. |
| Netto Milka 85–110 g: 0,99 €, UVP 1,99 €, -50 %, Mo.–Sa. | stimmt |
| Penny Ritter Sport 100 g: 0,99 € mit Penny-App, ohne App 1,11 €, UVP 1,99 €, -50 %, „versch. Sorten“ | stimmt; App-Bedingung ist Hauptpreis-Kennzeichnung, Preis ohne steht dabei |
| Auswahl | Tafeln mit Mengenangabe. Weitere Treffer (Lidl Ritter Sport Knusperstück 14,95 €/kg, REWE Lindor 24,95 €/kg, REWE Milka Weihnachtsmann 22,00 €/kg) teurer; Kinder/Edeka-Smarties keine Tafeln. Aldi Nord/Süd keine Tafelschokolade. In Ordnung. |
| „Bestes Angebot“ ohne Rang | vertretbar: Die Spannen überlappen (Kaufland 8,63–10,36 gegen Penny 9,90 und Netto 9,00–11,65), kein eindeutiger Sieger. Kachel 1 sagt „Mengenspannen, daher ohne Rangfolge“, Caption ebenso, keine „Platz“-Angabe, Kachel 2–3 „Mengenspanne“. Hinweis: Reihenfolge der Kacheln (Kaufland, Netto, Penny) darf nicht als Rang verstanden werden; die Überschrift „Bestes Angebot“ ist nur Serientitel, den Hinweis „ohne Rangfolge“ nicht entfernen. |
| Kachel 1: „Unbezahlte Werbung“ | ja, mit @kaufland, @netto_marken_discount, @pennydeutschland (retailers.json) |
| Caption: Gültigkeit, „Preise können je Markt abweichen“, App-Bedingung Penny, 5 Hashtags, keine fremden Zeichen | in Ordnung |

FREIGABE C: ja

## Zusammenfassung der Abweichungen

| Karussell | Abweichung | Schwere |
|---|---|---|
| A | „Top 3 der Woche“ (Kachel 1, Caption) behauptet Rang; Butter -60 % und Milchreis -52 % im selben Datensatz höher | blockierend |
| B | Caption „Kaufland nur mit Kaufland Card“ falsch (1,29 € auch ohne Card) | blockierend (Textkorrektur) |
| B | „Butter oder Die Streichzarte“: reine Butter nicht belegt, ohne Einfluss auf Rang | Hinweis |
| B | Netto erst ab Do. 26.11.: Postag spätestens Do. 26.11. (Regel 8) | Hinweis |
| C | Kaufland 8,63 €/kg selbst gerechnet, Quelle zeigt 8,64 | Hinweis |
| C | „Bestes Angebot“-Titel ohne Rang: nur mit Hinweis „ohne Rangfolge“ vertretbar | Hinweis |

FREIGABE A: nein – Rangbehauptung „Top 3“ nicht belegt
FREIGABE B: nein – Caption „Kaufland nur mit Kaufland Card“ korrigieren
FREIGABE C: ja

## Nachprüfung A/B

Geprüft nach Korrektur: alle 5 Kacheln von A und B (angesehen), caption.txt und sources.md beider Karussells, `auto/retailers.json`.

| Prüfpunkt | Ergebnis |
|---|---|
| A: Rang/„Top 3“ | Kachel 1 lautet „3 Lidl-Angebote DER WOCHE“ / „3 starke Rabatte aus dem Lidl-Prospekt“, Caption „Drei Lidl-Angebote der Woche“. Weder in Kacheln noch in Caption oder sources.md eine Rangbehauptung („Top“ kommt nur im Ordnernamen vor, nicht im Inhalt). |
| A: Preise und Bedingungen | unverändert: Nutella 1,99 € mit Lidl Plus (Normalpreis 3,99 €), nur Mo. 23.–Mi. 25.11., max. 3 pro Kunde; Mövenpick 1,79 € (UVP 3,99 €), nur Do. 26.–Sa. 28.11.; Landliebe 1,11 € (UVP 2,29 €), Mo. 23.–Sa. 28.11.; Übersichtskachel 5 stimmt. Kein abgeschnittener Text. |
| B: Kaufland-Formulierung | Caption: „Kaufland 1,15 € mit Kaufland Card (1,29 € ohne).“ sources.md: 1,15 € (card) / 4,60 €/kg, ohne Karte 1,29 € = 5,16 €/kg. Kachel 4: „MIT KAUFLAND CARD 1,15 €“, „ohne Kaufland Card 1,29 €“, 5,16 €/kg ohne Card; Kachel 5: „mit Kaufland Card“. Korrekt. |
| B: übrige Kacheln | unverändert: Lidl 0,99 € = 3,96 €/kg, Mo.–Sa.; Netto 0,99 € = 3,96 €/kg, nur Do. 26.–Sa. 28.11. (Kachel 3 und 5); Kaufland Platz 3 mit 4,60 €/kg. Kein abgeschnittener Text. |
| Kennzeichnung | Kachel 1 und Caption beider Karussells: „Unbezahlte Werbung / Kostenlose Werbung für …“, Gültigkeit, „Preise können je Markt abweichen“ vorhanden. |
| Hashtags | A: #lidl #angebote #angebotederwoche #sparen #lidlplus (5). B: #butter #angebote #angebotederwoche #sparen #preischeck (5). |
| Handles | A: @lidlde. B: @lidlde, @netto_marken_discount, @kaufland. Alle laut `auto/retailers.json` (handle_ig); @spar.bert ist das eigene Konto. |
| Hinweis (unverändert) | B: Netto läuft erst ab Do. 26.11.; spätester Postag Do. 26.11. (Regel 8). |

FREIGABE A: ja – Titel und Caption ohne Rangbehauptung; Preise, Bedingungen, Kennzeichnung, 5 Hashtags und Handle in Ordnung.
FREIGABE B: ja – Kaufland-Zeile korrekt („1,15 € mit Kaufland Card (1,29 € ohne)“) in Caption, sources.md und Kacheln; sonst unverändert und in Ordnung.
