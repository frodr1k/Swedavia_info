# API-nyckel uppdatering - Swedavia Flight Information

## ⚠️ VIKTIGT: API-nyckel krävs nu!

Integrationen har uppdaterats för att följa Swedavias officiella API-krav. Alla API-anrop måste nu autentiseras med en **Subscription Key**.

## Vad har ändrats?

### Före (v1.0.0 original)
- ❌ Ingen autentisering
- ❌ Fungerade troligen inte mot det riktiga API:t

### Efter (v1.0.0 uppdaterad)
- ✅ API Subscription Key krävs
- ✅ Korrekt autentisering via `Ocp-Apim-Subscription-Key` header
- ✅ Följer Swedavias officiella API-dokumentation

## Hur får jag en API-nyckel?

### Steg 1: Registrera dig (gratis!)
1. Gå till https://apideveloper.swedavia.se/
2. Klicka på **"Sign up"**
3. Fyll i e-post och lösenord
4. Bekräfta din e-postadress

### Steg 2: Prenumerera på FlightInfo (gratis!)
1. Logga in på portalen
2. Navigera till **"Products"**
3. Välj **"FlightInfo"**
4. Klicka på **"Subscribe"**
5. Du får omedelbar åtkomst (ingen godkännande-process)

### Steg 3: Kopiera din nyckel
1. Gå till **"Profile"** → **"Subscriptions"**
2. Välj din FlightInfo-subscription
3. Kopiera **Primary key** (eller Secondary key)

**Nyckeln ser ut så här:** `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6` (32 tecken hex)

## Uppdaterade filer

### Integration kod
- `const.py`: Lagt till `CONF_API_KEY`
- `api.py`: API-klient accepterar nu `api_key` parameter och skickar `Ocp-Apim-Subscription-Key` header
- `__init__.py`: Läser API-nyckel från config entry
- `config_flow.py`: Nytt obligatoriskt fält för API-nyckel

### Översättningar
- `translations/sv.json`: Svenska beskrivningar för API-nyckel
- `translations/en.json`: Engelska beskrivningar för API-nyckel
- `strings.json`: Bas-översättningar

### Dokumentation
- `README.md`: 
  - Ny sektion "Förberedelser - Skaffa API-nyckel"
  - Uppdaterad konfigurationsguide
  - API Information med länk till developer portal
- `QUICKSTART.md`:
  - Stor ny sektion "🔑 Skaffa API-nyckel"
  - Steg-för-steg guide
  - Uppdaterad felsökning
- `info.md`: Varning om API-nyckel krävs

### Tekniska detaljer
- API-dokumentation från Swedavia (`General_API_information.pdf`)
- FlightInfo-specifik dokumentation (`Using_the_FlightInfo_API.pdf`)
- Key rotation information (`keyrotation-2025_2030.pdf`)

## Ny konfigurationsprocess

```
┌─────────────────────────────────────────────┐
│  Konfigurera Swedavia Flyginformation      │
├─────────────────────────────────────────────┤
│                                             │
│  API Subscription Key: [____________]      │
│  (Från https://apideveloper.swedavia.se)   │
│                                             │
│  Flygplats: [ARN - Stockholm Arlanda ▼]   │
│                                             │
│  Typ av flyg: [Både ankomster och avgångar▼]│
│                                             │
│  Timmar bakåt: [2]                         │
│                                             │
│  Timmar framåt: [24]                       │
│                                             │
│  [Avbryt]              [Skicka]            │
└─────────────────────────────────────────────┘
```

## Felmeddelanden

### "Cannot connect to Swedavia API"
- Kontrollera din API-nyckel
- Verifiera internetanslutning
- Kontrollera att du har en aktiv FlightInfo-subscription

### "Invalid API key"
- Nyckeln är felaktig eller har upphört
- Kopiera nyckeln igen från developer portalen
- Kontrollera att du prenumererar på FlightInfo-produkten

## Kostnader

**100% GRATIS!** 🎉

- Registrering: Gratis
- FlightInfo API-produkt: Gratis
- Inga begränsningar för normal användning
- Inga kreditkort behövs

## Premium-produkter

Swedavia erbjuder också premium-produkter med:
- Högre rate limits
- Mer detaljerad data
- Prioriterad support

Kontakta api@swedavia.se för information om premium-produkter.

## Support

### Developer Portal
- Portal: https://apideveloper.swedavia.se/
- API-dokumentation: I portalen under varje produkt
- Kontakt: api@swedavia.se

### Integration Support
- GitHub Issues: https://github.com/frodr1k/Swedavia_info/issues
- GitHub Discussions: https://github.com/frodr1k/Swedavia_info/discussions

## Key Rotation

Swedavia roterar API-nycklar enligt schema (se `keyrotation-2025_2030.pdf`). Du får meddelande via e-post när det är dags att byta nyckel.

**När du får nytt:** 
1. Kopiera den nya nyckeln från portalen
2. Ta bort integrationen i Home Assistant
3. Lägg till igen med nya nyckeln

## Teknisk information

### HTTP Headers
```http
GET /flightinfo/v2/ARN/arrivals/2026-01-16
Accept: application/json
Ocp-Apim-Subscription-Key: [din-nyckel]
User-Agent: HomeAssistant-SwedaviaFlights/1.0
```

### Autentiseringsflöde
1. Användaren anger API-nyckel i config flow
2. Integration validerar nyckel genom test-anrop till API
3. Nyckel sparas i config entry (krypterad av Home Assistant)
4. Varje API-anrop inkluderar `Ocp-Apim-Subscription-Key` header
5. Swedavias API verifierar nyckeln och returnerar data

---

**Uppdaterad:** 2026-01-16  
**Version:** 1.0.0 (med API-nyckel stöd)  
**Status:** ✅ Produktionsklar
