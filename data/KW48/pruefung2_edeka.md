# Prüfung 2 (unabhängig): EDEKA, KW48 (23.–28.11.2026)

Quelle: kaufda-Prospekt "Aktuelle Angebote" ID 2501333895 (35 Seiten, Kopfzeile "Woche 48 · Gültig ab Montag, 23.11.2026 bis Samstag, 28.11.2026"). Offer-Schnittstelle `content-viewer-be.kaufda.de/v1/brochures/2501333895/pages` live abgerufen (deals, conditions, publicationProfiles) und für alle 10 Produkte das Angebotsbild (main.jpg) gelesen; dazu Seite 0 und 10 und die Fußzeilen/Randtexte (Seite 0, 7, 10, 18) per Bild und Texterkennung. Nicht auf pruefung_edeka.md gestützt.

Gültigkeit laut API: alle 10 Angebote 23.11.2026 00:00 bis 28.11.2026 (Salat, Froop, Nescafé, Smarties 22:00 Uhr), keine Tagesbeschränkung. Kein Pfand, kein Mengenlimit bei den 10 Produkten.

| # | Produkt (JSON) | price | card (App) | alt / Label | save | Quelle (API + Bild) | Ergebnis |
|---|---|---|---|---|---|---|---|
| 1 | Fleischkäse im Brötchen | 1,50 | – | – | – | 1,50 "AKTION", Stück, "wahlweise mit Senf oder Ketchup"; Fußnote *** "Erhältlich in teilnehmenden Märkten mit Bedientheke für Backwaren" | ok (Hinweis 3) |
| 2 | Leerdammer Original 140 g | 1,49 | 1,29 | 2,69 UVP | -52% | 1,49 (-44%), APP-PREIS 1,29 (-52%), UVP 2,69, "Mit APP" | ok (Hinweis 1, 2) |
| 3 | Wagner Die Backfrische Salami 320 g | 1,99 | 1,79 | 3,69 UVP | -51% | 1,99 (-46%), APP-PREIS 1,79 (-51%), UVP 3,69 | ok (Hinweis 1, 2) |
| 4 | Iglo Fischstäbchen 450 g | 2,79 | 2,49 | 4,89 UVP | -49% | 2,79 (-42%), APP-PREIS 2,49 (-49%), UVP 4,89 | ok (Hinweis 1, 2) |
| 5 | Müller Froop 150 g | 0,39 | – | 0,79 UVP | -50% | 0,39, UVP 0,79, -50% | ok |
| 6 | Gut&Günstig Blattsalat-Mischung 150/200 g | 0,85 | – | – | – | 0,85 "Discountbillig", Angebotstext "Salatmischung" (Packung: "Blattsalat-Mischung") | ok (Hinweis 4) |
| 7 | Gut&Günstig Spaghetti 500 g | 0,69 | – | – | – | 0,69; Angebotstext "Teigwaren, 100% Hartweizengrieß, versch. Ausformungen"; "Spaghetti" nur auf der Packungsabbildung | ABWEICHUNG |
| 8 | Mövenpick Edle Komposition 500 g | 6,99 | 6,49 | 8,99 UVP | -27% | 6,99 (-22%), APP-PREIS 6,49 (-27%), UVP 8,99 | ok (Hinweis 1, 2) |
| 9 | Nescafé Gold Cappuccino 140/125 g | 2,22 | – | 4,29 "UVP" | -48% | 2,22, durchgestrichen "4.29*", -48%. API-Typ REGULAR_PRICE (nicht RECOMMENDED_RETAIL_PRICE). Das * bedeutet laut Randtext "Entspricht dem niedrigsten Gesamtpreis der letzten 30 Tage", nicht UVP | ABWEICHUNG |
| 10 | Nestlé Smarties 120/130 g | 1,79 | – | 2,79 UVP | -35% | 1,79, UVP 2,79, -35% | ok |

## Abweichungen (sperren die Freigabe)
1. **Nescafé, Altpreis-Label falsch:** JSON `oldLabel: "UVP"` für 4,29. Die Quelle zeigt 4,29 mit Sternchen = niedrigster Gesamtpreis der letzten 30 Tage, API `REGULAR_PRICE`. Es gibt kein UVP-Label. Muss "Normalpreis" (oder ohne Label) heißen. Vorgabe: Label "UVP" nur, wenn die Quelle UVP zeigt (die UVP-Fälle Leerdammer, Wagner, Iglo, Froop, Mövenpick, Smarties sind belegt).
2. **Spaghetti:** Das Angebot ist "Teigwaren, versch. Ausformungen" (je 500 g, 0,69). Dass es Spaghetti sind, zeigt nur die Packungsabbildung, nicht der Angebotstext. Name im JSON/Video muss "Teigwaren (versch. Ausformungen)" lauten, sonst wird etwas behauptet, was das Angebot nicht zusagt.

