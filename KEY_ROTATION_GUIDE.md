# API Key Rotation Guide - Swedavia Flight Information

## 🔄 Vad är Key Rotation?

Swedavia roterar API-nycklar var 6:e månad av säkerhetsskäl. Detta innebär att din nyckel kommer att upphöra att fungera enligt ett förutbestämt schema.

## 📅 Rotation Schema 2025-2030

| Datum | Nyckel som regenereras | Åtgärd |
|-------|------------------------|--------|
| **2025-04-09** | Primary key | Uppdatera primary key före detta datum |
| **2025-10-03** | Secondary key | Uppdatera secondary key före detta datum |
| **2026-04-08** | Primary key | Uppdatera primary key före detta datum |
| **2026-10-02** | Secondary key | Uppdatera secondary key före detta datum |
| **2027-03-31** | Primary key | Uppdatera primary key före detta datum |
| **2027-10-01** | Secondary key | Uppdatera secondary key före detta datum |
| **2028-04-05** | Primary key | Uppdatera primary key före detta datum |
| **2028-10-06** | Secondary key | Uppdatera secondary key före detta datum |
| **2029-04-04** | Primary key | Uppdatera primary key före detta datum |
| **2029-10-05** | Secondary key | Uppdatera secondary key före detta datum |
| **2030-04-03** | Primary key | Uppdatera primary key före detta datum |
| **2030-10-04** | Secondary key | Uppdatera secondary key före detta datum |

**Mönster:** Primary key roteras i april, Secondary key roteras i oktober.

## 🛡️ Automatisk Failover (Rekommenderat!)

### Med både Primary och Secondary key

**Integrationen har automatisk failover!** Om du konfigurerar både primary och secondary keys:

1. ✅ Integrationen använder primary key som standard
2. ✅ Vid HTTP 401 (invalid key), växlar den automatiskt till secondary key
3. ✅ Om secondary också failar, får du ett felmeddelande
4. ✅ Efter failover fortsätter integrationen använda secondary key

**Detta ger dig skydd vid key rotation:**
- Primary key upphör → Integrationen växlar automatiskt till secondary
- Du har tid att uppdatera primary key i lugn och ro
- Ingen downtime!

### Exempel scenario (April 2026)

```
2026-04-08: Primary key regenereras av Swedavia
             ↓
Din gamla primary key slutar fungera
             ↓
Integrationen får HTTP 401
             ↓
Automatisk failover till secondary key
             ↓
Integrationen fortsätter fungera! ✅
             ↓
Du uppdaterar primary key när du har tid
             ↓
Före 2026-10-02: Uppdatera secondary key
```

## 📝 Konfigurera Både Nycklar

### Vid Installation

```
┌─────────────────────────────────────────────┐
│  Konfigurera Swedavia Flyginformation      │
├─────────────────────────────────────────────┤
│                                             │
│  Primary API Key: [abc123...]  ← Obligatorisk│
│                                             │
│  Secondary API Key: [def456...] ← Valfritt │
│  (Rekommenderat för automatisk failover)   │
│                                             │
│  Flygplats: [ARN ▼]                        │
│  ...                                        │
└─────────────────────────────────────────────┘
```

### Hur man hittar båda nycklarna

1. Logga in på https://apideveloper.swedavia.se/
2. Gå till **Profile** → **Subscriptions**
3. Välj din FlightInfo-subscription
4. **Primary key**: Visa och kopiera
5. **Secondary key**: Visa och kopiera (under primary key)

## 🔧 Uppdatera Nycklar

### Metod 1: Ta bort och lägg till igen (Enklast)

1. **Hämta nya nycklar** från developer portalen
2. **Ta bort** integrationen i Home Assistant
   - Inställningar → Enheter & tjänster
   - Klicka på tre prickar → Ta bort
3. **Lägg till** igen med nya nycklar
   - Inställningar → Enheter & tjänster → Lägg till integration
   - Sök "Swedavia"
   - Ange nya primary + secondary keys

**OBS:** Din historiska data bevaras, men du måste konfigurera om flygplats etc.

### Metod 2: Redigera configuration (Avancerat)

Om du är bekväm med Home Assistant's konfigurationsfiler:

1. Stoppa Home Assistant
2. Redigera `.storage/core.config_entries`
3. Hitta din Swedavia-entry
4. Uppdatera `api_key` och/eller `api_key_secondary`
5. Starta Home Assistant

**VARNING:** Felaktig redigering kan förstöra konfigurationen!

## ⚠️ Vad händer om du inte uppdaterar?

### Endast Primary Key konfigurerad

```
Rotation → Primary key upphör → HTTP 401 → Integration slutar fungera ❌
```

**Du får felmeddelande:**
```
"API authentication failed. Invalid subscription key. 
Please update your API key from https://apideveloper.swedavia.se/"
```

### Både Primary och Secondary konfigurerad

