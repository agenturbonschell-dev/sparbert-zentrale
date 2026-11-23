# Prüfung 2 (unabhängig): Penny, KW48, 23.–28.11.2026

Quelle: Penny-Prospekt kaufda-ID 2501335698, Seitenbilder (1600 px) S. 1, 11, 12, 13, 22, 23, 24, 47, 48 (Indizes 0, 10, 11, 12, 21, 22, 23, 46, 47) plus strukturierte Angebote (content-viewer-be). Nicht auf pruefung_penny.md gestützt.
Alle Preise, Altpreise, Rabatte, Mengen und Pfand wurden auf dem Seitenbild gelesen und mit den strukturierten Daten gegengeprüft.

| # | Produkt | App (card) | ohne App (price) | UVP/Alt | Rabatt | Menge | Pfand | Gültigkeit laut Quelle | Gültigkeit in Daten | Ergebnis |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Bauer Fruchtjoghurt | 0,39 (Nur mit App) | 0,49 | UVP 0,99 | -60% App (-50% ohne App) | je 250 g | – | Seite: "Ab Mo, 23.11."; Prospekt gesamt Mo 23.–Sa 28.11. (Titel + Fußzeile "KW 48 vom 23.11.–28.11.2026"); nur die strukturierten Daten nennen bis So 29.11. | Mo. 23. – So. 29.11. | Preise ok. **Gültigkeit "So. 29.11." steht nicht auf der Seite** (Seite und Prospekt: bis Sa 28.11.), Beschreibung nennt zugleich 23.–28.11. = Widerspruch |
| 2 | Lavazza Espresso Crema e Aroma | 12,99 (Nur mit App) | 13,99 | UVP 21,99 | -40% App | je 1.000 g, ganze Bohnen | – | Mo 23.–Sa 28.11. | Mo. 23. – Sa. 28.11. | ok |
| 3 | Grünländer Käsescheiben | 1,69 (Nur mit App) | 1,79 | UVP 2,99 | -43% App | je 156 g | – | Mo 23.–Sa 28.11. | gleich | ok |
| 4 | Original Wagner Piccolinis | 1,79 (Nur mit App) | 3,69 | kein UVP | -51% App | je 270 g, 9er | – | Mo 23.–Sa 28.11. | gleich | ok |
| 5 | Mühlenhof Gourmetschinken | 1,49 (Nur mit App) | 1,89 | kein UVP | -21% App | je 150 g | – | Mo 23.–Sa 28.11. | gleich | ok |
| 6 | Müller Milchreis | 0,39 (Nur mit App) | 0,99 | kein UVP | -60% App | je 200 g | – | Mo 23.–Sa 28.11. | gleich | ok |
| 7 | McCain Kroketten-Trio | – | 1,59 | UVP 2,89 | -44% | je 600 g | – | Mo 23.–Sa 28.11. | gleich | ok |
| 8 | Coca-Cola/Fanta/Sprite | 0,99 (Nur mit App) | 1,19 | UVP 1,69 | -41% App (-29% ohne App) | 1,25 l | zzgl. 0,25 € | Mo 23.–Sa 28.11. | gleich | ok |
| 9 | Pepsi 6 × 0,5 l | 3,99 (Nur mit App) | 7,14 | kein UVP | -44% App | 6 × 0,5 l | zzgl. 1,50 € | **Do. 26.–Sa. 28.11.** (Seitenkopf S. 48) | **Mi. 25. – Sa. 28.11.** | Preis, Pfand, Rabatt ok. **Gültigkeit falsch (Mi. 25. statt Do. 26.)** |
| 10 | Jacobs Krönung | 5,99 (Nur mit App) | 9,99 | kein UVP | -40% App | je 500 g, gemahlen | – | Mo 23.–Sa 28.11. | gleich | ok |
| 11 | Ritter Sport Bunte Vielfalt | 0,99 (Nur mit App) | 1,11 | UVP 1,99 | -50% App | je 100 g | – | Mo 23.–Sa 28.11. | gleich | ok |
| 12 | Haribo Fruchtgummi | 0,69 (Nur mit App) | 0,79 | UVP 1,19 | -42% App | Pico-Balla 190 g, Phantasia 205 g | – | Mo 23.–Sa 28.11. (S. 23); auf dem Titel zusätzlich "Ab Mo, 23.11." | gleich | ok |
| 13 | Bahlsen Pick up! | – | 1,99 | UVP 3,29 | -39% | je 5 × 28 g | – | **Do. 26.–Sa. 28.11.** (Seitenkopf S. 47) | **Mi. 25. – Sa. 28.11.** | Preis ok. **Gültigkeit falsch (Mi. 25. statt Do. 26.)** |
| 14 | Persil Universal Megaperls | 4,99 (Nur mit App) | 6,75 | kein UVP | -26% App | 16 WL, 1,04 kg | – | Mo 23.–Sa 28.11. | gleich | ok |
| 15 | Kuschelweich | 1,69 (Nur mit App) | 1,99 | UVP 2,49 | -32% App (-20% ohne App) | 43 WL, 1 l | – | Mo 23.–Sa 28.11. | gleich | ok |