## Hinweise
1. **App-Bezeichnung nicht ausdrücklich belegt:** Die Angebotsbilder zeigen nur "APP-PREIS**" bzw. "Mit APP". Die Fußnote zu "**" habe ich in den Prospektseiten (Bild und Texterkennung über alle 35 Seiten, Ränder und Fußzeilen) nicht gefunden. Ein Hinweis auf die EDEKA App steht nur auf Seite 8 (Nummer 7): "Nicht mit EDEKA App Rabatten kombinierbar!". Dass der App-Preis zur Edeka-App gehört, ist im Prospekt-Kontext sehr wahrscheinlich, aber nicht als Satz belegt. Empfehlung: im Video "App-Preis" ohne Namen oder "Edeka-App" nur, wenn der Eigentümer es bestätigt; sonst Beschreibung auf "mit App" umstellen.
2. Rabatt-Prozente: -52, -51, -49, -27 gehören zum App-Preis (als Hauptpreis); die Prozente für den Preis ohne App stehen im Bild anders (-44, -46, -42, -22) und sind im JSON nicht enthalten. Konsistent mit Regel "App-Preis ist Hauptpreis". Der Preis ohne App steht als `price` dabei.
3. Fleischkäse: "nur in teilnehmenden Märkten" stimmt sinngemäß; vollständig lautet die Quelle "teilnehmende Märkte mit Bedientheke für Backwaren". Kein Fehler, aber die Beschreibung nennt die Einschränkung nicht (siehe Beschreibung). Die Marke "EDEKA" im JSON für den Fleischkäse steht im Angebot nicht als Marke (nur Titel); unkritisch.
4. Salat: Angebotstext "Salatmischung", Packung "Blattsalat-Mischung" – Name im JSON deckt sich mit der Packung, nicht dem Angebotstext. Unkritisch.
5. Gültigkeit: Prospekt Mo. 23. – Sa. 28.11., JSON identisch. Ende bei einigen Angeboten laut API 28.11. 22:00 Uhr, im JSON nicht angegeben, unkritisch.

