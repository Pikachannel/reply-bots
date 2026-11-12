# Bluesky Reply Bots

<p align="left">
  <a href="SV_README.md"><img src="https://img.shields.io/badge/Språk-Svenska-blue?style=flat-square" alt="Svenska"></a>
</p>

<p align="left">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=flat-square" alt="English"></a>
</p>

## Übersicht

Dieses Repo enthält den Code für:
- Whimsy Miku Bot (whimsy.pikachannel.xyz)
- Evil Teto Bot (evil.pikachannel.xyz)

## Inhaltsverzeichnis
- [Overview](#overview)
- [Die Bots!](#the-bots)
  - [Derzeitige Features](#derzeitige-features)
  - [Nutzung](#nutzung)
  - [Content-Filterungssystem](#content-filterungssystem)
    - [Filter System](#filter-system)
    - [Posts löschen](#posts-löschen)
  - [Einstellungen](#einstellungen)
    - [Einstellungen synchronisieren](#einstellungen-synchronisieren)
    - [Spitzname](#spitzname)
    - [Post Chance](#post-chance)
    - [Post Intervall](#post-interval)
    - [Posts überspringen](#posts-überspringen)
    - [Sprache](#sprache)
- [Datenschutzrichtlinie](#datenschutzrichtlinie)
  - [Rahmen der Datenerfassung, nutzung, Speichern und Sicherheit](#rahmen-der-datenerfassung-nutzung-speichern-und-sicherheit)
  - [Löschen von Nutzerdaten](#löschen-von-nutzerdaten)
- [Lizenz](#lizenz)

---

## Die Bots!
Whimsy Miku antwortet mit positiven Antworten auf deine Posts!

Evil Teto antwortet mit lustig-gemeinen Antworten auf deine Posts.

#### Derzeitige Features
1. **Wählt zufällig vorbestimmte Nachirchten aus**, inklusive:
    - Support für mehrere Sprachen
    - Nachrichten die den Nutzernamen des Nutzers enthalten
2. **Ein Content-Filterungssystem**, inklusive:
    - Ein Post Filterungs
    - Ermöglicht es Nutzern, Antworten unter ihren Beiträgen zu löschen (mehr dazu in [Posts löschen](#Posts-löschen)).
3. **Benutzerdefinierte Spitznamen**: Nutzer können einen benutzerdefinierten Spitznamen festlegen der statt ihrem Bluesky Anzeigenamen benutzt.
4. **Post Chance**: Nutzer können die wahrscheinlichkeit auf eine Antwort auf ihre Posts ändern.
5. **Post Intervall**: Nutzer können den Zeitabstand zwischen Antworten unter ihren Beiträgen anpassen. Für alle Antworten gilt eine Mindestabklingzeit von 60 Sekunden.
6. **Posts überspringen**: Nutzer können ändern, wie viele Posts zwischen den Antworten liegen müssen.
7. **Wort des Tages!**: Evil Teto wird jeden einzelnen Tag ein zufälliges Wort posten.
8. **Sprachauswahl**: Nutzer können die gewünschte Sprache für Bot-Antworten festlegen, aktuelle werden die folgenden Sprachen unterstützt:
    - Englisch (EN)
    - Schwedisch (SV)
    - Deutsch (DE)

### Nutzung
1. Folge dem Bot auf Bluesky
    - Wenn du den Bot blockierst oder entfolgst dann könnte es bis zu 5 Minuten dauern bis der Bot aufhört auf deine Posts zu antworten.

### Content-Filterungssystem

#### Filter System
Das System überspringt Posts wenn einer der folgenden Bedingungen erfüllt werden:

**Post Inhalts Check**
1. Erkennt ob der Post einer der vordefiniert Keywords enthält
2. Erkennt ob der post einen Link oder ein Embed enthält
3. Führt eine Sentiment analyse auf den Post des Nutzers durch und bestimmt ob er negativ, neutral oder positiv ist (Der Code daführ ist derzeit nicht in diesem Repo).

#### Posts löschen
1. Finde die Bot Antwort unter einem deiner Posts.
2. Antworte auf die Bot Antwort mit "delete" und sie wird direkt gelöscht.

### Einstellungen
Du kannst sogar die Einstellungen der Bots konfigurieren! Das kannst du tun, 

indem du einfach einen der Befehle da unten per Direktnachricht an den Bot schreibst.

Um alle deine Einstellungen zu sehen:
1. Sende eine Direktnachricht mit diesem Befehle an den Bot:
    - `settings`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Einstellungen synchronisieren
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Einstellungen des akutellen Bots mit den eines anderen Bots synchonisieren:** `!sync <@other_bot_handle>`
    - **Einstellungen aller anderen Bots mit dem aktuellen Bot synchonisieren:** `!sync <@current_bot_handle>`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    
    
#### Spitzname
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Spitznamen einstellen:** `!nickname <nickname>` (Dein Spitzname kann Maximal 20 Zeichen lang sein)
    - **Spitznamen zurücksetzen:** `!nickname`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Post Chance
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Chance einstellen:** `!chance <chance>` (Muss eine Zahl zwischen 0 und 100 sein)
    - **Chance zurücksetzen:** `!chance`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern. 

#### Post Intervall
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Um einen Statischen Intervall einzustellen:** `!interval <interval>` (Muss eine Zahl zwischen 60 und 3600 sein)
    - **Um einen variablen Intervall einzustellen:** `!interval <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 60 und 3600 sein)
    - **Um den Intervall zurückzusetzen** `!interval`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Posts überspringen
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Um einen Statischen Intervall einzustellen:** `!skip <interval>` (Muss eine Zahl zwischen 0 und 50 sein)
    - **Um einen variablen Intervall einzustellen:** `!skip <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 0 und 50 sein)
    - **Um den Intervall zurückzusetzen** `!skip`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Sprache
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Um die Spracheinstellung einzustellen:** `!language <language>` (z.b.: `!language de` or `!language english`).
    - **Um die Spracheinstellung zurückzusetzen:** `!language`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.

## Datenschutzrichtlinie

### Rahmen der Datenerfassung, nutzung, Speichern und Sicherheit
Der Bot sammelt und nutzt die folgenden Daten:

**Posts der Follower:**
- Der Inhalt und Metadaten der Posts, gespostet von Accounts die dem Bot folgen.
- Informationen von gesammelten Posts werden nicht permanent gespeichert und 
werden nur temporär im Cache des Bots gespeichert.

 **Nutzer Metadaten**
- Nur öffentlich findbaren Informationen wie Nutzernamen und Profil Details.
- Nur die DID (Bluesky Account gebundene ID) wird gespeichert.

**Nutzer Einstellungen**
- Einstellungen die vom Nutzer geändert wurden, z.B: Spitznamen.
- Diese Informationen werden gegen die DID des Nutzers gespeichert.

**Sicherheit und Nutzung**
- Keine Daten werden mit Dritten geteilt.
- Keine Daten werden von KI Modellen genutzt.

### Löschen von Nutzerdaten
Wenn du möchstest das deine Daten von dem Bot gelöscht werden hast du 2 Optionen:

 **Automatische Löschvogang:**
 1. Sende eine Direktnachricht mit diesem Befehlt an den Bot:
    - `!delete` 
 2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.
    
 **Manuelle Löschvorgang**
 1. Kontaktiere Pikachannel mit einer der Folgenden:
    - Bluesky: [pikachannel.xyz](https://bsky.app/profile/pikachannel.xyz)
    - E-Mail:   pikachannel.dev@gmail.com  
 2. Warte auf die Bestätigung das deine Daten von dem Speicher des Bots gelöscht wurden.

## Lizenz

Dieses Github Repo ist Open Source und unter der MIT Lizenz freigegeben.

Siehe [LICENSE](https://github.com/Pikachannel/bluesky-bots/blob/main/LICENSE) für mehr Informationen.
