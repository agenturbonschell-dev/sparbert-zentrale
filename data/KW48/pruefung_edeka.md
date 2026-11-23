# Prüfung EDEKA KW48 (Mo. 23. – Sa. 28.11.2026), Weg 1 (Autor)
- Quelle: kaufda.de, EDEKA-Prospekt "Aktuelle Angebote" (Brochure-ID 2501333895, 35 Seiten, "Woche 48 · be", gültig ab Mo. 23.11. bis Sa. 28.11.2026, Berliner Ausgabe laut Titelseite) und kaufda-Einzelangebote von EDEKA (Offer-IDs unten, Bildkacheln mit Preisschild aus dem Prospekt). Von dem Prospekt liefert kaufda öffentlich nur Seite 1 und 2; die übrigen Seiten waren nicht abrufbar.
- Preise per Auge von Seite 1/2 bzw. den Angebotsbildern gelesen und mit dem JSON (`auto/fetch_kaufda.py`, `__NEXT_DATA__` der Sortiment-Seiten) abgeglichen. Gültigkeit laut JSON 22.11. 23:00 UTC bis 28.11. = Mo. 23. – Sa. 28.11. (Ortszeit).
- Handle: offen (`auto/retailers.json`: null), nicht raten. Karte/App: Edeka-App ("APP-PREIS" im Prospekt).
- Hinweis: regionale Ausgabe (Titelseite nennt edeka.de/berlin). Preise können je Markt/Region abweichen.

| Produkt | Hauptpreis / ohne App / Alt (UVP) | Quelle | Bedingung | geprüft |
|---|---|---|---|---|
| Fleischkäse im Brötchen, Stück | 1,50 (Aktion) / - / - | Prospekt S. 1, Offer c978ca83 | nur teilnehmende Märkte mit Backwaren-Bedientheke; Senf oder Ketchup | ja |
| Leerdammer Original, 140 g | App 1,29 / 1,49 (-44%) / UVP 2,69; Rabatt App -52% | Prospekt S. 1, Offer 1d0f4ba6 | APP-PREIS (Edeka-App) | ja |
| Wagner Die Backfrische Salami, 320 g (tiefgekühlt) | App 1,79 / 1,99 (-46%) / UVP 3,69; Rabatt App -51% | Prospekt S. 1, Offer a883dccc | APP-PREIS | ja |
| Iglo Fischstäbchen 450 g (tiefgekühlt) | App 2,49 / 2,79 (-42%) / UVP 4,89; Rabatt App -49% | Offer 8eeddd8d (Bildkachel) | APP-PREIS ("Mega-Black-Week-Preis") | ja |
| Müller Froop 150 g | 0,39 / - / UVP 0,79 (-50%) | Offer 0a17de9e (Bildkachel) | keine | ja |
| GUT&GÜNSTIG Blattsalat-Mischung 150/200 g | 0,85 / - / - | Prospekt S. 2, Offer 924ee4ee | "Discountbillig", keine Karte | ja |
| GUT&GÜNSTIG Spaghetti 500 g | 0,69 / - / - | Offer af58986d (Bildkachel) | keine | ja |
| Mövenpick Edle Komposition Kaffee gemahlen 500 g | App 6,49 / 6,99 (-22%) / UVP 8,99; Rabatt App -27% | Prospekt S. 1, Offer 36274e00 | APP-PREIS (Prospekt nennt auch Eilles, Idee Kaffee) | ja |
| Nescafé Gold Typ Cappuccino 140 g / 125 g | 2,22 / - / UVP 4,29 (-48%) | Offer b115dd9a (Bildkachel) | keine | ja |
| Nestlé Smarties 120/130 g | 1,79 / - / UVP 2,79 (-35%) | Offer d225a86e (Bildkachel) | keine | ja |

## Offen / Grenzen
- Nur Seite 1 und 2 des Prospekts als Vollbild gelesen; die übrigen 8 Produkte stammen aus kaufda-Einzelangeboten (Preis auf dem Bild und im JSON identisch). Weg 2 (unabhängige Prüferin) steht noch aus: FREIGABE: offen.
- "UVP" (Prospektfußnote: Preisempfehlung der Großhandlung bzw. niedrigster Preis der letzten 30 Tage) wird als "UVP" angezeigt, wie im Prospekt.
- Bei Iglo und Leerdammer/Wagner/Mövenpick steht der App-Preis als Hauptpreis und der Preis ohne App in der Plakette.
