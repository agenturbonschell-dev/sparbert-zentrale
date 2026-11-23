# Prüfung 2 (unabhängig) – ALDI Nord, KW48, 23.–28.11.2026

Quelle: kaufda.de/Geschaefte/Aldi-Nord, Prospekt ID 2501333881 ("Aktuelle Angebote", gültig Mo. 23.11. bis Sa. 28.11.2026). Abgerufen am 23.11.2026. Verglichen wurden die Seitenbilder (Seiten 1 und 2, von der Seite bereitgestellt) und die strukturierten OFFER-Objekte (prices.mainPrice/secondaryPrice/secondaryPriceIsUVP). Die Prüfdatei pruefung_aldi_nord.md wurde nicht herangezogen.

## Produkte (12 von 12 im Bild lesbar und gefunden)

| # | Produkt | Preis JSON / Prospekt | Altpreis JSON / Prospekt | Rabatt JSON / Prospekt | Menge/Einheit | Tage, Pfand, Limit | Ergebnis |
|---|---|---|---|---|---|---|---|
| 1 | Bärenmarke Haltbare Milch | 0,88 / 0,88 | 1,49 UVP / UVP 1,49 | -40% / -40% | 1 l, 1,5 % oder 3,5 % ok | Mo.–Sa.; kein Pfand; kein Limit | ok |
| 2 | Rougette Ofenkäse | 3,79 / 3,79 | 5,99 UVP / UVP 5,99 | -36% / -36% | 320 g ok | Mo.–Sa.; – | ok |
| 3 | Mars/Snickers Eisriegel | 1,99 / 1,99 | 3,69 ohne Label / 3,69 durchgestrichen, ohne "UVP" | -46% / -46% | 5 Stück, 248/252 ml ok | Mo.–Sa.; – | ok (Hinweis A) |
| 4 | Rücker Käsescheiben | 1,29 / 1,29 | 1,99 UVP / UVP 1,99 | -35% / -35% | 100 g ok | "ab Mo. 23.11." (bis Prospektende Sa.) | ok |
| 5 | Hainich Letscho | 1,69 / 1,69 | 2,29 UVP / UVP 2,29 | -26% / -26% | 650 g ok | "ab Mo. 23.11." | ok |
| 6 | Minutensteaks Schweinerücken | 2,29 / 2,29 | 2,99 ohne Label / 2,99 durchgestrichen, ohne "UVP" | -23% / -23% | 400 g ok | Mo.–Sa.; – | ok (Hinweise A, B) |
| 7 | Bio Kulturchampignons braun | 1,49 / 1,49 | 1,89 ohne Label / 1,89 durchgestrichen | -21% / -21% | 250 g ok | Mo.–Sa.; – | ok (Hinweis A) |
| 8 | Rosenkohl | 1,11 / 1,11 | leer / keiner ("AKTION") | leer / keiner | 750 g ok | Mo.–Sa.; – | ok, kein Altpreis/Rabatt behauptet (Hinweis B) |
| 9 | Bio Speisekartoffeln | 1,79 / 1,79 | 1,99 ohne Label / 1,99 durchgestrichen | -10% / -10% | 1,5 kg ok | Mo.–Sa.; – | ok (Hinweis A) |
| 10 | De Beukelaer Prinzenrolle | 1,39 / 1,39 | 2,59 ohne Label / 2,59 durchgestrichen | -46% / -46% | 352 g / 400 g ok | Mo.–Sa.; – | ok (Hinweis A) |
| 11 | Emil Reimann Lebkuchen-Spitzen | 2,69 / 2,69 | leer / keiner ("AKTION") | leer / keiner | 180 g ok | "ab Mo. 23.11."; – | ok, kein Altpreis/Rabatt behauptet |
| 12 | Finish Spülmaschinen-Caps | 9,99 / 9,99 | 14,99 UVP / UVP 14,99 | -33% / -33% | 74 / 82 Caps ok | Mo.–Sa.; – | ok |

Zusätzlich: Die kaufda-OFFER-Daten (mainPrice, secondaryPrice, UVP-Flag) stimmen für alle 12 Produkte mit JSON und Prospektbild überein. Das UVP-Flag von kaufda ist bei Eisriegel, Steaks, Champignons, Kartoffeln, Prinzenrolle "false"; das passt zu den fehlenden "oldLabel" im JSON.

## Abweichungen

Keine Abweichung bei Preis, Altpreis, Rabatt, Menge oder Gültigkeit.

## Hinweise (nicht freigabekritisch)

- A: Bei Eisriegel, Minutensteaks, Champignons, Speisekartoffeln, Prinzenrolle steht der Altpreis im Prospekt nur durchgestrichen, ohne "statt" und ohne "UVP". Die Vorlage setzt dann "statt X €" (Standardlabel, `oldLabel||'statt'`). Das ist eine sprachliche Deutung des durchgestrichenen Preises. Preis und Prozent entsprechen dem Prospekt; kein falsches "UVP" wird behauptet.
- B: Die "Marke" bei Minutensteaks (SCHWEINERÜCKEN) und Rosenkohl (FRISCHE) ist keine Marke im Prospekt, nur Produktbeschreibung. Kosmetisch.
- C: Kein Pfand, kein ausgewiesenes Mengenlimit, kein App-/Kartenpreis im Prospekt. Fußnote im Prospekt: Aktionsartikel nur in begrenzter Anzahl, können schon am Vormittag ausverkauft sein. Der Hinweis fehlt im Text, ist aber kein Mengenlimit je Kunde.
- D: Von der Seite wurden nur Prospektseiten 1 und 2 von 53 bereitgestellt; alle 12 Produkte stehen auf diesen Seiten. Mini-Cherrytomaten, Suppengemüse, Clementinen, Gläser, Erdnüsse stehen im Prospekt, sind aber nicht im JSON (kein Fehler, nur Auswahl).

## Beschreibung (auto/caption.py aldi_nord ... 0)

| Prüfpunkt | Ergebnis |
|---|---|
| "Unbezahlte Werbung / Kostenlose Werbung für @aldinord" | ja; Handle entspricht auto/retailers.json (handle_ig = aldinord) |
| Gültigkeit von–bis | ja, "Gültig 23.11. bis 28.11." (Prospekt: Mo. 23.11.–Sa. 28.11.) |
| "Preise können je Markt abweichen" | ja |
| Hashtags höchstens 5 | ja, genau 5 (#aldi #aldinord #angebote #angebotederwoche #sparen) |
| Preise in der Beschreibung (6 Produkte) | 0,88 / 3,79 / 1,99 / 1,29 / 1,69 / 2,29, alle gleich Prospekt |

Laufzeit am Postag (23.11.): noch 5 Tage, Regel "mindestens 2 Tage" erfüllt.

FREIGABE: ja
