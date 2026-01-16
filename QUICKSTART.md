# Snabbstart - Swedavia Flight Information

## 🚀 Vad har skapats?

En komplett Home Assistant integration för Swedavias flyginformation med:

- **12 svenska flygplatser** (ARN, GOT, MMX, BMA, LLA, UME, VBY, KRN, RNB, VST, ORB, NYO)
- **Ankomster** med bagageinformation (band, första/sista väska)
- **Avgångar** med gate-info (öppning/stängning) och incheckning
- **Code-share flyg** - Alla flightnummer för samma flygning
- **Realtidsdata** - Uppdateras var 5:e minut från Swedavias API

## 📁 Projektstruktur

```
Swedavia_info/
├── custom_components/swedavia_flights/    # Integration
│   ├── __init__.py                       # Setup och plattformar
│   ├── api.py                            # Swedavia API-klient
│   ├── config_flow.py                    # GUI-konfiguration
│   ├── const.py                          # Konstanter och konfiguration
│   ├── coordinator.py                    # DataUpdateCoordinator
│   ├── sensor.py                         # Sensor-entiteter
│   ├── manifest.json                     # Integration metadata
│   ├── strings.json                      # Översättningsstruktur
│   └── translations/                     # Översättningar
│       ├── en.json                       # Engelska
│       └── sv.json                       # Svenska
├── .github/workflows/                    # GitHub Actions
│   └── validate.yaml                     # HACS + Hassfest validering
├── README.md                             # Fullständig dokumentation
├── LICENSE                               # MIT License
├── hacs.json                             # HACS-konfiguration
├── info.md                               # HACS-beskrivning
├── RELEASE_NOTES_v1.0.0.md              # Release notes
├── DEVELOPMENT_STATUS.md                 # Utvecklingsstatus
└── .gitignore                            # Git ignore
```

## ⚡ Nästa steg - GitHub

### 1. Skapa GitHub Repository

1. Gå till https://github.com/new
2. Repository name: `Swedavia_info`
3. Description: `Home Assistant integration for Swedavia flight information`
4. Public
5. Skapa **UTAN** README, license, eller .gitignore (vi har redan dessa)

### 2. Pusha till GitHub

```bash
cd c:\git\Swedavia_info
git remote add origin https://github.com/frodr1k/Swedavia_info.git
git branch -M main
git push -u origin main
```

### 3. Skapa Release v1.0.0

1. Gå till repository på GitHub
2. Klicka på "Releases" → "Create a new release"
3. **Tag**: `v1.0.0`
4. **Title**: `v1.0.0 - Initial Release`
5. **Description**: Kopiera innehållet från `RELEASE_NOTES_v1.0.0.md`
6. Markera "Set as the latest release"
7. Klicka "Publish release"

## 🏠 Installation i Home Assistant

### Metod 1: HACS (Rekommenderat)

1. **Lägg till custom repository**:
   - HACS → Integrations → ⋮ (meny) → Custom repositories
   - URL: `https://github.com/frodr1k/Swedavia_info`
   - Category: Integration
   - Klicka "Add"

2. **Installera**:
   - Sök efter "Swedavia Flight Information"
   - Klicka "Download"
   - Starta om Home Assistant

3. **Konfigurera**:
   - Inställningar → Enheter & tjänster → Lägg till integration
   - Sök "Swedavia"
   - Välj flygplats och inställningar

### Metod 2: Manuell installation

1. **Kopiera filer**:
   ```bash
   # Kopiera hela custom_components/swedavia_flights mappen till:
   <home-assistant-config>/custom_components/swedavia_flights/
   ```

2. **Starta om** Home Assistant

3. **Konfigurera** som ovan

## 🎯 Användning

### Exempel 1: Ankomster Lovelace Card

```yaml
type: markdown
title: 🛬 Ankomster Arlanda
content: |
  {% set flights = state_attr('sensor.stockholm_arlanda_ankomster', 'flights') %}
  {% for flight in flights[:5] %}
  **{{ flight.flight_id }}** från {{ flight.origin }}
  ⏰ {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
  💼 Bagage: Band {{ flight.baggage_claim }}
  📍 Gate {{ flight.gate }} | Status: {{ flight.status }}
  ---
  {% endfor %}
```

