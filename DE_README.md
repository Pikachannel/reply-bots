# head

Paragraph.

## Second Level Heading

Paragraph.

- bullet
+ other bullet
* another bullet
    * child bullet

1. ordered
2. next ordered

### Third Level Heading

Some *italic* and **bold** text and `inline code`.

An empty line starts a new paragraph.

Use two spaces at the end  
to force a line break.

A horizontal ruler follows:

---

Add links inline like [this link to the Qt homepage](https://www.qt.io),

    Add code blocks with
    four spaces at the front.

> A blockquote
> starts with >
>
> and has the same paragraph rules as normal text.

### Nutzung
1. Folge dem Bot auf Bluesky
    - Wenn du den Bot blockierst oder entfolgst dann könnte es bis zu 5 Minuten dauern bis der Bot aufhört auf deine Posts zu antworten.

### Content Filterungs System

#### Filter System
Das System überspringt Posts wenn einer der folgenden Bedingungen erfüllt werden:

**Post Inhalts Check**
1. Erkennt ob der Post einer der vordefiniert Keywords enthält
2. Erkennt ob der post einen Link oder ein Embed enthält
3. Führt eine Sentiment analyse auf den Post des Nutzers durch und bestimmt ob es negativ, neutral oder positiv ist (Der Code daführ ist gerade nicht in diesem Repo).

#### Posts löschen
1. Finde die Antwort unter einem deiner Posts.
2. Antworte auf dien Antwort mit "delete" und sie wird direkt gelöscht

### Einstellungen
Du kannst sogar die Einstellungen der Bots konfigurieren! Das kannst du tun indem du einfach einer der Befehle da unten in die direkt

Nachrichten des Bots schreibst.

Um alle deine Einstellungen zu sehen:
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - `settings`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Einstellungs Synchonisierung
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Einstellungen des geradigen Bots mit den eines anderen Bots synchonisieren:** `!sync <@other_bot_handle>`
    - **Einstellungen aller anderen Bots mit den des geradigen Bots synchonisieren:** `!sync <@current_bot_handle>`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    
    

#### Spitznamen
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Spitznamen einstellen:** `!nickname <nickname>` (Dein Spitzname kann Maximal 20 Charactere lang sein)
    - **Spitznamen zurücksetzen:** ´!nickname`
2. Warte auf die Antwort des Bots.
- Sende während dieser Zeit keine neuen Nachrichten.
- Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Post Chance
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Chance einstellen:** `!chance <chance>` (Muss eine Zahl zwischen 0 und 100 sein)
    - **Chance zurücksetzen:** `!chance`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern. 


#### Post Intervall
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Um einen Statischen Intervall einzustellen:** `!interval <interval>` (Muss eine Zahl zwischen 60 und 3600 sein)
    - **Um einen variablen Intervall einzustellen:** `!interval <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 60 und 3600 sein)
    - **Um den Intervall zurückzusetzen** `!interval`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Posts überspringen
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Um einen Statischen Intervall einzustellen:** `!skip <interval>` (Muss eine Zahl zwischen 0 und 50 sein)
    - **Um einen variablen Intervall einzustellen:** `!skip <lower_bound-upper_bound>` (Beide Zahlen müssen zwischen 0 und 50 sein)
    - **Um den Intervall zurückzusetzen** `!skip`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.    

#### Sprache
1. Sende eine direkt Nachricht an den Bot in diesem Foramt:
    - **Um die Spracheinstellung einzustellen:** `!language <language>` (z.b.: `!language de`
  or `!language english`).
    - **Um die Spracheinstellung zurückzusetzen:** `!language`
2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.


## Datenschutzrichtlinie

### Rahmen der Datenerfassung, nutzung, das Speichern und Sicherheit
Der Bot sammelt und benutzt die folgenden Daten:

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



### Löschung der Daten
Wenn du möchstest das deine Daten von dem Bot gelöscht werden hast du 2 Optionen:

 **Der automatische Löschvogang:**
 1. Sende eine direkt Nachricht zu dem Bot in dem folgenden Format:
    - `!delete` 
 2. Warte auf die Antwort des Bots.
    - Sende während dieser Zeit keine neuen Nachrichten.
    - Die Antwort des Bots kann bis zu 5 Minuten dauern.
    
 **Der manuelle Löschvorgang**
 1. Kontaktiere Pikachannel mit einer der Folgenden:
    - Bluesky: [pikachannel.xyz](https://bsky.app/profile/pikachannel.xyz)
    - E-Mail:   pikachannel.dev@gmail.com  
 2. Warte auf die Bestätigung das deine Daten von dem Speicher des Bots gelöscht wurden.

## Lizenz

Dieses Github Repo ist Open Source und unter der MIT Lizenz freigegeben.

Für mehr Informationen schauen sie die [LIZENZ](https://github.com/Pikachannel/bluesky-bots/blob/main/LICENSE) an.