```
Rotation → Primary key upphör → HTTP 401 → Automatisk failover till Secondary ✅
```

**Du får varning i loggen:**
```
WARNING: Primary API key failed (401), trying secondary key
```

**Men integrationen fortsätter fungera!** 🎉

## 📧 Notifikationer från Swedavia

Swedavia skickar e-post innan key rotation:
- Vanligtvis 1-2 veckor före datum
- Påminnelse om vilket datum som påverkas
- Information om vilken nyckel (primary eller secondary) som roteras

**Tips:** Lägg till en påminnelse i din kalender några dagar före varje datum!

## 🔍 Kontrollera Vilken Nyckel Som Används

### Kontrollera i Developer Portal

1. Logga in på https://apideveloper.swedavia.se/
2. Profile → Subscriptions → FlightInfo
3. Primary och Secondary keys visas (maskerade)
4. Klicka "Show" för att se hela nyckeln
5. Jämför med vad du har konfigurerat

### Kontrollera i Home Assistant Loggen

```
DEBUG: Requesting https://api.swedavia.se/flightinfo/v2/ARN/arrivals/2026-01-16
WARNING: Primary API key failed (401), trying secondary key
```

Om du ser "trying secondary key" betyder det att:
- Primary key har upphört
- Integrationen har växlat till secondary
- **Du bör uppdatera primary key!**

## 🎯 Best Practices

### ✅ Rekommenderat Setup

1. **Konfigurera både primary och secondary keys**
   - Ger automatisk failover
   - Minimerar downtime
   - Mer robust lösning

2. **Sätt påminnelser i kalendern**
   - 1 vecka före varje rotationsdatum
   - Uppdatera nycklar proaktivt

3. **Kontrollera regelbundet**
   - Logga in på developer portalen var 6:e månad
   - Verifiera att keys är aktuella

4. **Testa efter uppdatering**
   - Kontrollera att sensorer uppdateras
   - Verifiera i Home Assistant-loggen

### ❌ Undvik

1. **Endast en nyckel konfigurerad**
   - Risk för downtime vid rotation
   - Ingen automatisk failover

2. **Glömma att uppdatera**
   - Sätt kalenderpåminnelser!
   - Prenumerera på Swedavias e-post

3. **Använda gamla nycklar**
   - Keys har max 12 månaders livstid
   - Gamla keys slutar fungera

## 📊 Key Lifecycle

```
Primary Key Lifecycle (12 månader):

Månad 0: Ny primary key genereras (April)
Månad 6: Secondary key genereras (Oktober) 
         ↓ Primary key är fortfarande giltig
Månad 12: Primary key regenereras (April)
          ↓ Gammal primary key UPPHÖR
          ↓ Ny primary key börjar gälla
```

## 🆘 Felsökning

### "Access denied due to invalid subscription key"

**Orsak:** Din API-nyckel har upphört eller är felaktig.

**Lösning:**
1. Logga in på https://apideveloper.swedavia.se/
2. Kontrollera dina subscription keys
3. Uppdatera integrationen med nya keys

### Integrationen växlar ofta mellan keys

**Orsak:** En av dina nycklar är felaktig eller har upphört.

**Lösning:**
1. Kontrollera i Home Assistant-loggen vilken key som failar
2. Uppdatera den felaktiga nyckeln
3. Om båda failar, hämta nya keys från portalen

### Kan inte logga in på developer portalen

**Lösning:**
1. Använd "Forgot password" för att återställa
2. Kontakta Swedavia: api@swedavia.se

## 💡 Tips: Automation för Påminnelser

Skapa en automation i Home Assistant som påminner dig:

```yaml
automation:
  - alias: "Påminnelse - Swedavia Key Rotation"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: template
        value_template: >
          {% set month = now().month %}
          {% set day = now().day %}
          {# April rotation (primary) #}
          {{ (month == 4 and day >= 1 and day <= 8) or
          {# Oktober rotation (secondary) #}
             (month == 10 and day >= 1 and day <= 4) }}
    action:
      - service: persistent_notification.create
        data:
          title: "Swedavia API Key Rotation"
          message: >
            {% if now().month == 4 %}
            Primary API key roteras snart! Uppdatera din primary key från https://apideveloper.swedavia.se/
            {% else %}
            Secondary API key roteras snart! Uppdatera din secondary key från https://apideveloper.swedavia.se/
            {% endif %}
```

## 📚 Mer Information

- **Developer Portal:** https://apideveloper.swedavia.se/
- **Kontakt:** api@swedavia.se
- **Key Rotation Schedule:** Se PDF `keyrotation-2025_2030.pdf`
- **Integration Issues:** https://github.com/frodr1k/Swedavia_info/issues

---

**Uppdaterad:** 2026-01-16  
**Gäller:** 2025-2030  
**Status:** ✅ Automatisk failover implementerad