### Exempel 2: Avgångar med Gate-info

```yaml
type: markdown
title: 🛫 Avgångar Arlanda  
content: |
  {% set flights = state_attr('sensor.stockholm_arlanda_avgangar', 'flights') %}
  {% for flight in flights[:5] %}
  **{{ flight.flight_id }}** till {{ flight.destination }}
  ⏰ {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
  🚪 Gate {{ flight.gate }} - {{ flight.gate_action }}
  ✈️ Incheckning: {{ flight.check_in_status }}
  ---
  {% endfor %}
```

### Exempel 3: Notifiering vid försening

```yaml
automation:
  - alias: "Notifiera vid försenat flyg"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_avgangar
    condition:
      - condition: template
        value_template: >
          {% set flights = state_attr(trigger.entity_id, 'flights') %}
          {{ flights | selectattr('status', 'search', 'Försenat') | list | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          message: "Försening upptäckt på Arlanda!"
```

## 🔧 Konfiguration

### Konfigureringsalternativ

**Vid installation:**
- **Flygplats**: Välj från 12 svenska flygplatser
- **Flygtyp**: Ankomster, Avgångar eller Både
- **Timmar bakåt**: Hur långt tillbaka i tiden (standard: 2h)
- **Timmar framåt**: Hur långt fram i tiden (standard: 24h)

**Justera senare:**
- Inställningar → Enheter & tjänster
- Välj integrationen → Konfigurera
- Ändra timmar bakåt/framåt

## 📊 Sensor-attribut

### Ankomster (`sensor.{flygplats}_ankomster`)
- `flights`: Lista med alla flyg med:
  - `flight_id`, `airline`, `origin`
  - `scheduled_time`, `estimated_time`, `actual_time`
  - `status`, `terminal`, `gate`
  - `baggage_claim` - Band-nummer
  - `first_bag`, `last_bag` - Väsketider
  - `code_share_flights` - Alla flightnummer
  - `remarks` - Anmärkningar

### Avgångar (`sensor.{flygplats}_avgangar`)
- `flights`: Lista med alla flyg med:
  - `flight_id`, `airline`, `destination`
  - `scheduled_time`, `estimated_time`, `actual_time`
  - `status`, `terminal`, `gate`
  - `gate_action`, `gate_open`, `gate_close`
  - `check_in_status`, `check_in_from`, `check_in_to`
  - `code_share_flights`
  - `remarks`

## 🐛 Felsökning

### Integrationen syns inte i Home Assistant
- Kontrollera att mappen ligger i rätt plats: `config/custom_components/swedavia_flights/`
- Starta om Home Assistant
- Kolla loggen för fel: Inställningar → System → Loggar

### API-fel
- Kontrollera internetanslutning
- Swedavias API kan vara tillfälligt nere
- Integrationen har automatisk retry och felhantering

### Inga flyg visas
- Kontrollera tidsfönstret (timmar bakåt/framåt)
- Det kanske inte finns några flyg inom tidsfönstret
- Kolla sensor-attribut för att se rådata

## 📈 Prestandainformation

- **Uppdateringsfrekvens**: Var 5:e minut
- **API rate limiting**: Minimum 1 sekund mellan requests
- **Max flyg per sensor**: 50 (API returnerar vanligtvis färre)
- **Minnesanvändning**: Minimal, endast aktuella flyg cachas

## 🤝 Support

- **Buggrapporter**: [GitHub Issues](https://github.com/frodr1k/Swedavia_info/issues)
- **Funktionsförslag**: [GitHub Discussions](https://github.com/frodr1k/Swedavia_info/discussions)
- **Pull requests**: Välkomna!

## 📝 License

MIT License - Fri att använda och modifiera!

---

**Lycka till med din nya Swedavia-integration! ✈️**
