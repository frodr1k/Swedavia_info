# Lovelace Cards for Baggage Status

Examples of different cards to display baggage information from the Swedavia Flight Information integration.

> **📱 Want push notifications when bags start arriving?**  
> See [BAGGAGE_NOTIFICATIONS.md](BAGGAGE_NOTIFICATIONS.md) for 7 different automations with mobile notifications!

## Prerequisites

You need to have added at least one airport with **Arrivals** or **Both arrivals and departures** in the integration to see baggage data.

The sensor is named: `sensor.{airport}_baggage`

Examples:
- `sensor.stockholm_arlanda_arrivals_baggage`
- `sensor.goteborg_landvetter_arrivals_baggage`
- `sensor.malmo_arrivals_baggage`

---

## Variant 1: Simple List of All Belts ⭐ Recommended

```yaml
type: custom:auto-entities
card:
  type: entities
  title: 🛄 Baggage Belts - Current Deliveries
  show_header_toggle: false
filter:
  include:
    - entity_id: sensor.*_baggage
      attributes:
        baggage_claim_status: delivering
  exclude: []
sort:
  method: attribute
  attribute: baggage_claim_belt
card_mod:
  style: |
    ha-card {
      border-left: 4px solid #2196F3;
    }
```

**Displays:**
- All belts where bags are being delivered
- Sorted by belt number
- Nice card with blue accent

---

## Variant 2: Markdown with Full Information

```yaml
type: markdown
title: 🛄 Baggage Claim Right Now
content: |
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_baggage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    
    {% if active_belts | length > 0 %}
      {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  ## Belt {{ flight.baggage_claim_belt }}
  
  **Flight:** {{ flight.flight_number }} from {{ flight.arrival_airport_swedish }}
  **Status:** 🟢 Bags being delivered
  {% if flight.baggage_claim_first_bag %}
  **First bag:** {{ flight.baggage_claim_first_bag }}
  {% endif %}
  {% if flight.baggage_claim_last_bag %}
  **Last bag (est):** {{ flight.baggage_claim_last_bag }}
  {% endif %}
  **Arrival:** {{ flight.scheduled_arrival_time }}
  
  ---
      {% endfor %}
    {% else %}
  ### ✅ No active baggage belts right now
  
  All bags delivered or no flights with baggage status.
    {% endif %}
  {% else %}
  ### ⚠️ No baggage sensor found
  
  Add an airport with arrivals in the Swedavia integration.
  {% endif %}
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
```

**Displays:**
- All belts with ongoing delivery
- Flight number and origin
- First and last bag times
- Scheduled arrival time
- Beautiful gradient background

---

## Variant 3: Entity Card with Filter

```yaml
type: entities
title: 🛄 Active Baggage Belts
entities:
  - type: custom:auto-entities
    filter:
      include:
        - entity_id: sensor.*_baggage
          attributes:
            baggage_claim_status: delivering
      exclude: []
    sort:
      method: attribute
      attribute: baggage_claim_belt
    card:
      type: custom:template-entity-row
      name: >
        {{ state_attr(config.entity, 'baggage_claim_belt') }} - 
        {{ state_attr(config.entity, 'flight_number') }}
      secondary: >
        {{ state_attr(config.entity, 'arrival_airport_swedish') }}
      icon: mdi:bag-suitcase
```

**Displays:**
- Clean list format
- Belt number and flight
- Origin airport
- Luggage icon

---

## Variant 4: Grid Card with Individual Belts

```yaml
type: grid
columns: 2
square: false
cards:
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_baggage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  - type: markdown
    content: |
      ## 🛄 Belt {{ flight.baggage_claim_belt }}
      
      **{{ flight.flight_number }}**  
      from {{ flight.arrival_airport_swedish }}
      
      {% if flight.baggage_claim_first_bag %}
      🟢 Started: {{ flight.baggage_claim_first_bag }}
      {% endif %}
      
      {% if flight.baggage_claim_last_bag %}
      ⏱️ Est end: {{ flight.baggage_claim_last_bag }}
      {% endif %}
    card_mod:
      style: |
        ha-card {
          background: rgba(33, 150, 243, 0.1);
          border-left: 4px solid #2196F3;
        }
    {% endfor %}
  {% endif %}
```

**Displays:**
- Grid layout with 2 columns
- Separate card per active belt
- Start and estimated end time
- Blue accent color

---

## Variant 5: Glance Card - Quick Overview

```yaml
type: glance
title: 🛄 Baggage Overview
entities:
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_baggage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    {% for flight in active_belts %}
  - entity: sensor.{{ baggage_sensor[0].entity_id.split('.')[1] }}
    name: Belt {{ flight.baggage_claim_belt }}
    icon: mdi:bag-suitcase
    {% endfor %}
  {% endif %}
columns: 4
show_state: false
```

