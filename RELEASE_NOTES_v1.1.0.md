# Release Notes - v1.1.0

## 🎉 New Feature: Baggage Claim Sensor

### 💼 Dedicated Baggage Tracking

Added a new sensor specifically for tracking baggage claim information!

**What it does:**
- Shows number of flights with active baggage claim information
- Provides detailed baggage tracking for arriving flights
- Perfect for notifications and monitoring specific flights

### Sensor Details

**Entity ID**: `sensor.{airport}_bagage`

**State**: Count of flights with baggage information

**Attributes**:
- `baggage_claims`: List of baggage claim events including:
  - Flight number and code-shares
  - Airline information
  - Origin airport
  - Scheduled and actual arrival times
  - Flight status
  - Terminal
  - **Baggage belt/carousel number**
  - **Estimated first bag time**
  - **Actual first bag time**
  - **Last bag time**

### Use Cases

- ✅ Get notified when first bag arrives for your flight
- ✅ Monitor which baggage belts are active
- ✅ Track when last bag is expected
- ✅ Display baggage information on dashboard
- ✅ Create automations for specific flight numbers

### Example: Lovelace Card

```yaml
type: markdown
content: |
  ## 💼 Bagageband Arlanda
  {% set baggage = state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims') %}
  {% if baggage %}
    Antal flyg: {{ states('sensor.stockholm_arlanda_bagage') }}
    
    {% for claim in baggage[:8] %}
      **{{ claim.flight_id }}** från {{ claim.origin }}
      
      {% if claim.first_bag %}
        ✅ Första väska: {{ claim.first_bag | as_timestamp | timestamp_custom('%H:%M') }}
      {% elif claim.estimated_first_bag %}
        🕐 Beräknad: {{ claim.estimated_first_bag | as_timestamp | timestamp_custom('%H:%M') }}
      {% endif %}
      
      📍 Band {{ claim.baggage_claim }} | Terminal {{ claim.terminal }}
      ---
    {% endfor %}
  {% endif %}
```

### Example: Automation for Specific Flight

```yaml
automation:
  - alias: "Notifiera om specifikt flyg på bagageband"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_bagage
        attribute: baggage_claims
    variables:
      my_flight: "SK1234"  # Ditt flightnummer
    condition:
      - condition: template
        value_template: >
          {% set baggage = state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims') %}
          {{ baggage | selectattr('flight_id', 'search', my_flight) | list | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Ditt flyg {{ my_flight }} har landat!"
          message: >
            {% set baggage = state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims') %}
            {% set my_claim = baggage | selectattr('flight_id', 'search', my_flight) | first %}
            Bagageband: {{ my_claim.baggage_claim }}
            Terminal: {{ my_claim.terminal }}
            {% if my_claim.first_bag %}
            Första väskan ute: {{ my_claim.first_bag | as_timestamp | timestamp_custom('%H:%M') }}
            {% endif %}
```

### Example: First Bag Notification

```yaml
automation:
  - alias: "Notifiera när första väskan kommit ut"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_bagage
        attribute: baggage_claims
    condition:
      - condition: template
        value_template: >
          {% set baggage = state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims') %}
          {{ baggage | selectattr('first_bag') | list | length > 0 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Bagageband {{ state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims')[0].baggage_claim }}"
          message: >
            {% set claim = state_attr('sensor.stockholm_arlanda_bagage', 'baggage_claims')[0] %}
            Första väskan från {{ claim.flight_id }} har kommit ut!
```

## 📚 Documentation Updates

- Added comprehensive baggage sensor documentation in README
- Added Lovelace card examples
- Added automation examples for:
  - First bag notifications
  - Specific flight tracking
  - Baggage belt monitoring
- Swedish and English translations included

## 🔧 Technical Details

- Automatically created when `arrivals` or `both` flight types are configured
- Filters only flights with baggage claim information
- Sorted chronologically by arrival time
- Includes all baggage-related timestamps from Swedavia API
- Icon: `mdi:bag-suitcase`
- State class: Measurement

## 📈 Performance

- No additional API calls (uses existing arrivals data)
- Efficient filtering of baggage information
- Updates in sync with arrivals sensor (every 5 minutes)

## 🌍 Translations

Added entity names in both languages:
- **Swedish**: "Bagage"
- **English**: "Baggage Claim"

## 🔄 Upgrade Notes

Simply update via HACS or pull the latest code:

1. The baggage sensor will be **automatically created** for:
   - Existing configurations with "arrivals" flight type
   - Existing configurations with "both" flight types
2. Restart Home Assistant after update
3. New entity will appear as: `sensor.{airport}_bagage`

No configuration changes needed!

## 🎯 What's Next?

Future improvements being considered:
- Binary sensor for active baggage belts
- Event triggers for first/last bag
- Separate notifications per baggage belt
- Historical baggage delay statistics

---

**Full Changelog**: v1.0.1...v1.1.0
