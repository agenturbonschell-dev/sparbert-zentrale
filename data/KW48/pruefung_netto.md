# Prüfung Netto Marken-Discount, KW 48 (Mo. 23. – Sa. 28.11.2026)

Weg 1 (Auswertung der Quelle). Stand: 23.11.2026. Noch nicht: Weg 2 (unabhängige Prüferin, FREIGABE ja/nein) und Posten-Freigabe.

## Quelle
- kaufda.de, Händlerseite `Netto-Marken-Discount`, Prospekt "Aktuelle Angebote" (Netto Marken-Discount, publisher DE-1034), ID 2501339273 / contentId 1460efb2-9ae2-4ec0-998a-b72f2f3f337f, 76 Seiten, gültig laut Titelseite "Montag 23.11. – Samstag 28.11.26".
- Strukturierte Seitendaten (Angebote je Seite mit Preisen/Bedingungen): `https://content-viewer-be.kaufda.de/v1/brochures/2501339273/pages?partner=kaufda_web&lat=52.5&lng=13.4` (Abruf mit Berliner Koordinaten; Preise können je Markt abweichen). Auszug aller 404 Angebote: `data/KW48/netto_raw_offers.json`.
- Jede Zahl unten wurde zusätzlich auf dem Seitenbild des Prospekts (zoomlarge-Seite) abgelesen. API-Werte und Seitenbild stimmen bei allen 14 Produkten überein.
- "Seite" = gedruckte Seitenzahl (API-Seite 0 = Seite 1). Beschriftung wie im Prospekt: "UVP" nur, wenn dort UVP steht; durchgestrichener Preis ohne Beschriftung = "Normalpreis" (API: REGULAR_PRICE).

## Produkte
| Produkt | Preis (Hauptpreis) / ohne App / Alt | Quelle (Seite, Angebots-ID) | Bedingung | geprüft |
|---|---|---|---|---|
| Melitta Auslese Klassisch, Kaffee gemahlen 500 g | 4,49 mit App / 4,99 ohne / 8,49 Normalpreis, -47% | S. 1, c7be9bc3-e35c-4ddd-bf1d-409653b1221c | Netto-App-Preis; max. 4 Packungen; Mo.–Sa. | ja |
| Müller Joghurt mit der Ecke 113–150 g | 0,29 mit App / 0,33 ohne / 0,89 UVP, -67% | S. 1, b9c5475c-b108-42c6-874e-751d7067361f | Netto-App-Preis; Mo.–Sa. | ja |
| Clementinen, Griechenland/Spanien, Kl. I, 2,3-kg-Kiste (XXL) | 3,49 / UVP 4,99, -30% | S. 1, 86e6e046-93c9-4199-92b8-f35178931c21 | Mo.–Sa. | ja |
| Frau Antje Beste Butter 250 g | 0,99 / UVP 2,99, -66% | S. 54, e9f8ed4e-4f0e-4646-99f9-491345ec922f | nur Do. 26. – Sa. 28.11. | ja |
| iglo Schlemmer Filet 380 g | 2,79 / 4,89 Normalpreis, -42% | S. 2, a8e370d6-1bd1-430f-b942-6fa29f9487b9 | Mo.–Sa. | ja |
| Dr. Oetker Ristorante Pizza, Doppelpack, 640–820 g | 3,49 / UVP 6,98, -50% | S. 55, 6ebba994-f6aa-4e30-94f4-81901013fcfa | nur Do. 26. – Sa. 28.11. | ja |
| Volvic Naturelle 1,5 l | 0,69 / 1,35 Normalpreis, -48% | S. 54, 31ce0c68-4a2f-4596-afee-8d8b18f8ca89 | zzgl. 0,25 € Pfand; nur Do.–Sa. | ja |
| Hohes C versch. Sorten 1 l | 1,79 / UVP 2,89, -38% | S. 23, 32ea9326-87c0-4a52-9886-9da89de3a769 | zzgl. 0,25 € Pfand; Mo.–Sa. | ja |
| Meßmer Ländertee 40–50 g | 1,29 mit App / 1,49 ohne / 2,39 UVP, -46% | S. 37, 1d2054d4-7023-4dcb-94ca-8cca4b559df4 | Netto-App-Preis; Mo.–Sa. | ja |
| Nutella Nuss-Nugat-Creme 350–500 g | 2,99 / UVP 3,99, -25% | S. 2, 1229d2a3-d594-4e22-9245-ca0ce953628b | Mo.–Sa. | ja |
| Milka Schokolade 85–110 g | 0,99 / UVP 1,99, -50% | S. 32, e0d29753-81a0-45c4-8f31-a38f0b0c920b | Mo.–Sa. | ja |
| Kinder Riegel (oder Duplo) 327–420 g | 3,99 mit App / 4,44 ohne / 5,39 UVP, -25% | S. 55, fe0cd3af-612f-4f92-b3cd-90d837a297b6 | Netto-App-Preis; nur Do.–Sa. | ja |
| Regina Toilettenpapier Kamille, 3-lagig, 16 x 150 Blatt | 4,99 / UVP 6,79, -26% | S. 44, 33ad6014-6190-4a16-8b4a-1c9e3b81fd93 | Mo.–Sa. | ja |
| Palmolive Spülmittel 500–750 ml | 1,29 / 1,79 Normalpreis, -27% | S. 44, 2857783f-a2a1-456a-82d4-48b7c484d2ab | Mo.–Sa. | ja |

## Nicht aufgenommen (bewusst)
- Sunil Waschmittel (8,99): gilt laut Prospekt nur Samstag 28.11. (Tag-Bedingung, würde am Postag nicht 2 Tage laufen).
- Leibniz Kekse (App 0,99): Freisteller aus der Quelle am Rand abgeschnitten, nicht sauber.
- Alkohol, Tabak, Protein-Produkte, Non-Food-Exoten, Fleischtheke/loses Obst ohne Marke: nicht ausgewählt.

## Hinweise für Weg 2 / Posten
- Kein Skript `gegencheck` für Netto vorhanden. Wiederholbare Gegenprobe: obige API-URL neu abrufen und je ID Preise (deals SPECIAL_PRICE = App, SALES_PRICE = ohne App/Regulär, RECOMMENDED_/REGULAR_PRICE = UVP/Normalpreis) vergleichen.
- Die App-Preise sind laut Prospekt "+APP"-Preise; ein Gültigkeitszeitraum nur für die App ist nicht gesondert angegeben (gilt wie der Angebotszeitraum).
- Do.–Sa.-Angebote (Butter, Pizza, Volvic, Kinder Riegel): Regel 8 (mind. 2 Tage Restlaufzeit am Postag) bei Postzeitpunkt beachten; spätester Postag für das Video insgesamt: Do. 26.11.
