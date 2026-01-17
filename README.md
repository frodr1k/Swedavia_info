# Swedavia Flight Information

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/frodr1k/Swedavia_info.svg)](https://github.com/frodr1k/Swedavia_info/releases)
[![License](https://img.shields.io/github/license/frodr1k/Swedavia_info.svg)](LICENSE)

A Home Assistant integration for displaying flight information from Swedish airports using Swedavia's official API.

**[🇸🇪 Läs på svenska](#svenska) | [Read in English](#english)**

---

<a name="english"></a>

## Features

- 🛬 **Arrivals** - Display arriving flights with baggage information
- 🛫 **Departures** - Display departing flights with gate and check-in info
- 🏢 **All Swedish Swedavia airports** - ARN, GOT, MMX, BMA, LLA, UME, VBY, KRN, RNB, VST, ORB, NYO
- ⏰ **Flexible time window** - Choose how many hours ahead/back to show flights
- 🔄 **Automatic updates** - Data refreshes every 5 minutes
- 🎫 **Code-share information** - Display all flight numbers for the same flight
- 💼 **Baggage information** - Belt numbers and times for first/last baggage
- 🚪 **Gate information** - Terminal, gate, opening and closing times
- ✈️ **Detailed flight information** - Status, delays, remarks
- 🔑 **API Key Rotation Management** - Automatic warnings and failover support

## Prerequisites - Get API Key

**Swedavia's API requires a free API key (Subscription Key):**

1. Go to Swedavia developer portal: https://apideveloper.swedavia.se/
2. Click **"Sign up"** and create a free account
3. Confirm your email address (check spam folder)
4. Log in to the portal
5. Go to **"Products"** → **"FlightInfo"**
6. Click **"Subscribe"** (free, immediate access)
7. Go to **"Profile"** → **"Subscriptions"**
8. Copy your **Primary key** or **Secondary key**

**The key looks something like:** `abc123def456ghi789jkl012mno345pq`

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations
   - Click menu (three dots) → Custom repositories
   - Add: `https://github.com/frodr1k/Swedavia_info`
   - Category: Integration

2. Install "Swedavia Flight Information" from HACS

3. Restart Home Assistant

### Manual installation

1. Copy the `custom_components/swedavia_flights` folder to your Home Assistant `config/custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Swedavia Flight Information"
4. Fill in the details:
   - **Primary API Key**: Your primary subscription key from the developer portal (required)
   - **Secondary API Key**: Your secondary key (optional but recommended)
   - **Airport**: Select which Swedish airport to monitor
   - **Flight type**: Arrivals, Departures, or Both
   - **Hours back**: How many hours back in time (default: 2)
   - **Hours ahead**: How many hours ahead in time (default: 24)

### Where do I find my API key?

1. Log in to https://apideveloper.swedavia.se/
2. Go to **Profile** → **Subscriptions**
3. Select your FlightInfo subscription
4. Copy **Primary key** (and preferably also **Secondary key**)

**💡 Tip:** Configure both primary and secondary keys for automatic failover during key rotation!

## 🔄 API Key Rotation

**Important:** Swedavia rotates API keys every 6 months for security reasons.

- **Primary key** rotates in April each year
- **Secondary key** rotates in October each year

### Automatic Failover (Recommended!)

If you configure **both primary and secondary keys**:
- ✅ Automatic switch to secondary key if primary expires
- ✅ No downtime during key rotation
- ✅ Time to update keys at your convenience

### Rotation Schedule 2025-2030

| Date | Key | Action |
|------|-----|--------|
| 2025-04-09 | Primary | Update before this date |
| 2025-10-03 | Secondary | Update before this date |
| 2026-04-08 | Primary | Update before this date |
| 2026-10-02 | Secondary | Update before this date |

**📚 Detailed information:**
- [KEY_ROTATION_MANAGEMENT.md](KEY_ROTATION_MANAGEMENT.md) - Complete guide
- [KEY_ROTATION_QUICK_ACCESS.md](KEY_ROTATION_QUICK_ACCESS.md) - ⚡ Ready-to-use dashboard buttons and scripts!

## Sensors

The integration creates the following sensors:

### Arrivals Sensor
- **State**: Number of arriving flights
- **Attributes**:
  - `flights`: List of all flights including:
    - Flight number and code-share
    - Airline (name, IATA, ICAO)
    - Times (scheduled, estimated, actual)
    - Status (in Swedish)
    - Terminal and gate
    - Origin airport
    - **Baggage information**:
      - Belt number (`baggage_claim`)
      - First baggage (`first_bag`, `estimated_first_bag`)
      - Last baggage (`last_bag`)
    - Remarks

### Departures Sensor
- **State**: Number of departing flights
- **Attributes**:
  - `flights`: List of all flights including:
    - Flight number and code-share
    - Airline (name, IATA, ICAO)
    - Times (scheduled, estimated, actual)
    - Status (in Swedish)
    - Terminal and gate
    - Destination airport
    - **Gate information**:
      - Gate action (`gate_action`)
      - Gate opens (`gate_open`)
      - Gate closes (`gate_close`)
    - **Check-in**:
      - Status (`check_in_status`)
      - Desk from/to (`check_in_from`, `check_in_to`)
    - Remarks

### Baggage Sensor 🎉
- **State**: Number of flights with baggage information
- **Attributes**:
  - `flights`: List of baggage events including:
    - Flight number and code-share
    - Airline
    - Origin airport
    - Arrival times (scheduled, actual)
    - Status
    - Terminal
    - **Baggage belt** (`baggage_claim_belt`)
    - **Baggage status** (`baggage_claim_status`)
    - **First bag** (estimated and actual time)
    - **Last bag** (time)

**Use cases**:
- Notifications when first bag arrives
- Monitor which belts are active
- Display when last bag is expected

### Key Rotation Sensor 🔑
- **State**: Status and days until next rotation
- **Attributes**:
  - Next rotation dates for both keys
  - Days until rotation
  - Warning messages
  - Update service reference

## Usage Examples

### Lovelace Card - Arrivals

```yaml
type: markdown
content: |
  ## 🛬 Arrivals Arlanda
  {% set flights = state_attr('sensor.stockholm_arlanda_arrivals', 'flights') %}
  {% if flights %}
    {% for flight in flights[:10] %}
      **{{ flight.flight_id }}** {{ flight.airline }}
      {{ flight.origin }} → ARN
      {% if flight.actual_time %}
        ✅ Landed {{ flight.actual_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% elif flight.estimated_time %}
        🕐 Estimated {{ flight.estimated_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% else %}
        📅 Scheduled {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% endif %}
      
      Terminal {{ flight.terminal }} | Gate {{ flight.gate }}
      {% if flight.baggage_claim %}
        💼 Baggage: Belt {{ flight.baggage_claim }}
        {% if flight.first_bag %}
          (First bag {{ flight.first_bag | as_timestamp | timestamp_custom('%H:%M') }})
        {% endif %}
      {% endif %}
      
      Status: {{ flight.status }}
      {% if flight.remarks %}
        ⚠️ {{ flight.remarks }}
      {% endif %}
      
      ---
    {% endfor %}
  {% else %}
    No arriving flights right now
  {% endif %}
```

### Lovelace Card - Departures

```yaml
type: markdown
content: |
  ## 🛫 Departures Arlanda
  {% set flights = state_attr('sensor.stockholm_arlanda_departures', 'flights') %}
  {% if flights %}
    {% for flight in flights[:10] %}
      **{{ flight.flight_id }}** {{ flight.airline }}
      ARN → {{ flight.destination }}
      {% if flight.actual_time %}
        ✅ Departed {{ flight.actual_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% elif flight.estimated_time %}
        🕐 Estimated {{ flight.estimated_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% else %}
        📅 Scheduled {{ flight.scheduled_time | as_timestamp | timestamp_custom('%H:%M') }}
      {% endif %}
      
      Terminal {{ flight.terminal }} | Gate {{ flight.gate }}
      {% if flight.gate_action %}
        🚪 {{ flight.gate_action }}
        {% if flight.gate_open %}
          (Opens {{ flight.gate_open | as_timestamp | timestamp_custom('%H:%M') }})
        {% endif %}
      {% endif %}
      
      {% if flight.check_in_status %}
        ✈️ Check-in: {{ flight.check_in_status }}
        {% if flight.check_in_from %}
          Desk {{ flight.check_in_from }}-{{ flight.check_in_to }}
        {% endif %}
      {% endif %}
      
      Status: {{ flight.status }}
      {% if flight.remarks %}
        ⚠️ {{ flight.remarks }}
      {% endif %}
      
      ---
    {% endfor %}
  {% else %}
    No departing flights right now
  {% endif %}
```

### Lovelace Card - Baggage Belts 💼

```yaml
type: markdown
content: |
  ## 💼 Baggage Belts Arlanda
  {% set flights = state_attr('sensor.stockholm_arlanda_baggage', 'flights') %}
  {% if flights %}
    {% set active = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    {% if active | length > 0 %}
      ## Active belts: {{ active | length }}
      {% for flight in active | sort(attribute='baggage_claim_belt') %}
      ### Belt {{ flight.baggage_claim_belt }}
      **{{ flight.flight_number }}** from {{ flight.arrival_airport_swedish }}
      
      {% if flight.baggage_claim_first_bag %}
      ✅ First bag: {{ flight.baggage_claim_first_bag }}
      {% endif %}
      {% if flight.baggage_claim_last_bag %}
      🏁 Last bag: {{ flight.baggage_claim_last_bag }}
      {% endif %}
      
      ---
      {% endfor %}
    {% else %}
      ✅ No active belts right now
    {% endif %}
  {% endif %}
```

**📚 More baggage card examples:** See [LOVELACE_BAGGAGE_EXAMPLES.md](LOVELACE_BAGGAGE_EXAMPLES.md) for 7 different variants, including:
- Simple list with active belts
- Markdown with full information
- Compact view with icons
- Detailed table
- Conditional cards (only shown when belts are active)
- Multi-airport overview
- With notifications

**📱 Automatic notifications:** See [BAGGAGE_NOTIFICATIONS.md](BAGGAGE_NOTIFICATIONS.md) for 7 different automations that send push notifications to your phone when bags start arriving!

### Automation - Baggage Belt Notification

```yaml
automation:
  - alias: "Notify when first bag arrives"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_baggage
        attribute: flights
    condition:
      - condition: template
        value_template: >
          {% set flights = state_attr('sensor.stockholm_arlanda_baggage', 'flights') %}
          {% set delivering = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
          {{ delivering | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Baggage belt activated"
          message: >
            {% set flights = state_attr('sensor.stockholm_arlanda_baggage', 'flights') %}
            {% set delivering = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | first %}
            Belt {{ delivering.baggage_claim_belt }} - Flight {{ delivering.flight_number }}
```

### Automation - Delay Notification

```yaml
automation:
  - alias: "Notify about delayed flights"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_departures
    condition:
      - condition: template
        value_template: >
          {% set flights = state_attr('sensor.stockholm_arlanda_departures', 'flights') %}
          {{ flights | selectattr('status', 'search', 'Försenat') | list | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Delayed flights from Arlanda"
          message: >
            {% set flights = state_attr('sensor.stockholm_arlanda_departures', 'flights') %}
            {% set delayed = flights | selectattr('status', 'search', 'Försenat') | list %}
            {{ delayed | length }} flights are delayed
```

## API Information

This integration uses Swedavia's official Flight Information API v2:
- **Endpoint**: `https://api.swedavia.se/flightinfo/v2`
- **Developer Portal**: https://apideveloper.swedavia.se/
- **Authentication**: Subscription Key (Ocp-Apim-Subscription-Key header)
- **Cost**: Free for FlightInfo product
- **Update frequency**: Every 5 minutes
- **Rate limiting**: Implemented with 1 second minimum between requests

### Get API Key

1. **Register account**: https://apideveloper.swedavia.se/
2. **Subscribe to FlightInfo**: Products → FlightInfo → Subscribe (free)
3. **Get key**: Profile → Subscriptions → Primary key

## Documentation

- 📖 **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- 🔑 **[Key Rotation Management](KEY_ROTATION_MANAGEMENT.md)** - Rotation guide and automation
- ⚡ **[Quick Access Guide](KEY_ROTATION_QUICK_ACCESS.md)** - Ready-to-use scripts and buttons
- 🎴 **[Baggage Card Examples](LOVELACE_BAGGAGE_EXAMPLES.md)** - 7 Lovelace card variants
- 📱 **[Baggage Notifications](BAGGAGE_NOTIFICATIONS.md)** - 7 notification automation variants
- 📋 **[Quick Setup](QUICK_SETUP.yaml)** - Copy-paste configuration examples

## Support

- 🐛 **Bug reports**: [GitHub Issues](https://github.com/frodr1k/Swedavia_info/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/frodr1k/Swedavia_info/discussions)

## License

MIT License - see [LICENSE](LICENSE) for details

## Credits

- Swedavia for providing an open API
- Home Assistant community for inspiration and support

---

<a name="svenska"></a>

# 🇸🇪 Svenska

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
- 🔑 **API-nyckel Rotationshantering** - Automatiska varningar och failover-stöd

## Installation

### HACS (Rekommenderat)

1. Lägg till detta repository som en custom repository i HACS:
   - Gå till HACS → Integrations
   - Klicka på menyn (tre prickar) → Custom repositories
   - Lägg till: `https://github.com/frodr1k/Swedavia_info`
   - Kategori: Integration

2. Installera "Swedavia Flight Information" från HACS

3. Starta om Home Assistant

## Konfiguration

1. Gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **Lägg till integration**
3. Sök efter "Swedavia Flight Information"
4. Fyll i uppgifterna

### Skaffa API-nyckel

1. Gå till https://apideveloper.swedavia.se/
2. Skapa ett gratis konto
3. Prenumerera på FlightInfo (gratis)
4. Kopiera din Primary key från Profile → Subscriptions

## Dokumentation på Svenska

- 🔑 **[Nyckelrotationshantering](KEY_ROTATION_MANAGEMENT.md)** - Komplett guide med rotation 2025-2030
- ⚡ **[Snabbguide](KEY_ROTATION_QUICK_ACCESS.md)** - Färdiga dashboard-knappar och scripts
- 🎴 **[Bagagekort-exempel](LOVELACE_BAGGAGE_EXAMPLES.md)** - 7 olika Lovelace-kort
- 📱 **[Bagagenotifieringar](BAGGAGE_NOTIFICATIONS.md)** - 7 olika automationer för push-notiser
- 📋 **[Snabbinstallation](QUICK_SETUP.yaml)** - Kopiera/klistra konfiguration

## Support

- 🐛 **Buggrapporter**: [GitHub Issues](https://github.com/frodr1k/Swedavia_info/issues)
- 💬 **Diskussioner**: [GitHub Discussions](https://github.com/frodr1k/Swedavia_info/discussions)

## Licens

MIT License - se [LICENSE](LICENSE) för detaljer
