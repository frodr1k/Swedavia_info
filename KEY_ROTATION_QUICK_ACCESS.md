# Easy Access to Key Rotation Service

## Quick Access Methods

### Method 1: Dashboard Button Card ⭐ Recommended

Add this button to your dashboard for one-click access:

```yaml
type: button
name: Uppdatera API-nycklar
icon: mdi:key-plus
tap_action:
  action: call-service
  service: swedavia_flights.update_api_keys
  service_data:
    api_key: !secret swedavia_api_key_primary
    api_key_secondary: !secret swedavia_api_key_secondary
```

**Setup:**
1. Add keys to `secrets.yaml`:
   ```yaml
   swedavia_api_key_primary: "your_primary_key_here"
   swedavia_api_key_secondary: "your_secondary_key_here"
   ```
2. When keys rotate, update `secrets.yaml`
3. Click button to update integration
4. Restart Home Assistant (if needed)

### Method 2: Script for Quick Update

Create a script in `configuration.yaml`:

```yaml
script:
  update_swedavia_keys:
    alias: "Uppdatera Swedavia API-nycklar"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: !secret swedavia_api_key_primary
          api_key_secondary: !secret swedavia_api_key_secondary
      - service: notify.persistent_notification
        data:
          title: "✅ API-nycklar uppdaterade"
          message: "Swedavia API-nycklar har uppdaterats för alla integrationer."
```

Then add a button to dashboard:

```yaml
type: button
name: Uppdatera API-nycklar
icon: mdi:key-plus
tap_action:
  action: call-service
  service: script.update_swedavia_keys
```

### Method 3: Input Helper for Manual Entry

For dynamic key updates without editing files:

**Step 1:** Create input helpers via UI or `configuration.yaml`:

```yaml
input_text:
  swedavia_primary_key:
    name: Swedavia Primary Key
    icon: mdi:key
    max: 64
    
  swedavia_secondary_key:
    name: Swedavia Secondary Key
    icon: mdi:key-variant
    max: 64
```

**Step 2:** Create update script:

```yaml
script:
  update_swedavia_keys_from_input:
    alias: "Uppdatera Swedavia-nycklar från input"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: "{{ states('input_text.swedavia_primary_key') }}"
          api_key_secondary: "{{ states('input_text.swedavia_secondary_key') }}"
      - service: notify.persistent_notification
        data:
          title: "✅ API-nycklar uppdaterade"
          message: "Swedavia API-nycklar har uppdaterats."
```

**Step 3:** Create dashboard card:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: 🔑 Swedavia API-nycklar
    entities:
      - entity: input_text.swedavia_primary_key
        name: Primary Key
      - entity: input_text.swedavia_secondary_key
        name: Secondary Key
      - entity: sensor.stockholm_arlanda_api_nyckel_rotation
        name: Rotation Status
  - type: button
    name: Uppdatera Nycklar
    icon: mdi:key-plus
    tap_action:
      action: call-service
      service: script.update_swedavia_keys_from_input
