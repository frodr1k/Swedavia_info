# Lovelace Cards för Bagagestatus

Exempel på olika kort för att visa bagageinformation från Swedavia Flight Information integrationen.

## Förutsättningar

Du behöver ha lagt till minst en flygplats med **Ankomster** eller **Både ankomster och avgångar** i integrationen för att se bagagedata.

Sensorn heter: `sensor.{flygplats}_bagage`

Exempel:
- `sensor.stockholm_arlanda_ankomster_bagage`
- `sensor.goteborg_landvetter_ankomster_bagage`
- `sensor.malmo_ankomster_bagage`

---

## Variant 1: Enkel lista med alla band ⭐ Rekommenderad

```yaml
type: custom:auto-entities
card:
  type: entities
  title: 🛄 Bagageband - Aktuella utlämningar
  show_header_toggle: false
filter:
  include:
    - entity_id: sensor.*_bagage
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

**Visar:**
- Alla band där väskor är på väg ut
- Sorterat efter bandnummer
- Snyggt kort med blå accent

---

## Variant 2: Markdown med full information

```yaml
type: markdown
title: 🛄 Bagageutlämning just nu
content: |
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    
    {% if active_belts | length > 0 %}
      {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  ## Band {{ flight.baggage_claim_belt }}
  
  **Flight:** {{ flight.flight_number }} från {{ flight.arrival_airport_swedish }}
  **Status:** 🟢 Väskor på väg ut
  {% if flight.baggage_claim_first_bag %}
  **Första väska:** {{ flight.baggage_claim_first_bag }}
  {% endif %}
  {% if flight.baggage_claim_last_bag %}
  **Sista väska (est):** {{ flight.baggage_claim_last_bag }}
  {% endif %}
  **Ankomst:** {{ flight.scheduled_arrival_time }}
  
  ---
      {% endfor %}
    {% else %}
  ### ✅ Inga aktiva bagageband just nu
  
  Alla väskor är utlämnade eller inga flyg med bagagestatus.
    {% endif %}
  {% else %}
  ### ⚠️ Ingen bagagesensor hittades
  
  Lägg till en flygplats med ankomster i Swedavia-integrationen.
  {% endif %}
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
```

**Visar:**
- Alla band med pågående utlämning
- Flight nummer och ursprung
- Första och sista väska-tider
- Ankomsttid
- Snygg gradient-bakgrund

---

## Variant 3: Kompakt lista med ikoner

```yaml
type: custom:auto-entities
card:
  type: glance
  title: 🛄 Aktiva bagageband
  show_state: false
  columns: 4
filter:
  include:
    - entity_id: sensor.*_bagage
      attributes:
        baggage_claim_status: delivering
      options:
        name: >-
          [[[ return 'Band ' + entity.attributes.baggage_claim_belt; ]]]
        icon: mdi:bag-suitcase
        tap_action:
          action: more-info
  exclude: []
sort:
  method: attribute
  attribute: baggage_claim_belt
```

**Visar:**
- Kompakt vy med ikoner
- Bandnummer som namn
- 4 kolumner
- Klicka för mer info

---

## Variant 4: Detaljerad tabell med alla fält

```yaml
type: markdown
title: 🛄 Bagageband - Fullständig information
content: |
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    
    {% if active_belts | length > 0 %}
  | Band | Flight | Från | Status | Första väska | Sista väska | Ankomst |
  |:----:|:------:|:----:|:------:|:------------:|:-----------:|:-------:|
      {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  | **{{ flight.baggage_claim_belt }}** | {{ flight.flight_number }} | {{ flight.arrival_airport_swedish }} | 🟢 Aktiv | {{ flight.baggage_claim_first_bag if flight.baggage_claim_first_bag else '-' }} | {{ flight.baggage_claim_last_bag if flight.baggage_claim_last_bag else '-' }} | {{ flight.scheduled_arrival_time }} |
      {% endfor %}
      
  ---
  **Uppdaterad:** {{ as_timestamp(baggage_sensor[0].last_changed) | timestamp_custom('%H:%M:%S') }}
    {% else %}
  ### ✅ Inga aktiva bagageband
  
  Alla väskor är utlämnade.
  
  **Uppdaterad:** {{ as_timestamp(baggage_sensor[0].last_changed) | timestamp_custom('%H:%M:%S') }}
    {% endif %}
  {% else %}
  ### ⚠️ Ingen bagagesensor
  {% endif %}
```

**Visar:**
- Tabell med alla detaljer
- Sorterat efter band
- Senaste uppdateringstid
- Kompakt och läsbar

---

## Variant 5: Card med conditional visibility

```yaml
type: conditional
conditions:
  - condition: template
    value_template: >-
      {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
      {% if baggage_sensor %}
        {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
        {{ flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length > 0 }}
      {% else %}
        false
      {% endif %}
card:
  type: markdown
  title: 🛄 Aktiva bagageband
  content: |
    {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    
    {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
    ## 🟢 Band {{ flight.baggage_claim_belt }}
    
    **{{ flight.flight_number }}** från **{{ flight.arrival_airport_swedish }}**
    
    {% if flight.baggage_claim_first_bag %}
    - Första väska: {{ flight.baggage_claim_first_bag }}
    {% endif %}
    {% if flight.baggage_claim_last_bag %}
    - Sista väska (uppskattad): {{ flight.baggage_claim_last_bag }}
    {% endif %}
    
    {% if not loop.last %}---{% endif %}
    {% endfor %}
  card_mod:
    style: |
      ha-card {
        animation: pulse 2s ease-in-out infinite;
        border: 2px solid #4CAF50;
      }
      @keyframes pulse {
        0%, 100% { box-shadow: 0 0 10px rgba(76, 175, 80, 0.3); }
        50% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.6); }
      }
```

**Visar:**
- Kortet visas BARA när det finns aktiva band
- Pulserar för att dra uppmärksamhet
- Grön border
- Perfekt för dashboard som alltid är synlig

---

## Variant 6: Multi-flygplats överblick

Om du har flera flygplatser konfigurerade:

```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🛄 Bagagestatus - Alla flygplatser
    content: |
      {% set baggage_sensors = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
      
      {% if baggage_sensors | length > 0 %}
        {% for sensor in baggage_sensors %}
          {% set flights = sensor.attributes.flights | default([]) %}
          {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
          
      ## {{ sensor.attributes.friendly_name | replace(' Bagage', '') }}
      
          {% if active_belts | length > 0 %}
            {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
      - **Band {{ flight.baggage_claim_belt }}**: {{ flight.flight_number }} från {{ flight.arrival_airport_swedish }}
        {% if flight.baggage_claim_first_bag %}(Första väska: {{ flight.baggage_claim_first_bag }}){% endif %}
            {% endfor %}
          {% else %}
      ✅ Inga aktiva band
          {% endif %}
          
          {% if not loop.last %}---{% endif %}
        {% endfor %}
      {% else %}
      ### ⚠️ Inga bagagesensorer
      {% endif %}
```

**Visar:**
- Alla flygplatser du har konfigurerade
- Aktiva band per flygplats
- Perfekt översikt

---

## Variant 7: Med notifikation när nytt band aktiveras

Skapa automation + kort:

### Automation:
```yaml
automation:
  - alias: "Notifiera när bagageband aktiveras"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
    condition:
      - condition: template
        value_template: >
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_active = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
          {% set old_active = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
          {{ new_active | length > old_active | length }}
    action:
      - service: notify.persistent_notification
        data:
          title: "🛄 Nytt bagageband aktiverat"
          message: >
            {% set flights = trigger.to_state.attributes.flights | default([]) %}
            {% set active = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% for flight in active %}
              {% if flight not in trigger.from_state.attributes.flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            Band {{ flight.baggage_claim_belt }}: {{ flight.flight_number }} från {{ flight.arrival_airport_swedish }}
              {% endif %}
            {% endfor %}
```

### Card:
```yaml
type: markdown
title: 🛄 Bagageband med notifieringar
content: |
  Notifieringar är aktiverade när nya bagageband börjar lämna ut väskor.
  
  {% set baggage_sensor = states.sensor | selectattr('entity_id', 'search', '_bagage$') | list %}
  {% if baggage_sensor %}
    {% set flights = baggage_sensor[0].attributes.flights | default([]) %}
    {% set active_belts = flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
    
    {% if active_belts | length > 0 %}
  ## Aktiva band just nu: {{ active_belts | length }}
      {% for flight in active_belts | sort(attribute='baggage_claim_belt') %}
  
  ### Band {{ flight.baggage_claim_belt }}
  {{ flight.flight_number }} från {{ flight.arrival_airport_swedish }}
      {% endfor %}
    {% else %}
  ### ✅ Inga aktiva band
    {% endif %}
  {% endif %}
```

---

## Installation av Auto-entities (för vissa varianter)

Om du använder varianterna med `custom:auto-entities`, installera först:

1. Gå till **HACS** → **Frontend**
2. Sök efter "**Auto-entities**"
3. Klicka **Install**
4. Starta om Home Assistant

---

## Tips & Tricks

### Filtrera specifik flygplats:
```yaml
entity_id: sensor.stockholm_arlanda_ankomster_bagage
```

### Visa alla band (även inaktiva):
Ta bort filtret:
```yaml
baggage_claim_status: delivering
```

### Visa bara vissa band:
```yaml
{% set active_belts = flights | selectattr('baggage_claim_belt', 'in', ['1', '2', '3']) | list %}
```

### Lägg till ljud vid nytt band:
```yaml
action:
  - service: tts.google_translate_say
    data:
      entity_id: media_player.speaker
      message: "Bagageband {{ flight.baggage_claim_belt }} är nu aktivt för flight {{ flight.flight_number }}"
```

---

## Felsökning

### "Ingen bagagesensor hittades"
- Kontrollera att du har lagt till en flygplats med **Ankomster** eller **Både**
- Sensor måste ha `_bagage` i namnet

### "Inga aktiva band visas"
- Kontrollera att det faktiskt finns flyg med bagagestatus = "delivering"
- Testa att använda Developer Tools → States och sök efter din bagagesensor

### Card-mod fungerar inte
- Installera **card-mod** från HACS (Frontend)

---

**Välj den variant som passar din dashboard bäst!** 🎯

Den enklaste för nybörjare: **Variant 1** eller **Variant 2**  
Den snyggaste: **Variant 5** (med conditional + animation)  
För flera flygplatser: **Variant 6**
