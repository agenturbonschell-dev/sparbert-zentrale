# Sparbert Zentrale

Wöchentliche Angebotsvideos (9:16) mit dem Maskottchen Sparbert für Kaufland, Lidl, Edeka, Penny, Netto, REWE, Aldi.

## Harte Regeln (nie brechen)
1. **Preise müssen stimmen.** Jede Zahl stammt aus der Quelle der jeweiligen Woche und wird vor dem Rendern gegen sie geprüft.
2. **Bedingungen immer zeigen:** App-Preis, Karten-Preis (Kaufland Card, Lidl Plus), nur bestimmte Tage (z. B. Fr.–Sa.), Pfand, Mengenlimit. Der Preis mit Karte/App wird als Hauptpreis gezeigt, der Preis ohne steht dazu. Ein Händler gewinnt einen Preis-Check nur, wenn die Bedingung im Video steht.
3. **„Kein Angebot gefunden“ heißt nur: nichts gefunden.** Händler ohne Treffer werden im Video nicht aufgelistet, im Bericht schon.
4. **Nichts wird ohne Freigabe veröffentlicht**, bis der Eigentümer vollautomatisches Posten ausdrücklich erlaubt.
5. Beschreibung enthält immer: Gültigkeit von–bis, „Unbezahlte Werbung / Kostenlose Werbung für @Händler“, Hinweis „Preise können je Markt abweichen“.
6. Händler-Konten (@handle) nie raten: `auto/retailers.json`, `null` = offen.

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