```

### Method 4: Complete Management Card

Full-featured card with status and update:

```yaml
type: vertical-stack
cards:
  # Status Card
  - type: markdown
    content: |
      ## 🔑 API-nyckel Management
      
      **Status:** {{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
      
      ### Primär Nyckel
      - Nästa rotation: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_next_rotation')[:10] }}
      - Dagar kvar: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_days_until') }}
      {% if state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_warning') %}
      
      ⚠️ **{{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_warning') }}**
      {% endif %}
      
      ### Sekundär Nyckel
      - Nästa rotation: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_next_rotation')[:10] }}
      - Dagar kvar: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_days_until') }}
      {% if state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_warning') %}
      
      ⚠️ **{{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_warning') }}**
      {% endif %}
      
      [Hämta nya nycklar →](https://apideveloper.swedavia.se/)
  
  # Input Fields
  - type: entities
    entities:
      - entity: input_text.swedavia_primary_key
        name: New Primary Key
      - entity: input_text.swedavia_secondary_key
        name: New Secondary Key
  
  # Update Button
  - type: button
    name: Uppdatera API-nycklar
    icon: mdi:key-plus
    tap_action:
      action: call-service
      service: script.update_swedavia_keys_from_input
```

### Method 5: Conditional Warning Card

Shows update button only when rotation is near:

```yaml
type: conditional
conditions:
  - condition: template
    value_template: >
      {{ 'rotation' in states('sensor.stockholm_arlanda_api_nyckel_rotation').lower() 
         and 'OK' not in states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
card:
  type: vertical-stack
  cards:
    - type: markdown
      content: |
        ## ⚠️ API-nyckel Rotation Påminnelse
        
        {{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
        
        Det är dags att uppdatera dina API-nycklar!
        
        1. Gå till [Swedavia Developer Portal](https://apideveloper.swedavia.se/)
        2. Hämta nya nycklar under Profile → Subscriptions
        3. Ange dem nedan och klicka "Uppdatera"
    
    - type: entities
      entities:
        - entity: input_text.swedavia_primary_key
        - entity: input_text.swedavia_secondary_key
    
    - type: button
      name: 🔄 Uppdatera Nycklar Nu
      icon: mdi:key-plus
      tap_action:
        action: call-service
        service: script.update_swedavia_keys_from_input
```

### Method 6: Developer Tools Quick Access

Create a shortcut in your `configuration.yaml`:

```yaml
homeassistant:
  customize:
    sensor.stockholm_arlanda_api_nyckel_rotation:
      custom_ui_state_card: state-card-custom-ui
      extra_data_template: >
        [
          {
            "type": "button",
            "action": "call-service",
            "service": "swedavia_flights.update_api_keys",
            "service_data": {
              "api_key": "{{ states('input_text.swedavia_primary_key') }}",
              "api_key_secondary": "{{ states('input_text.swedavia_secondary_key') }}"
            },
            "name": "Update Keys"
          }
        ]
```

### Method 7: Mobile App Notification Action

Get notified and update with one tap on mobile:

```yaml
automation:
  - alias: "API-nyckel Rotation Notifiering med Action"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_api_nyckel_rotation
    condition:
      - condition: template
        value_template: >
          {{ 'rotation' in trigger.to_state.state.lower() and 
             'OK' not in trigger.to_state.state }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Swedavia API-nyckel Rotation"
          message: "{{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}"
          data:
            actions:
              - action: "OPEN_PORTAL"
                title: "Öppna Developer Portal"
                uri: "https://apideveloper.swedavia.se/"
              - action: "OPEN_DASHBOARD"
                title: "Uppdatera Nycklar"
                uri: "/lovelace/swedavia"  # Your dashboard path
```

### Method 8: Voice Assistant Command

Create a sentence for voice update:

```yaml
conversation:
  intents:
    UpdateSwedaviaKeys:
      - "uppdatera swedavia nycklar"
      - "byt api nycklar för swedavia"
      - "rotera swedavia nycklar"

intent_script:
  UpdateSwedaviaKeys:
    speech:
      text: "Uppdaterar Swedavia API-nycklar nu"
    action:
      - service: script.update_swedavia_keys_from_input
```

Then just say: "Hey Google, uppdatera swedavia nycklar"

## Complete Setup Example

Here's a complete setup combining all methods:

### 1. Add to `secrets.yaml`:
```yaml
swedavia_api_key_primary: "your_primary_key"
swedavia_api_key_secondary: "your_secondary_key"
```

### 2. Add to `configuration.yaml`:
```yaml
input_text:
  swedavia_primary_key:
    name: Swedavia Primary Key
    icon: mdi:key
    max: 64
    
  swedavia_secondary_key:
    name: Swedavia Secondary Key
    icon: mdi:key-variant
    max: 64

script:
  update_swedavia_keys:
    alias: "Uppdatera Swedavia API-nycklar"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: !secret swedavia_api_key_primary
          api_key_secondary: !secret swedavia_api_key_secondary
      - service: notify.persistent_notification
        data:
          title: "✅ API-nycklar uppdaterade"
          message: "Swedavia API-nycklar har uppdaterats."

  update_swedavia_keys_from_input:
    alias: "Uppdatera från Input"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: "{{ states('input_text.swedavia_primary_key') }}"
          api_key_secondary: "{{ states('input_text.swedavia_secondary_key') }}"
      - service: input_text.set_value
        target:
          entity_id: input_text.swedavia_primary_key
        data:
          value: ""
      - service: input_text.set_value
        target:
          entity_id: input_text.swedavia_secondary_key
        data:
          value: ""
      - service: notify.persistent_notification
        data:
          title: "✅ API-nycklar uppdaterade"
          message: "Swedavia API-nycklar har uppdaterats och input rensad."

automation:
  - alias: "Swedavia Key Rotation Alert"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_api_nyckel_rotation
    condition:
      - condition: template
        value_template: >
          {{ 'rotation' in trigger.to_state.state.lower() and 
             'OK' not in trigger.to_state.state }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Swedavia API-nyckel Rotation"
          message: "{{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}"
          data:
            actions:
              - action: "OPEN_PORTAL"
                title: "Hämta nya nycklar"
                uri: "https://apideveloper.swedavia.se/"
```

### 3. Add dashboard card:
```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🔑 Swedavia API Management
    content: |
      **Status:** {{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
      
      {% if state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_warning') %}
      ### ⚠️ Varning
      {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_warning') }}
      {% endif %}
      {% if state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_warning') %}
      {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_warning') }}
      {% endif %}
      
      [→ Hämta nya nycklar](https://apideveloper.swedavia.se/)
  
  - type: conditional
    conditions:
      - condition: template
        value_template: >
          {{ 'rotation' in states('sensor.stockholm_arlanda_api_nyckel_rotation').lower() 
             and 'OK' not in states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
    card:
      type: entities
      title: Uppdatera Nycklar
      entities:
        - entity: input_text.swedavia_primary_key
          name: Ny Primary Key
        - entity: input_text.swedavia_secondary_key
          name: Ny Secondary Key
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Uppdatera från Secrets
        icon: mdi:key
        tap_action:
          action: call-service
          service: script.update_swedavia_keys
      - type: button
        name: Uppdatera från Input
        icon: mdi:key-plus
        tap_action:
          action: call-service
          service: script.update_swedavia_keys_from_input
```

## Best Practice Workflow

### Normal Situation (>3 days to rotation)
- Monitor sensor on dashboard
- Nothing to do

### Warning Period (1-3 days)
1. See warning on dashboard
2. Click "Hämta nya nycklar" link
3. Copy keys from portal
4. Paste into input fields on dashboard
5. Click "Uppdatera från Input"
6. Done!

### Rotation Day
1. Get mobile notification
2. Tap "Hämta nya nycklar"
3. Copy keys
4. Open Home Assistant app
5. Navigate to Swedavia dashboard
6. Paste and update
7. Integration auto-reloads

## Quick Command Reference

| Action | Command |
|--------|---------|
| Update from secrets | `script.update_swedavia_keys` |
| Update from input | `script.update_swedavia_keys_from_input` |
| Direct service call | `swedavia_flights.update_api_keys` |
| Check status | View `sensor.{airport}_api_nyckel_rotation` |

---

Choose the method that fits your workflow best! 🎯

**Recommended for most users:** Method 3 (Input Helper) with Method 4 (Complete Management Card)
