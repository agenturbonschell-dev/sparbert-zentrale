# Sparbert Zentrale – Organisation (Stand 23.11.2026)

Ziel: Jeden Tag die aktuelle Werbung aller Supermärkte als Video (später auch Bild/Karussell) auf Instagram (@spar.bert) und TikTok (@sparbert) posten, mit Kennzeichnung, sauber geprüften Preisen und passenden Hashtags.

## Abteilungen
| Abteilung | Aufgabe | Rollenanweisung |
|---|---|---|
| **Händler-Agenten** (je ein Agent: Kaufland, Lidl, Edeka, REWE, Netto, Penny, Aldi Nord, Aldi Süd) | holen täglich die aktuelle Werbung ihres Händlers, wählen Angebote, bauen Freisteller/Video/Text, melden „bereit zur Prüfung" | `agents/haendler.md` |
| **Prüfabteilung** (unabhängig, sieht nur Daten und Quelle) | prüft jedes Video vor dem Post gegen die Quelle (Preis, App-/Kartenpreis, Tage, Pfand, Limit, Kennzeichnung, Hashtags); gibt „FREIGABE ja/nein"; prüft auch nach dem Post stichprobenartig, ob der Beitrag stimmt | `agents/pruefung.md` |
| **Marketingabteilung** (Mia) | steuert die Händler-Agenten: Reihenfolge, Slots (12:00/14:00), Formate, Hooks, Hashtags, A/B-Tests; liefert täglich neue Ideen (z. B. „Bestes Angebot der Woche: Kaffee/Schokolade", Preis-Checks, Top-3, Bild-/Karussell-Posts) | `agents/marketing.md` |
| **Betrieb** (läuft in der Hauptsitzung) | startet täglich die Agenten, übergibt geprüfte Videos an die Posting-Werkzeuge (Instagram über Windsor, TikTok über Buffer), hält `data/<KW>/posts.md` aktuell, berichtet dem Eigentümer | `agents/betrieb.md` |

## Übergaben (Dateien im Repo)
- `data/<KW>/<haendler>_products.json` → Händler-Agent liefert
- `data/<KW>/pruefung_<haendler>.md` → Prüfabteilung liefert (ohne „FREIGABE: ja" kein Post)
- `marketing/YYYY-MM-DD.md` und `marketing/ideen.md` → Marketing liefert Ideen und Anweisungen
- `data/<KW>/posts.md` → Betrieb protokolliert jeden Post (Zeit, Plattform, Media-ID/Link)

## Täglicher Ablauf (Berlin)
06:07 Mia: Recherche, Ideen, Anweisungen an die Händler-Agenten.
09:03 Betrieb: startet pro Händler einen Agenten (parallel), danach die Prüfabteilung für alle neuen Videos.
12:00 und 14:00 Post-Slots (Instagram + TikTok zugleich). Ein Händler pro Slot, Angebote müssen noch ≥ 2 Tage laufen.
Abends: Betrieb berichtet kurz dem Eigentümer (gepostet, geprüft, offen).

## Kennzeichnung und Hashtags (Standard, immer)
- Beschreibung: „Unbezahlte Werbung / Kostenlose Werbung für @Händler", Gültigkeit von–bis, „Preise können je Markt abweichen. Angebote teils nur mit App/Karte oder an bestimmten Tagen."
- Händler markieren, wenn @handle in `auto/retailers.json` steht (Edeka, REWE: offen, nie raten).
- Höchstens 5 Hashtags: Händler-Tag zuerst, dann #angebote #angebotederwoche #sparen.
- Bild- und Karussell-Posts: zusätzlich auf der ersten Kachel klein „Unbezahlte Werbung".

## Formate
1. Wochen-Angebotsvideo je Händler (Hauptformat, 60 s; Test mit 30 s).
2. „Bestes Angebot der Woche" je Kategorie (Kaffee, Schokolade, Butter, Getränke …) als Preis-Check Reel; nur mit Händlern, die ein Angebot haben.
3. Bild- und Karussell-Posts (Top 5 des Tages, Preis-Check-Tabelle) über Windsor `create_carousel_post`/`create_image_post`.
4. Stories (Erinnerung „Heute neu", „Letzter Tag") über `create_story`.

## Grenzen
Siehe CLAUDE.md. Technisch: Geplante Aufgaben dürfen keine Konnektoren nutzen und Mias Aufgabe darf nicht ins Repo schreiben, solange das Repo nicht als Quelle der Aufgabe eingetragen ist. Posten läuft deshalb über die Hauptsitzung.
