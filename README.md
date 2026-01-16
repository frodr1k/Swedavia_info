# Swedavia Flight Information

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/frodr1k/Swedavia_info.svg)](https://github.com/frodr1k/Swedavia_info/releases)
[![License](https://img.shields.io/github/license/frodr1k/Swedavia_info.svg)](LICENSE)

En Home Assistant integration för att visa flyginformation från svenska flygplatser via Swedavias officiella API.

## Funktioner

- 🛬 **Ankomster** - Visa ankommande flyg med bagage-information
- 🛫 **Avgångar** - Visa avgående flyg med gate och incheckning
- 🏢 **Alla svenska Swedavia-flygplatser** - ARN, GOT, MMX, BMA, LLA, UME, VBY, KRN, RNB, VST, ORB, NYO
- ⏰ **Flexibelt tidsfönster** - Välj hur många timmar framåt/bakåt du vill se flyg
- 🔄 **Automatisk uppdatering** - Data uppdateras var 5:e minut
- 🎫 **Code-share information** - Visa alla flightnummer för samma flygning
- 💼 **Bagageinformation** - Band-nummer och tider för första/sista bagage
- 🚪 **Gate-information** - Terminal, gate, öppnings- och stängningstider
- ✈️ **Detaljerad flyginformation** - Status, förseningar, anmärkningar

## Installation

### Förberedelser - Skaffa API-nyckel

**Swedavias API kräver en gratis API-nyckel (Subscription Key):**

1. Gå till Swedavias developer portal: https://apideveloper.swedavia.se/
2. Klicka på **"Sign up"** och skapa ett gratis konto
3. Bekräfta din e-postadress (kolla spam-mappen)
4. Logga in på portalen
5. Gå till **"Products"** → **"FlightInfo"**
6. Klicka på **"Subscribe"** (gratis, direkt åtkomst)
7. Gå till **"Profile"** → **"Subscriptions"**
8. Kopiera din **Primary key** eller **Secondary key**

**Nyckeln ser ut ungefär så här:** `abc123def456ghi789jkl012mno345pq`

### HACS (Rekommenderat)

1. Lägg till detta repository som en custom repository i HACS:
   - Gå till HACS → Integrations
   - Klicka på menyn (tre prickar) → Custom repositories
   - Lägg till: `https://github.com/frodr1k/Swedavia_info`
   - Kategori: Integration

2. Installera "Swedavia Flight Information" från HACS

3. Starta om Home Assistant

### Manuell installation

1. Kopiera mappen `custom_components/swedavia_flights` till din Home Assistant `config/custom_components` katalog
2. Starta om Home Assistant

## Konfiguration

1. Gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **Lägg till integration**
3. Sök efter "Swedavia Flight Information"
4. Fyll i uppgifterna:
   - **API Subscription Key**: Din nyckel från developer portalen
   - **Flygplats**: Välj vilken svensk flygplats du vill övervaka
   - **Typ av flyg**: Ankomster, Avgångar eller Både
   - **Timmar bakåt**: Hur många timmar bakåt i tiden (standard: 2)
   - **Timmar framåt**: Hur många timmar framåt i tiden (standard: 24)

### Var hittar jag min API-nyckel?

1. Logga in på https://apideveloper.swedavia.se/
2. Gå till **Profile** → **Subscriptions**
3. Välj din FlightInfo-subscription
4. Kopiera **Primary key** (eller Secondary key)

## Sensorer

Integrationen skapar följande sensorer:

### Ankomster Sensor
- **State**: Antal ankommande flyg
- **Attributes**:
  - `flights`: Lista med alla flyg inkl:
    - Flightnummer och code-share
    - Flygbolag (namn, IATA, ICAO)
    - Tider (scheduled, estimated, actual)
    - Status (på svenska)
    - Terminal och gate
    - Ursprungsflygplats
    - **Bagageinformation**:
      - Band-nummer (`baggage_claim`)
      - Första bagage (`first_bag`, `estimated_first_bag`)
      - Sista bagage (`last_bag`)
    - Anmärkningar

### Avgångar Sensor
- **State**: Antal avgående flyg
- **Attributes**:
  - `flights`: Lista med alla flyg inkl:
    - Flightnummer och code-share
    - Flygbolag (namn, IATA, ICAO)
    - Tider (scheduled, estimated, actual)
    - Status (på svenska)
    - Terminal och gate
    - Destinationsflygplats
    - **Gate-information**:
      - Gate-åtgärd (`gate_action`)
      - Gate öppnar (`gate_open`)
      - Gate stänger (`gate_close`)
    - **Incheckning**:
      - Status (`check_in_status`)
      - Disk från/till (`check_in_from`, `check_in_to`)
    - Anmärkningar

## Exempel på användning

### Lovelace Card - Ankomster

```yaml
type: markdown
content: |
  ## 🛬 Ankomster Arlanda
  {% set flights = state_attr('sensor.stockholm_arlanda_ankomster', 'flights') %}
  {% if flights %}
    {% for flight in flights[:10] %}
      **{{ flight.flight_id }}** {{ flight.airline }}
      {{ flight.origin }} → ARN
      {% if flight.actual_time %}
        ✅ Landade {{ flight.actual_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% elif flight.estimated_time %}
        🕐 Beräknad {{ flight.estimated_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% else %}
        📅 Schemalagd {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% endif %}
      
      Terminal {{ flight.terminal }} | Gate {{ flight.gate }}
      {% if flight.baggage_claim %}
        💼 Bagage: Band {{ flight.baggage_claim }}
        {% if flight.first_bag %}
          (Första väska {{ flight.first_bag | as_timestamp | timestamp_custom('%H:%M') }})
        {% endif %}
      {% endif %}
      
      Status: {{ flight.status }}
      {% if flight.remarks %}
        ⚠️ {{ flight.remarks }}
      {% endif %}
      
      ---
    {% endfor %}
  {% else %}
    Inga ankommande flyg just nu
  {% endif %}
```

### Lovelace Card - Avgångar

```yaml
type: markdown
content: |
  ## 🛫 Avgångar Arlanda
  {% set flights = state_attr('sensor.stockholm_arlanda_avgangar', 'flights') %}
  {% if flights %}
    {% for flight in flights[:10] %}
      **{{ flight.flight_id }}** {{ flight.airline }}
      ARN → {{ flight.destination }}
      {% if flight.actual_time %}
        ✅ Avgick {{ flight.actual_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% elif flight.estimated_time %}
        🕐 Beräknad {{ flight.estimated_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% else %}
        📅 Schemalagd {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% endif %}
      
      Terminal {{ flight.terminal }} | Gate {{ flight.gate }}
      {% if flight.gate_action %}
        🚪 {{ flight.gate_action }}
        {% if flight.gate_open %}
          (Öppnar {{ flight.gate_open | as_timestamp | timestamp_custom('%H:%M') }})
        {% endif %}
      {% endif %}
      
      {% if flight.check_in_status %}
        ✈️ Incheckning: {{ flight.check_in_status }}
        {% if flight.check_in_from %}
          Disk {{ flight.check_in_from }}-{{ flight.check_in_to }}
        {% endif %}
      {% endif %}
      
      Status: {{ flight.status }}
      {% if flight.remarks %}
        ⚠️ {{ flight.remarks }}
      {% endif %}
      
      ---
    {% endfor %}
  {% else %}
    Inga avgående flyg just nu
  {% endif %}
```

### Automation - Notifiering om förseningar

```yaml
automation:
  - alias: "Notifiera om försenade flyg"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_avgangar
    condition:
      - condition: template
        value_template: >
          {% set flights = state_attr('sensor.stockholm_arlanda_avgangar', 'flights') %}
          {{ flights | selectattr('status', 'search', 'Försenat') | list | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Försenade flyg från Arlanda"
          message: >
            {% set flights = state_attr('sensor.stockholm_arlanda_avgangar', 'flights') %}
            {% set delayed = flights | selectattr('status', 'search', 'Försenat') | list %}
            {{ delayed | length }} flyg är försenade
```

## API Information

Denna integration använder Swedavias officiella Flight Information API v2:
- **Endpoint**: `https://api.swedavia.se/flightinfo/v2`
- **Developer Portal**: https://apideveloper.swedavia.se/
- **Autentisering**: Subscription Key (Ocp-Apim-Subscription-Key header)
- **Kostnad**: Gratis för FlightInfo-produkten
- **Uppdateringsfrekvens**: Var 5:e minut
- **Rate limiting**: Implementerad med 1 sekunds minimum mellan requests

### Skaffa API-nyckel

1. **Registrera konto**: https://apideveloper.swedavia.se/
2. **Prenumerera på FlightInfo**: Produkter → FlightInfo → Subscribe (gratis)
3. **Hämta nyckel**: Profile → Subscriptions → Primary key

## Support

- 🐛 **Buggrapporter**: [GitHub Issues](https://github.com/frodr1k/Swedavia_info/issues)
- 💬 **Diskussioner**: [GitHub Discussions](https://github.com/frodr1k/Swedavia_info/discussions)

## License

MIT License - se [LICENSE](LICENSE) för detaljer

## Tack till

- Swedavia för att tillhandahålla ett öppet API
- Home Assistant communityt för inspiration och stöd