## Beschreibung (`python3 auto/caption.py edeka data/KW48/edeka_products.json 0`, Exit 0)
- "Unbezahlte Werbung / Kostenlose Werbung für Edeka": ja. Kein @handle erfunden; `auto/retailers.json` hat für Edeka `handle_ig`/`handle_tt` = null (offen). Gleichzeitig steht kein @Edeka-Tag im Text, wie vorgesehen.
- Gültigkeit "23.11. bis 28.11.": ja, stimmt.
- "Preise können je Markt abweichen": ja. Zusatz "Angebote teils nur mit App/Karte oder an bestimmten Tagen": ja.
- Hashtags: 5 (#edeka #angebote #angebotederwoche #sparen #prospekt), höchstens 5 erfüllt.
- Preise in der Beschreibung (1,50; 1,29; 1,79; 2,49; 0,39; 0,85) entsprechen der Quelle.
- Mängel: (a) "(mit Edeka-App)" wie Hinweis 1, Name der App nicht ausdrücklich belegt. (b) Der Fleischkäse steht ohne "nur in teilnehmenden Märkten" in der Liste (Regel 2: Bedingung zeigen; die allgemeine Zeile ersetzt das nicht). (c) Preise ohne App (1,49 / 1,99 / 2,79) stehen in der Liste nicht dabei.

## Behaupte-nichts-Prüfung
Alle Altpreise bis auf Nescafé (Abweichung 1) und alle Rabatte entsprechen Bild und API. Alle anderen Preise, App-Preise, Mengen, Tage stimmen. Abweichung 2 (Spaghetti) behauptet eine Sorte, die der Angebotstext nicht nennt.

FREIGABE: nein – Nescafé-Altpreis 4,29 fälschlich als "UVP" gelabelt (Quelle: 30-Tage-Tiefstpreis/Normalpreis); "Spaghetti" im Angebot nur "Teigwaren, versch. Ausformungen"; Beschreibung ohne Fleischkäse-Einschränkung. Nach Korrektur erneut prüfen.

## Nachprüfung

Geprüft nur die Korrekturen.

**JSON (data/KW48/edeka_products.json):** Nescafé `oldLabel` = "Normalpreis" (ok, entspricht REGULAR_PRICE/30-Tage-Tiefstpreis der Quelle). Teigwaren: Name "Teigwaren", unit "je 500 g · versch. Ausformungen" (ok, entspricht Angebotstext). Übrige UVP-Labels unverändert und laut Erstprüfung belegt.

**Beschreibung (`python3 auto/caption.py edeka data/KW48/edeka_products.json 0`):** Kennzeichnung "Unbezahlte Werbung / Kostenlose Werbung für Edeka" vorhanden, kein erfundener @handle (retailers.json: null). Gültigkeit 23.11. bis 28.11. korrekt. "Preise können je Markt abweichen" vorhanden. 5 Hashtags (max. 5 ok). Fleischkäse mit "(nur in teilnehmenden Märkten)", App-Preise als "mit App". Alle Preise stimmen mit der Quelle überein. Mängel (a) und (b) aus der Erstprüfung behoben. Offen bleibt nur das frühere Nebenthema (c), die Preise ohne App stehen nicht in der Liste; die Preise ohne App stehen im Video, nicht kritisch.

**Video-Template (templates/angebote_edeka.html):** Plakette "Preis mit App" / "ohne App" ist korrekt (CARDNAME='App'). Die Anzeige "Normalpreis 4,29 €" (oldLabel + Altpreis, durchgestrichen, Schrift 36 px) wäre sinnvoll und passt in die Breite. ABER: Das Template liest die JSON nicht, sondern enthält eine eigene eingebettete `PRODUCTS`-Liste, und diese wurde nicht korrigiert:
- Zeile ca. 102: `"name": "Spaghetti"`, `"unit": "je 500-g-Beutel"` (statt "Teigwaren" / "je 500 g · versch. Ausformungen")
- Zeile ca. 133 bzw. 145 (Nescafé): `"oldLabel": "UVP"` (statt "Normalpreis")
Das gerenderte Video würde damit weiterhin die beiden gesperrten Fehler zeigen. Zusätzlich nennen Kommentare (Zeile 147, 152) noch "Edeka-App", sichtbar im Video nicht relevant.

FREIGABE: nein – Video-Template enthält eigene, unkorrigierte PRODUCTS-Liste (Nescafé oldLabel "UVP", "Spaghetti"/"je 500-g-Beutel"); JSON und Beschreibung sind korrekt. Nach Angleichung des Templates an die JSON erneut prüfen.

## Endprüfung

- (a) templates/angebote_edeka.html und templates/_build_edeka.html (identisch): kein "Spaghetti", kein "je 500-g-Beutel"; Nescafé hat oldLabel "Normalpreis". Die 6 übrigen "UVP" gehören zu Leerdammer, Wagner, Iglo, Froop, Mövenpick, Smarties und stimmen mit der JSON überein.
- (b) Alle 10 Produkte der Vorlagen-PRODUCTS-Liste sind identisch zu data/KW48/edeka_products.json (Preis, card, old, oldLabel, valid, note, name, unit): 0 Abweichungen.
- (c) out/edeka_KW48_ton.mp4 (Änderungszeit 12:35:15) ist älter als edeka_products.json (12:39:40) und die Vorlage (12:40:30), also NICHT neu gebaut. Frames bestätigen es: bei 24,5 s steht "Spaghetti / je 500-g-Beutel", bei 32 s "UVP 4,29 €" beim Nescafé.

FREIGABE: nein – Video out/edeka_KW48_ton.mp4 ist noch mit den alten Daten gerendert (Spaghetti, Nescafé "UVP"); Vorlage und JSON sind korrekt, nach Neubau erneut prüfen.

## Endprüfung 2

- (a) out/edeka_KW48_ton.mp4 (19:42:38) ist neuer als data/KW48/edeka_products.json (12:39:40), templates/angebote_edeka.html (13:00:09) und templates/_build_edeka.html (19:39:42); beide Vorlagen sind inhaltlich identisch. Länge 33,6 s = Intro 0,6 + Produkte (10 × 2,7 + 4 × 0,4) + Abspann 4,4.
- (b) Frames bei Produktstart + ca. 1,4 s (START aus _build_edeka.html):
  - Fleischkäse im Brötchen (2,0 s): 1,50 €, Hinweis "nur in teilnehmenden Märkten" sichtbar, OK.
  - Leerdammer (5,0 s): 1,29 € "Preis mit App", "ohne App: 1,49 €", "UVP 2,69 €", OK.
  - Wagner (8,1 s): 1,79 € "Preis mit App", "ohne App: 1,99 €", "UVP 3,69 €", OK.
  - Iglo (11,2 s): 2,49 € "Preis mit App", "ohne App: 2,79 €", "UVP 4,89 €", OK.
  - Mövenpick (22,4 s): 6,49 € "Preis mit App", "ohne App: 6,99 €", "UVP 8,99 €", OK.
  - Teigwaren (19,6 s): Titel "Teigwaren", "je 500 g · versch. Ausformungen", 0,69 €, OK. Das Packungsbild trägt den Aufdruck "Spaghetti" (Produktfoto, kein Text des Videos), unkritisch.
  - Nescafé (25,3 s): "Normalpreis 4,29 €" statt UVP, 2,22 €, OK. Kosmetisch: Die Altpreiszeile ist wegen der Länge des Wortes rechts knapp am Rahmen und das "€" ragt leicht unter den Rahmen; Zahl und Label sind lesbar, keine Beanstandung.
  - Keine "Edeka-App"-Beschriftung mehr im Bild, nur "App".
- (c) auto/caption.py edeka data/KW48/edeka_products.json 0: Kennzeichnung "Unbezahlte Werbung / Kostenlose Werbung für Edeka" ohne erfundenen @handle, Gültigkeit 23.11. bis 28.11., "Preise können je Markt abweichen", 5 Hashtags, Fleischkäse "(nur in teilnehmenden Märkten)", App-Preise mit "(mit App)". OK.

FREIGABE: ja
