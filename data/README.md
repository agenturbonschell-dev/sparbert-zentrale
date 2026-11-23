Wöchentliche Daten je KW kommen hierher (data/KW48/…).

## kaufda-Händler (Edeka, REWE, Netto, Aldi, Penny) – Stand 23.11.2026
- `auto/fetch_kaufda.py <Slug> <out.json>` liefert je Händlerseite ca. 16 strukturierte Angebote (Preis, Altpreis, Bedingung wie „APP-PREIS", Gültigkeit). Slugs: Edeka, REWE, Netto-Marken-Discount, Aldi-Nord. Aldi-Sued und Penny liefern über diese URL keine Daten (Penny: 404, Aldi Süd: 0).
- Die Seite zeigt nur eine Auswahl (inkl. Nicht-Lebensmittel, Alkohol); die vollständigen Angebote stecken in den Prospektseiten (Bilder).
- Die Angebotsbilder sind Prospekt-Ausschnitte mit Preisschild und Text, keine sauberen Freisteller. Für Videos in Kaufland-/Lidl-Qualität braucht es Freisteller (GrabCut je Produkt) oder eine andere Bildquelle.
