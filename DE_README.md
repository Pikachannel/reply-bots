# Bluesky Reply Bots

<p align="left">
  <a href="SV_README.md"><img src="https://img.shields.io/badge/Språk-Svenska-blue?style=flat-square" alt="Svenska"></a>
</p>

<p align="left">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=flat-square" alt="English"></a>
</p>

## Übersicht

Dieses GitHub-Repo enthält den Code für:
- Whimsy Miku Bot (whimsy.pikachannel.xyz)
- Evil Teto Bot (evil.pikachannel.xyz)

## Inhaltsverzeichnis
- [Übersicht](#übersicht)
- [Die Bots!](#die-bots)
  - [Derzeitige Features](#derzeitige-features)
  - [Nutzung](#nutzung)
  - [Content-Filterungssystem](#content-filterungssystem)
    - [Filter System](#filter-system)
    - [Posts löschen](#posts-löschen)
  - [Einstellungen](#einstellungen)
    - [Einstellungen synchronisieren](#einstellungen-synchronisieren)
    - [Spitzname](#spitzname)
    - [Post Chance](#post-chance)
    - [Post Intervall](#post-intervall)
    - [Posts überspringen](#posts-überspringen)
    - [Sprache](#sprache)
- [Datenschutzrichtlinie](#datenschutzrichtlinie)
  - [Rahmen der Datenerfassung, Nutzung, Speicherung und Sicherheit](#rahmen-der-datenerfassung-nutzung-speicherung-und-sicherheit)
  - [Löschen von Nutzerdaten](#löschen-von-nutzerdaten)
- [Lizenz](#lizenz)

---

## Die Bots!
Whimsy Miku antwortet mit positiven Antworten auf deine Posts!

Evil Teto antwortet mit lustig-gemeinen Antworten auf deine Posts.

#### Derzeitige Features
1. **Wählt zufällig vorbestimmte Nachrichten aus**, inklusive:
    - Support für mehrere Sprachen
    - Nachrichten, die den Nutzernamen des Nutzers enthalten
2. **Ein Content-Filterungssystem**, inklusive:
    - Ein Post-Filterungssystem
    - Ermöglicht es Nutzern, Antworten unter ihren Posts zu löschen (mehr dazu in [Posts löschen](#Posts-löschen)).
3. **Benutzerdefinierte Spitznamen**: Nutzer können einen benutzerdefinierten Spitznamen festlegen, der statt ihres Bluesky-Anzeigenamens benutzt wird.
4. **Post Chance**: Nutzer können die Wahrscheinlichkeit auf eine Antwort auf ihre Posts ändern.
5. **Post Intervall**: Nutzer können den Zeitabstand zwischen Antworten unter ihren Beiträgen anpassen. Für alle Antworten gilt eine Mindestabklingzeit von 60 Sekunden.
6. **Posts überspringen**: Nutzer können ändern, wie viele Posts zwischen den Antworten liegen müssen.
7. **Wort des Tages!**: Evil Teto wird jeden einzelnen Tag ein zufälliges Wort posten.
8. **Sprachauswahl**: Nutzer können die gewünschte Sprache für Bot-Antworten festlegen, Aktuell werden die folgenden Sprachen unterstützt:
    - Englisch (EN)
    - Schwedisch (SV)
    - Deutsch (DE)

### Nutzung
1. Folge dem Bot auf Bluesky
    - Wenn du den Bot blockierst oder entfolgst, dann könnte es bis zu 5 Minuten dauern, bis der Bot aufhört, auf deine Posts zu antworten.

### Content-Filterungssystem

#### Filter System
Das System überspringt Posts, wenn eine der folgenden Bedingungen erfüllt ist:

**Post Inhalts Check**
1. Erkennt, ob der Post eines der vordefinierten Keywords enthält
2. Erkennt, ob der Post einen Link oder ein Embed enthält
3. Führt eine Sentimentanalyse auf den Post des Nutzers durch und bestimmt, ob er negativ ist.

**Account-Level Prüfung:**
1. Prüft, ob der Nutzer von der Bluesky-Moderation unter irgendeiner Moderationskategorie markiert wurde.

**Post-Level Prüfung:**
1. Liest Bluesky Post Labels, darunter:
   - Selbst angehängte Labels.
   - Bluesky-Moderations-Labels.

#### Posts löschen
1. Finde die Bot-Antwort unter einem deiner Posts.
2. Antworte auf die Bot-Antwort mit "delete" und sie wird direkt gelöscht.

### Einstellungen
Du kannst sogar die Einstellungen der Bots konfigurieren! Das kannst du tun, indem du einfach einen der Befehle da unten per Direktnachricht an den Bot schreibst.

Der Bot prüft alle 5 Minuten, ob neue Befehle da sind. Du kannst bis zu 10 Befehle pro Überprüfung senden und sie werden genau in der Reihenfolge verarbeitet, in der sie gesendet wurden.

Um alle deine Einstellungen zu sehen:
1. Sende eine Direktnachricht mit diesem Befehl an den Bot:
    - `!settings`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Einstellungen synchronisieren
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Einstellungen des aktuellen Bots mit denen eines anderen Bots synchronisieren:** `!sync <@other_bot_handle>`
    - **Einstellungen aller anderen Bots mit dem aktuellen Bot synchronisieren:** `!sync <@current_bot_handle>`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    
    
#### Spitzname
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Spitznamen einstellen:** `!nickname <nickname>` (Dein Spitzname kann maximal 20 Zeichen lang sein)
    - **Spitznamen zurücksetzen:** `!nickname`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Post Chance
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Chance einstellen:** `!chance <chance>` (Muss eine Zahl zwischen 0 und 100 sein)
    - **Chance zurücksetzen:** `!chance`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern. 

#### Post Intervall
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Intervall festlegen:** `!interval <interval>` (Muss eine Zahl zwischen 60 und 3600 sein)
    - **Variablen Intervall festlegen:** `!interval <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 60 und 3600 sein)
    - **Intervall zurücksetzen:** `!interval`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Posts überspringen
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Intervall festlegen:** `!skip <interval>` (Muss eine Zahl zwischen 0 und 50 sein)
    - **Variablen Intervall festlegen:** `!skip <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 0 und 50 sein)
    - **Intervall zurücksetzen:** `!skip`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.     

#### Sprache
1. Sende eine Direktnachricht mit einem dieser Befehle an den Bot:
    - **Spracheinstellung festlegen:** `!language <language>` (z.b.: `!language de` or `!language english`).
    - **Spracheinstellung zurücksetzen:** `!language`
2. Warte auf die Antwort des Bots.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.

## Datenschutzrichtlinie

### Rahmen der Datenerfassung, Nutzung, Speicherung und Sicherheit
Der Bot sammelt und nutzt die folgenden Daten:

**Posts der Follower:**
- Der Inhalt und Metadaten der Posts, gespostet von Accounts, die dem Bot folgen.
- Informationen von gesammelten Posts werden nicht permanent gespeichert und 
werden nur temporär im Cache des Bots gespeichert.

 **Nutzer Metadaten**
- Nur öffentlich findbaren Informationen wie Nutzernamen und Profildetails.
- Nur die DID (Bluesky-Account-gebundene ID) wird gespeichert.

**Nutzer Einstellungen**
- Einstellungen, die vom Nutzer geändert wurden, z.B. Spitznamen.
- Diese Informationen werden gegen die DID des Nutzers gespeichert.

**Sicherheit und Nutzung**
- Keine Daten werden mit Dritten geteilt.
- Keine Daten werden von KI-Modellen genutzt.

### Löschen von Nutzerdaten
Um deine Daten vom Bot zu löschen, ist das mit den folgenden Wegen möglich:

**Automatischer Löschvorgang:**
1. Sende eine Direktnachricht mit diesem Befehl an den Bot:
  - **Einzelner Bot:** `!delete`
  - **Alle Bots:** `!delete all` 
2. Warte auf die Antwort des Bots.
   - Die Antwort des Bots kann bis zu 5 Minuten dauern.     
   
 **Manueller Löschvorgang**
 1. Kontaktiere Pikachannel über eine der folgenden:
    - Bluesky: [pikachannel.xyz](https://bsky.app/profile/pikachannel.xyz)
    - E-Mail:   pikachannel.dev@gmail.com  
 2. Warte auf die Bestätigung, dass deine Daten aus dem Speicher des Bots gelöscht wurden.

## Lizenz

Dieses GitHub-Repo ist Open Source und unter der MIT-Lizenz freigegeben.

Siehe [LICENSE](LICENSE) für mehr Informationen.