## Beschreibung (auto/caption.py penny … 0)
- "Unbezahlte Werbung / Kostenlose Werbung für @pennydeutschland": vorhanden, Handle stimmt mit auto/retailers.json (handle_ig).
- Gültigkeit "23.11. bis 28.11.": vorhanden, **widerspricht aber der Zeile "Bauer … Mo. 23. – So. 29.11"** (Bauer-Datum nicht belegt, siehe oben).
- "Preise können je Markt abweichen": vorhanden. App/Karte-Hinweis: vorhanden ("mit Penny-App" je Zeile plus Sammelhinweis).
- Hashtags: 5, ok. Genannte Produkte (Index 0) sind alle Mo.–Sa. gültig, kein Tage-Hinweis nötig außer Bauer.
- Preis ohne App steht in der Beschreibung nicht dabei (nur im Video zu prüfen; das Video lag nicht vor).

## Abweichungen
1. Pepsi: Daten "Mi. 25.", Quelle "Do. 26.–Sa. 28.11." (Seitenbild). Grund: strukturierte Daten in UTC (25.11. 23:00 UTC = 26.11. 00:00 Berlin).
2. Bahlsen: Daten "Mi. 25.", Quelle "Do. 26.–Sa. 28.11." (gleicher Grund).
3. Bauer: "bis So. 29.11." nur in Metadaten, nicht auf der Seite; Prospekt und Seite sagen bis Sa 28.11.; Beschreibung widerspricht sich.

FREIGABE: nein – Gültigkeit Pepsi und Bahlsen falsch (Do. 26.11. statt Mi. 25.11.), Bauer "bis So. 29.11." auf der Seite nicht belegt und widerspricht der Beschreibung (23.–28.11.); Preise, App-Bedingungen, Rabatte, Mengen und Pfand aller 15 Produkte stimmen

## Nachprüfung (23.11.2026, nach Korrektur)
- Dateien: out/penny_KW48_ton.mp4 (20:07) ist neuer als penny_products.json (12:41) und templates/angebote_penny.html (13:00); Länge 50,7 s (INTRO 0,6 + 16 Produkte, PER 2,7, CARD_EXTRA 0,4 je App-Produkt, TAIL 4,4).
- JSON: Pepsi "Do. 26. – Sa. 28.11.", Bahlsen "Do. 26. – Sa. 28.11.", Bauer "Mo. 23. – Sa. 28.11." – korrekt.
- Frames (Bauer 2,4 s; Wagner 11,7 s; Coca-Cola 23,7 s; Pepsi 26,8 s; Bahlsen 39,2 s; Persil 41,9 s): Tage im Bild korrekt (Pepsi und Bahlsen Do. 26.–Sa. 28.11., Bauer Mo. 23.–Sa. 28.11.); App-Plakette "Preis mit Penny-App" mit "ohne App"-Preis bei Bauer, Wagner, Coca-Cola, Pepsi, Persil; Pfand bei Coca-Cola (0,25 €) und Pepsi (1,50 €) sichtbar; UVP nur bei Bauer, Coca-Cola, Bahlsen (Quelle nennt UVP), Pepsi, Wagner und Persil ohne UVP; Bahlsen ohne App-Plakette (kein App-Preis); kein abgeschnittener Text.
- Beschreibung (caption.py penny … 0): @pennydeutschland, "Unbezahlte Werbung / Kostenlose Werbung für @pennydeutschland", Gültigkeit 23.11. bis 28.11., "Preise können je Markt abweichen", Hinweis "teils nur mit App/Karte oder an bestimmten Tagen", 5 Hashtags, Genannte Produkte alle Mo.–Sa. (passt); einziges Sonderzeichen ist das Emoji in der Titelzeile (vom Generator vorgesehen).

FREIGABE: ja