**Displays:**
- Compact glance view
- Icons for active belts
- Up to 4 belts visible at once
- Perfect for small spaces

---

## Variant 6: Conditional Card - Only Show When Active

```yaml
type: conditional
conditions:
  - entity: sensor.stockholm_arlanda_arrivals_baggage
    state_not: "unavailable"
  - condition: template
    value_template: >
      {{ state_attr('sensor.stockholm_arlanda_arrivals_baggage', 'active_belts') | int > 0 }}
card:
  type: vertical-stack
  cards:
    - type: markdown
      content: |
        ## 🛄 Baggage Claim Active
        
        **{{ state_attr('sensor.stockholm_arlanda_arrivals_baggage', 'active_belts') }}** belt(s) currently delivering bags
    
    - type: entities
      entities:
        - entity: sensor.stockholm_arlanda_arrivals_baggage
          name: Full Baggage Info
          icon: mdi:information-outline
```

**Displays:**
- Only appears when bags are being delivered
- Shows number of active belts
- Link to full sensor information
- Saves dashboard space

---

## Variant 7: Advanced - Separate Card Per Flight

```yaml
type: vertical-stack
cards:
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_baggage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    {% if active_belts | length > 0 %}
      {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  - type: entities
    title: "Flight {{ flight.flight_number }} - Belt {{ flight.baggage_claim_belt }}"
    entities:
      - type: attribute
        entity: sensor.{{ baggage_sensor[0].entity_id.split('.')[1] }}
        attribute: arrival_airport_swedish
        name: From
        icon: mdi:airplane-landing
      - type: attribute
        entity: sensor.{{ baggage_sensor[0].entity_id.split('.')[1] }}
        attribute: scheduled_arrival_time
        name: Arrival Time
        icon: mdi:clock-outline
      {% if flight.baggage_claim_first_bag %}
      - type: attribute
        entity: sensor.{{ baggage_sensor[0].entity_id.split('.')[1] }}
        attribute: baggage_claim_first_bag
        name: First Bag
        icon: mdi:bag-checked
      {% endif %}
      {% if flight.baggage_claim_last_bag %}
      - type: attribute
        entity: sensor.{{ baggage_sensor[0].entity_id.split('.')[1] }}
        attribute: baggage_claim_last_bag
        name: Last Bag (est)
        icon: mdi:bag-suitcase-off
      {% endif %}
    card_mod:
      style: |
        ha-card {
          border-left: 4px solid #4CAF50;
        }
      {% endfor %}
    {% else %}
  - type: markdown
    content: |
      ### ✅ No Baggage Deliveries
      
      All bags have been delivered or no active flights with baggage information.
    {% endif %}
  {% else %}
  - type: markdown
    content: |
      ### ⚠️ No Baggage Sensor
      
      Add an airport with arrivals in the Swedavia integration to see baggage information.
  {% endif %}
```

**Displays:**
- Detailed card per active flight
- All baggage information
- Expandable rows
- Green accent border
- Message when no active belts

---

## Installation Requirements

### Required for Variant 1, 3:
- **auto-entities** card: Install via HACS
- Search for "auto-entities" in HACS Frontend

### Optional Styling:
- **card-mod**: For custom styling
- Install via HACS Frontend

### All Other Variants:
- Use standard Home Assistant cards
- No additional installations needed

---

## Troubleshooting

### "Entity not found"
- Verify sensor name matches your airport
- Check integration is properly configured
- Ensure "Arrivals" or "Both" selected in config

### "No data displayed"
- No flights currently delivering baggage
- Check `sensor.{airport}_baggage` state and attributes
- Verify flights in attributes have `baggage_claim_status: delivering`

### "auto-entities not working"
- Install auto-entities from HACS
- Restart Home Assistant
- Clear browser cache

### "Templates not rendering"
- Check Jinja2 syntax
- Verify sensor name in template
- Use Developer Tools → Template to test

---

## Tips & Tricks

1. **Replace sensor name**: Change `stockholm_arlanda` to your airport code
2. **Combine variants**: Mix and match cards for your needs
3. **Add to dashboard**: Create a dedicated "Airport" view
4. **Mobile friendly**: Variants 1, 5, and 6 work great on mobile
5. **Notifications**: Combine with [BAGGAGE_NOTIFICATIONS.md](BAGGAGE_NOTIFICATIONS.md) for alerts

---

**Recommended setup:** Start with Variant 1 (simple list), then add Variant 2 (detailed info) if you want more information.
