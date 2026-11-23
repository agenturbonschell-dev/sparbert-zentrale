# Sparbert Zentrale

Wöchentliche Angebotsvideos (9:16) mit dem Maskottchen Sparbert für Kaufland, Lidl, Edeka, Penny, Netto, REWE, Aldi.

## Harte Regeln (nie brechen)
1. **Preise müssen stimmen.** Jede Zahl stammt aus der Quelle der jeweiligen Woche und wird vor dem Rendern gegen sie geprüft.
2. **Bedingungen immer zeigen:** App-Preis, Karten-Preis (Kaufland Card, Lidl Plus), nur bestimmte Tage (z. B. Fr.–Sa.), Pfand, Mengenlimit. Der Preis mit Karte/App wird als Hauptpreis gezeigt, der Preis ohne steht dazu. Ein Händler gewinnt einen Preis-Check nur, wenn die Bedingung im Video steht.
3. **„Kein Angebot gefunden“ heißt nur: nichts gefunden.** Händler ohne Treffer werden im Video nicht aufgelistet, im Bericht schon.
4. **Posten:** Der Eigentümer hat vollautomatisches Posten am 23.11.2026 ausdrücklich erlaubt. Gepostet wird nur, wenn die Prüfung bestanden ist (Regel 7), nur auf dem eigenen Konto spar.bert (Instagram, über Windsor), höchstens 2 Beiträge pro Tag und Plattform, Reels und Bildposts zusammengezählt (12:00 und 14:00 Uhr; der Eigentümer will wenige, gut verteilte Posts), nie derselbe Händler zweimal am Tag. Bei jeder Abweichung oder Unsicherheit: nicht posten, Bericht an den Eigentümer. Kein Löschen oder Ändern fremder Konten, keine Kommentare, keine Nachrichten an Händler.
7. **Prüfverfahren (Pflicht vor jedem Post), zwei Wege:** (a) Skript/Auswertung der Quelle (Kaufland: `auto/gegencheck.py` holt live neu und vergleicht jedes Produkt; Exit-Code 0 nötig). (b) Unabhängige Prüferin (zweiter Agent, sieht nur Daten und Quelle, nicht die Auswahl) liest die Prospektseiten und gibt „FREIGABE: ja/nein". Ergebnis steht in `data/<KW>/pruefung_<haendler>.md`. Ohne beide Freigaben wird nicht gepostet. Die „FREIGABE: ja" der Prüfabteilung genügt; eine zusätzliche Freigabe des Eigentümers je Post ist nicht nötig (Eigentümer am 23.11.2026). Nach dem Post: Video aus dem öffentlichen Repo `sparbert-videos` löschen.
8. **Tempo:** Posten täglich um 12:00 und 14:00 Uhr (Berlin), je ein Händler pro Slot, Instagram und TikTok jeweils zum selben Slot; Reihenfolge nach Gültigkeitsbeginn der Angebote; Angebote müssen am Postag noch mindestens 2 Tage laufen (Ausnahme: Eigentümer ordnet es an). Händler laufen getrennt voneinander (eigener Agent je Händler).
5. Beschreibung enthält immer: Gültigkeit von–bis, „Unbezahlte Werbung / Kostenlose Werbung für @Händler“, Hinweis „Preise können je Markt abweichen“.
6. Händler-Konten (@handle) nie raten: `auto/retailers.json`, `null` = offen.

## Organisation
Abteilungen, Übergaben, täglicher Ablauf, Formate und Kennzeichnungsstandard: `ORGANISATION.md`; Rollenanweisungen in `agents/`.

## Quellen
- Kaufland: `https://filiale.kaufland.de/angebote/uebersicht.html` (JSON im Seitenquelltext, `OfferTemplate`; Zeitraum je Kategorie `salesFrom/salesTo`).
- Lidl: Prospekt-API `https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=<id>` (Seitenbilder; Preise von den Bildern lesen).
- Übrige: kaufda.de (`__NEXT_DATA__`), Prospekte erscheinen oft erst Sa./So.; Einzelangebote später.

## Aufbau
- `templates/` HTML-Vorlagen (Canvas): `intro`, `angebote_*`, `preischeck`. Produkte stehen als `PRODUCTS`/`ROWS` oben im Skript.
- `tools/` Rendern (`render3.js`: Playwright → ffmpeg, 2× Auflösung), Freistellen (`grabc.py`, `cut.py`), Sparbert-Posen (`hq*.py`, `toon.py`), Soundeffekte (`sfx.py`).
- `auto/` Händlerliste, Text-Generator (`caption.py`).
- `assets/` Sparbert-Posen, Logos, Hintergründe. Wöchentliche Produktbilder und fertige Videos werden nicht eingecheckt (`.gitignore`).

## Rendern
`node tools/render3.js file://…/templates/<vorlage>.html <startFrame> <endFrame> out.mp4 2` (4 Prozesse parallel, danach `ffmpeg -f concat`).

## Stil
Deutsch, kurz, ohne Hype. Rechte an Produktbildern und Logos liegen bei Händlern und Marken.
