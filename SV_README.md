# Bluesky-svarsbotar
<p align="left">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=flat-square" alt="English"></a>
</p>

## Översikt
Detta GitHub repo innehåller all kod för:
- Whimsy Miku Bot (whimsy.pikachannel.xyz)
- Evil Teto Bot (evil.pikachannel.xyz)
---
## Innehållsförteckning
- [Översikt](#översikt)
- [Botarna!](#botarna)
  - [Nuvarande funktioner](#nuvarande-funktioner)
  - [Så här använder du tjänsten](#så-här-använder-du-tjänsten)
  - [System för innehållsfiltrering](#system-för-innehållsfiltrering)
    - [Filtersystem](#filtersystem)
    - [Ta bort inlägg](#ta-bort-inlägg)
  - [Inställningar](#inställningar)
    - [Synkronisera inställningar](#synkronisera-inställningar)
    - [Anpassat smeknamn](#anpassat-smeknamn)
    - [Sannolikhet för inlägg](#sannolikhet-för-inlägg)
    - [Intervall för inlägg](#intervall-för-inlägg)
    - [Hoppa över inlägg](#hoppa-över-inlägg)
    - [Språk](#språk)
- [Integritetspolicy](#integritetspolicy)
  - [Datainsamling, användning, lagring och säkerhet](#datainsamling-användning-lagring-och-säkerhet)
  - [Borttagning av data](#borttagning-av-data)
- [Licens](#licens)

## Botarna!
Whimsy Miku - *som har glimten i ögat* - svarar på dina inlägg med positiva meddelanden!

Evil Teto - som namnet förhoppningsvis förklarar - svarar på dina inlägg med elaka meddelanden i en humoristisk ton!

### Nuvarande funktioner
1. **Slumpmässigt valda förinställda meddelanden**, inklusive:
   - Stöd för flera språk
   - Meddelanden som inkluderar användarens namn.
2. **System för innehållsfiltrering**, inklusive:
   - Ett filter för inlägg
   - Möjlighet för användare att radera svar på sina inlägg genom att svara med ordet "delete".
3. **Anpassade smeknamn**: Användare kan ange ett eget smeknamn istället för att använda sitt visningsnamn på Bluesky.
4. **Svarschans**: Användare kan justera sannolikheten för att ett svar skapas på deras inlägg.
5. **Svarsintervall**: Användare kan ändra tidsintervallet mellan svar på sina inlägg. Alla svar har en minsta väntetid (nedkylningsperiod) på 60 sekunder.
6. **Hoppa över inlägg**: Användare kan ställa in hur många inlägg som ska passera mellan de tillfällen då boten kan svara på deras inlägg.
7. **Dagens ord**: Evil Teto publicerar ett slumpmässigt ord varje dag.
8. **Språk Val**: Användare kan sätta botten's svar-språk, vilket för nuvarande inkluderar (men är inte begränsat till) förljande:
   - Engelska (EN)
   - Svenska (SV)

### Så här använder du tjänsten
1. Följ boten på Bluesky
   - Om du slutar följa eller blockerar boten kan det ta upp till 5 minuter innan detta registreras och boten slutar svara.

### System för innehållsfiltrering

#### Filtersystem
Systemet hoppar över svar om något av följande villkor är uppfyllt:

**Kontroller av inläggets innehåll:**
1. Identifierar om ett inlägg innehåller fördefinierade nyckelord.
2. Identifierar om ett inlägg innehåller en länk eller inbäddat innehåll.
3. Utför en sentimentanalys av användarens inlägg för att avgöra om det är negativt, neutralt eller positivt (koden för detta ingår för närvarande inte i detta arkiv).

**Kontroller på kontonivå:**
1. Kontrollerar om användarens konto har flaggats av Blueskys modereringsteam.

**Kontroller på inläggsnivå:**
1. Identifierar etiketter (labels) på Bluesky-inlägg, inklusive:
   - Etiketter som användaren själv har lagt till.
   - Etiketter från Blueskys moderering.

#### Ta bort inlägg
1. Hitta ett svar som skrivits under ett av dina inlägg.
2. Svara på det med ordet "delete", så tas det bort omedelbart.

### Inställningar
Du kan justera inställningarna för botarna! Detta görs genom att skicka rätt kommando i ett direktmeddelande (DM) till boten; kommandona finns listade nedan.
För att se dina nuvarande inställningar:
1. Skicka ett direktmeddelande till boten med följande kommando:
   - `!settings`
2. Vänta på att boten svarar **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.

#### Synkronisera inställningar
1. Skicka ett direktmeddelande till boten med något av följande kommandon:
   - **Synkronisera den aktuella botens inställningar med en annan bot:** `!sync <@annan_bot>`
   - **Synkronisera alla andra botars inställningar med den aktuella boten:** `!sync <@nuvarande_bot>`
2. Vänta på att boten svarar **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.


#### Anpassat smeknamn
1. Skicka ett direktmeddelande till boten enligt följande format:
   - **Ange smeknamn:** `!nickname <smeknamn>` (ditt smeknamn får vara högst 20 tecken långt)
   - **Återställ smeknamn:** `!nickname`
2. Vänta på svar från boten **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.

#### Sannolikhet för inlägg
1. Skicka ett direktmeddelande till boten enligt följande format:
   - **Ange sannolikhet:** `!chance <sannolikhet>` (måste vara ett tal mellan 0 och 100)
   - **Återställ sannolikhet:** `!chance`
2. Vänta på svar från boten **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.

#### Intervall för inlägg
1. Skicka ett direktmeddelande till boten enligt följande format:
   - **Ange fast intervall:** `!interval <intervall>` (måste vara ett tal mellan 60 och 3600)
   - **Ange variabelt intervall:** `!interval <lägre_gräns-övre_gräns>` (båda talen måste vara mellan 60 och 3600)
   - **Återställ intervall:** `!interval`
2. Vänta på svar från boten **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.
   - 
#### Hoppa över inlägg
1. Skicka ett direktmeddelande till boten enligt följande format:
   - **Ange fast intervall:** `!skip <intervall>` (måste vara ett heltal mellan 0 och 50)
   - **Ange variabelt intervall:** `!skip <lägre_gräns-övre_gräns>` (båda heltalen måste vara mellan 0 och 50)
   - **Återställ intervall:** `!skip`
2. Vänta på svar från boten **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.

#### Språk
1. Skicka ett direkt medelande till botten i förljande format:
   - **Sätt Språket:** `!language <language>` (till exempel, `!language sv` eller `!language engelska`).
   - **Återställ Språket** `!language`
2. Vänta tills botten svarar **innan** du skickar ett nytt medelande.
   - Svarstid kan ta up till ett par till 5 minuter.


## Integritetspolicy

### Datainsamling, användning, lagring och säkerhet
Botarna samlar in och använder följande data:

**Inlägg från följare:**
   - Innehåll och metadata för inlägg från konton som följer boten. 
   - Information om inlägg **sparas aldrig permanent** utan lagras endast tillfälligt i botens cacheminne.

**Användarmetadata:**
   - Offentligt tillgänglig information, såsom användarnamn och profiluppgifter. 
   - Den enda information som sparas är användarens DID (en typ av användar-ID på Bluesky).

**Användarinställningar:**
   - Inställningar som användaren själv har konfigurerat, till exempel smeknamn. 
   - Denna information lagras **kopplad till användarens DID**.

**Säkerhet och användning:**
   - Ingen data delas med tredje part.
   - Ingen data används av en AI-modell.

### Borttagning av data
Om du vill att dina uppgifter ska tas bort från boten finns det två alternativ:

**Automatisk borttagning:**
1. Skicka ett direktmeddelande till boten med följande innehåll:
   - `!delete`
2. Vänta på att boten svarar **innan** du skickar ett nytt meddelande. 
   - Det kan ta upp till 5 minuter att få svar.

**Manuell borttagning:**
1. Kontakta Pikachannel via:
   - Bluesky: [pikachannel.xyz](https://bsky.app/profile/pikachannel.xyz)
   - E-post: pikachannel.dev@gmail.com
2. Invänta bekräftelse på att dina uppgifter har tagits bort från botens lagring.

## Licens
Detta arkiv är öppen källkod och publiceras under MIT-licensen.

Se [LICENSE](https://github.com/Pikachannel/bluesky-bots/blob/main/LICENSE) för mer information.
