# Swedavia Flight Information

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/frodr1k/Swedavia_info.svg)](https://github.com/frodr1k/Swedavia_info/releases)
[![License](https://img.shields.io/github/license/frodr1k/Swedavia_info.svg)](LICENSE)

A Home Assistant integration for displaying flight information from Swedish airports using Swedavia's official API.

> **⚠️ IMPORTANT - API LIMIT:** Swedavia's API has a strict limit of **10,001 API calls per 30 days**. This integration automatically optimizes update intervals to stay within this limit. The API Counter sensor helps you monitor usage in real-time.

**[🇸🇪 Läs på svenska](#svenska) | [Read in English](#english)**

---

<a name="english"></a>

## ⚠️ API Usage Limits

**Swedavia enforces a strict API limit:**
- **Maximum:** 10,001 API calls per 30-day rolling window
- **Monitoring:** Built-in API Counter tracks all calls
- **Auto-optimization:** Smart scheduler adjusts update intervals automatically
- **Safety margin:** Integration uses max 85% of limit by default

**What happens if you exceed the limit?**
- API returns 429 (Too Many Requests) errors
- No flight data until the 30-day window resets
- Your subscription key may be temporarily blocked

**Monitor your usage:**
- Check `sensor.api_call_counter` for current usage
- Automatic warnings at 75%, 90%, and 100%
- Detailed schedule information in sensor attributes

## Features

- 🛬 **Arrivals** - Display arriving flights with baggage information
- 🛫 **Departures** - Display departing flights with gate and check-in info
- 🏢 **All Swedish Swedavia airports** - ARN, GOT, MMX, BMA, LLA, UME, VBY, KRN, RNB, VST, ORB, NYO
- ⏰ **Flexible time window** - Choose how many hours ahead/back to show flights
- 🔄 **Automatic updates** - Smart scheduler optimizes update frequency (5-30 minutes)
- 🎫 **Code-share information** - Display all flight numbers for the same flight
- 💼 **Baggage information** - Belt numbers and times for first/last baggage
- 🚪 **Gate information** - Terminal, gate, opening and closing times
- ✈️ **Detailed flight information** - Status, delays, remarks
- 🔑 **API Key Rotation Management** - Automatic warnings and failover support
- 📊 **API Call Counter** - Monitor your API usage against the 10,001 calls/30 days limit
- ⚡ **Boost Mode** - Temporarily increase update frequency (2 min intervals for 4 hours)

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

### API Call Counter Sensor 📊
- **State**: Number of API calls in the last 30 days
- **Attributes**:
  - `total_calls_30_days`: Total number of API calls
  - `remaining_calls`: Remaining calls before limit
  - `percentage_used`: Percentage of limit used
  - `limit`: API limit (10,001 calls per 30 days)
  - `rolling_window_days`: Rolling window size (30 days)
  - `oldest_call`: Date of oldest API call in the window

**Important**: Swedavia's API has a limit of **10,001 calls per 30 days**. This sensor helps you monitor your usage and avoid hitting the limit.

**Icon behavior**:
- 🟢 Green counter: < 75% usage
- 🟡 Yellow warning: 75-89% usage
- 🟠 Orange alert: 90-99% usage
- 🔴 Red alert: ≥ 100% usage

**Automatic warnings**:
- 75% usage: Info message in logs
- 90% usage: Warning in logs
- 100% usage: Error in logs

## Smart Update Scheduler ⚙️

The integration automatically optimizes update intervals based on your configuration to stay within the API limit while providing the best possible update frequency.

**How it works:**
- **Single airport, arrivals OR departures only**: 5-10 minute intervals
- **Single airport, both arrivals AND departures**: 15-20 minute intervals
- **Multiple airports**: Automatically adjusted (up to 30 minutes)
- **Staggered updates**: Multiple airports update at different times for even load distribution

**Example with 2 airports:**
```
Airport 1 updates at: 00, 20, 40 minutes
Airport 2 updates at: 10, 30, 50 minutes
→ Continuous data updates every 10 minutes
```

**Safety margin**: Uses maximum 85% of API limit (8,501 of 10,001 calls) to allow buffer for:
- Network retries
- Manual API calls via services
- Boost mode usage
- Unexpected situations

## Boost Mode ⚡

**Temporarily increase update frequency for real-time updates when you're at the airport.**

### Overview
- **Normal interval**: 10-30 minutes
- **Boost interval**: 2 minutes
- **Duration**: 1-12 hours (default: 4 hours)
- **Use case**: When waiting at airport and need real-time gate/baggage updates

### ⚠️ WARNING
Boost Mode uses **7.5x more API calls** than normal operation!
- Normal 4 hours: ~48 API calls
- Boost 4 hours: ~360 API calls
- Recommended: Max 3-4 boost sessions per month

### Activate Boost

**Via Service:**
```yaml
service: swedavia_flights.enable_boost_mode
data:
  airport: "ARN"
  duration: 4  # hours (1-12)
```

**Via Automation (when entering airport zone):**
```yaml
automation:
  - alias: "Auto Boost When At Arlanda"
    trigger:
      - platform: zone
        entity_id: person.me
        zone: zone.arlanda_airport
        event: enter
    action:
      - service: swedavia_flights.enable_boost_mode
        data:
          airport: "ARN"
          duration: 4
```

**Via Button Card:**
```yaml
type: button
name: "⚡ Boost Arlanda (4h)"
icon: mdi:rocket-launch
tap_action:
  action: call-service
  service: swedavia_flights.enable_boost_mode
  data:
    airport: "ARN"
    duration: 4
```

### Deactivate Boost

**Automatic:** Boost mode ends automatically after the specified duration.

**Manual:**
```yaml
service: swedavia_flights.disable_boost_mode
data:
  airport: "ARN"
```

### Boost Mode Best Practices

✅ **DO:**
- Use only when at the airport
- Limit to 2-4 hours per session
- Maximum 3-4 boost sessions per month
- Monitor API usage with counter sensor

❌ **DON'T:**
- Leave boost active overnight
- Activate for multiple airports simultaneously
- Use for daily monitoring
- Ignore API usage warnings

### API Impact Example

With smart scheduler using 85% of limit (~8,640 calls/month):
- Available margin: ~1,361 calls
- One 4-hour boost: ~360 calls (uses 26% of margin)
- Safe limit: 3-4 boost sessions per month

## Services

### update_api_keys

Update API keys when they are rotated by Swedavia.

```yaml
service: swedavia_flights.update_api_keys
data:
  api_key: "new_primary_key_here"
  api_key_secondary: "new_secondary_key_here"
```

### enable_boost_mode

Temporarily increase update frequency to 2 minutes.

```yaml
service: swedavia_flights.enable_boost_mode
data:
  airport: "ARN"  # Airport IATA code
  duration: 4     # Hours (1-12), default: 4
```

### disable_boost_mode

Manually disable boost mode before it expires.

```yaml
service: swedavia_flights.disable_boost_mode
data:
  airport: "ARN"  # Airport IATA code
```

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
- **API Limit**: 10,001 calls per 30 days (strictly enforced)
- **Update frequency**: 5-30 minutes (automatically optimized based on configuration)
- **Rate limiting**: 1 second minimum between requests
- **Boost mode**: Optional 2-minute intervals for temporary real-time updates

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

> **⚠️ VIKTIGT - API-GRÄNS:** Swedavias API har en strikt gräns på **10,001 API-anrop per 30 dagar**. Integrationen optimerar automatiskt uppdateringsintervall för att hålla sig inom denna gräns. API Counter-sensorn hjälper dig övervaka användningen i realtid.

## ⚠️ API-användningsgränser

**Swedavia har en strikt API-gräns:**
- **Maximum:** 10,001 API-anrop per 30-dagars rullande fönster
- **Övervakning:** Inbyggd API Counter spårar alla anrop
- **Auto-optimering:** Smart scheduler justerar uppdateringsintervall automatiskt
- **Säkerhetsmarginal:** Integrationen använder max 85% av gränsen som standard

**Vad händer om du överskrider gränsen?**
- API:et returnerar 429 (Too Many Requests) fel
- Ingen flygdata tills 30-dagars fönstret återställs
- Din prenumerationsnyckel kan blockeras temporärt

**Övervaka din användning:**
- Kolla `sensor.api_call_counter` för aktuell användning
- Automatiska varningar vid 75%, 90% och 100%
- Detaljerad schemainformation i sensor-attribut

## Funktioner

- 🛬 **Ankomster** - Visa ankommande flyg med bagage-information
- 🛫 **Avgångar** - Visa avgående flyg med gate och incheckning
- 🏢 **Alla svenska Swedavia-flygplatser** - ARN, GOT, MMX, BMA, LLA, UME, VBY, KRN, RNB, VST, ORB, NYO
- ⏰ **Flexibelt tidsfönster** - Välj hur många timmar framåt/bakåt du vill se flyg
- 🔄 **Smart uppdatering** - Scheduler optimerar uppdateringsfrekvens (5-30 minuter)
- 🎫 **Code-share information** - Visa alla flightnummer för samma flygning
- 💼 **Bagageinformation** - Band-nummer och tider för första/sista bagage
- 🚪 **Gate-information** - Terminal, gate, öppnings- och stängningstider
- ✈️ **Detaljerad flyginformation** - Status, förseningar, anmärkningar
- 🔑 **API-nyckel Rotationshantering** - Automatiska varningar och failover-stöd
- 📊 **API-anropsräknare** - Övervaka din API-användning mot 10,001 anrop/30 dagar gränsen
- ⚡ **Boost-läge** - Tillfälligt ökad uppdateringsfrekvens (2 min intervall i 4 timmar)

## Smart Uppdateringsschemaläggare ⚙️

Integrationen optimerar automatiskt uppdateringsintervall baserat på din konfiguration för att hålla sig inom API-gränsen samtidigt som du får bästa möjliga uppdateringsfrekvens.

**Hur det fungerar:**
- **En flygplats, endast ankomster ELLER avgångar**: 5-10 minuters intervall
- **En flygplats, både ankomster OCH avgångar**: 15-20 minuters intervall
- **Flera flygplatser**: Automatiskt justerat (upp till 30 minuter)
- **Förskjutna uppdateringar**: Flera flygplatser uppdateras vid olika tidpunkter för jämn belastning

**Exempel med 2 flygplatser:**
```
Flygplats 1 uppdateras: 00, 20, 40 minuter
Flygplats 2 uppdateras: 10, 30, 50 minuter
→ Kontinuerlig datauppdatering var 10:e minut
```

**Säkerhetsmarginal**: Använder max 85% av API-gränsen (8,501 av 10,001 anrop) för att ge utrymme för:
- Nätverksförsök
- Manuella API-anrop via tjänster
- Boost-läge användning
- Oväntade situationer

## Boost-läge ⚡

**Öka tillfälligt uppdateringsfrekvensen för realtidsuppdateringar när du är på flygplatsen.**

### Översikt
- **Normalt intervall**: 10-30 minuter
- **Boost-intervall**: 2 minuter
- **Varaktighet**: 1-12 timmar (standard: 4 timmar)
- **Användningsfall**: När du väntar på flygplatsen och behöver realtidsuppdateringar om gate/bagage

### ⚠️ VARNING
Boost-läge använder **7.5x fler API-anrop** än normal drift!
- Normal 4 timmar: ~48 API-anrop
- Boost 4 timmar: ~360 API-anrop
- Rekommenderat: Max 3-4 boost-sessioner per månad

### Aktivera Boost

**Via Tjänst:**
```yaml
service: swedavia_flights.enable_boost_mode
data:
  airport: "ARN"
  duration: 4  # timmar (1-12)
```

**Via Automation (när du kommer till flygplatsen):**
```yaml
automation:
  - alias: "Auto Boost När På Arlanda"
    trigger:
      - platform: zone
        entity_id: person.me
        zone: zone.arlanda
        event: enter
    action:
      - service: swedavia_flights.enable_boost_mode
        data:
          airport: "ARN"
          duration: 4
```

**Via Knapp-kort:**
```yaml
type: button
name: "⚡ Boosta Arlanda (4h)"
icon: mdi:rocket-launch
tap_action:
  action: call-service
  service: swedavia_flights.enable_boost_mode
  data:
    airport: "ARN"
    duration: 4
```

### Avaktivera Boost

**Automatiskt:** Boost-läget avslutas automatiskt efter angiven varaktighet.

**Manuellt:**
```yaml
service: swedavia_flights.disable_boost_mode
data:
  airport: "ARN"
```

### Bästa Praxis för Boost-läge

✅ **GÖR:**
- Använd endast när du är på flygplatsen
- Begränsa till 2-4 timmar per session
- Maximum 3-4 boost-sessioner per månad
- Övervaka API-användning med räknarsensor

❌ **GÖR INTE:**
- Lämna boost aktiverat över natten
- Aktivera för flera flygplatser samtidigt
- Använd för daglig övervakning
- Ignorera API-användningsvarningar

### API-påverkan Exempel

Med smart scheduler som använder 85% av gränsen (~8,640 anrop/månad):
- Tillgänglig marginal: ~1,361 anrop
- En 4-timmars boost: ~360 anrop (använder 26% av marginalen)
- Säker gräns: 3-4 boost-sessioner per månad

## Tjänster

### update_api_keys

Uppdatera API-nycklar när de roteras av Swedavia.

```yaml
service: swedavia_flights.update_api_keys
data:
  api_key: "ny_primär_nyckel_här"
  api_key_secondary: "ny_sekundär_nyckel_här"
```

### enable_boost_mode

Öka tillfälligt uppdateringsfrekvensen till 2 minuter.

```yaml
service: swedavia_flights.enable_boost_mode
data:
  airport: "ARN"  # Flygplats IATA-kod
  duration: 4     # Timmar (1-12), standard: 4
```

### disable_boost_mode

Avaktivera boost-läget manuellt innan det går ut.

```yaml
service: swedavia_flights.disable_boost_mode
data:
  airport: "ARN"  # Flygplats IATA-kod
```

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
