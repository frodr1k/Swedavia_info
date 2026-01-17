# Easy Access to Key Rotation Service

Eight different methods to quickly update your Swedavia API keys when they rotate.

## Quick Access Methods

### Method 1: Dashboard Button Card ⭐ Recommended

Add this button to your dashboard for one-click access:

```yaml
type: button
name: Update API Keys
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
    alias: "Update Swedavia API Keys"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: !secret swedavia_api_key_primary
          api_key_secondary: !secret swedavia_api_key_secondary
      - service: notify.persistent_notification
        data:
          title: "✅ API Keys Updated"
          message: "Swedavia API keys have been updated for all integrations."
```

Then add a button to dashboard:

```yaml
type: button
name: Update API Keys
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
    alias: "Update Swedavia Keys from Input"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: "{{ states('input_text.swedavia_primary_key') }}"
          api_key_secondary: "{{ states('input_text.swedavia_secondary_key') }}"
      - service: notify.persistent_notification
        data:
          title: "✅ API Keys Updated"
          message: "Swedavia API keys have been updated."
```

**Step 3:** Create dashboard card:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: 🔑 Swedavia API Keys
    entities:
      - entity: input_text.swedavia_primary_key
        name: Primary Key
      - entity: input_text.swedavia_secondary_key
        name: Secondary Key
      - entity: sensor.stockholm_arlanda_api_key_rotation
        name: Rotation Status
  - type: button
    name: Update Keys
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
      ## 🔑 API Key Management
      
      **Status:** {{ states('sensor.stockholm_arlanda_api_key_rotation') }}
      
      ### Primary Key
      - Next rotation: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_next_rotation')[:10] }}
      - Days remaining: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_days_until') }}
      {% if state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_warning') %}
      
      ⚠️ **{{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_warning') }}**
      {% endif %}
      
      ### Secondary Key
      - Next rotation: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_next_rotation')[:10] }}
      - Days remaining: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_days_until') }}
      {% if state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_warning') %}
      
      ⚠️ **{{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_warning') }}**
      {% endif %}
      
      [Get new keys →](https://apideveloper.swedavia.se/)
  
  # Input Fields
  - type: entities
    entities:
      - entity: input_text.swedavia_primary_key
        name: New Primary Key
      - entity: input_text.swedavia_secondary_key
        name: New Secondary Key
  
  # Update Button
  - type: button
    name: Update API Keys
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
      {{ 'rotation' in states('sensor.stockholm_arlanda_api_key_rotation').lower() 
         and 'OK' not in states('sensor.stockholm_arlanda_api_key_rotation') }}
card:
  type: vertical-stack
  cards:
    - type: markdown
      content: |
        ## ⚠️ API Key Rotation Reminder
        
        {{ states('sensor.stockholm_arlanda_api_key_rotation') }}
        
        It's time to update your API keys!
        
        1. Go to [Swedavia Developer Portal](https://apideveloper.swedavia.se/)
        2. Get new keys under Profile → Subscriptions
        3. Enter them below and click "Update"
    
    - type: entities
      entities:
        - entity: input_text.swedavia_primary_key
        - entity: input_text.swedavia_secondary_key
    
    - type: button
      name: 🔄 Update Keys Now
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
    sensor.stockholm_arlanda_api_key_rotation:
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
  - alias: "API Key Rotation Notification with Action"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_api_key_rotation
    condition:
      - condition: template
        value_template: >
          {{ 'rotation' in trigger.to_state.state.lower() and 
             'OK' not in trigger.to_state.state }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Swedavia API Key Rotation"
          message: "{{ states('sensor.stockholm_arlanda_api_key_rotation') }}"
          data:
            actions:
              - action: "OPEN_PORTAL"
                title: "Open Developer Portal"
                uri: "https://apideveloper.swedavia.se/"
              - action: "OPEN_DASHBOARD"
                title: "Update Keys"
                uri: "/lovelace/swedavia"  # Your dashboard path
```

### Method 8: Voice Assistant Command

Create a sentence for voice update:

```yaml
conversation:
  intents:
    UpdateSwedaviaKeys:
      - "update swedavia keys"
      - "rotate api keys for swedavia"
      - "change swedavia keys"

intent_script:
  UpdateSwedaviaKeys:
    speech:
      text: "Updating Swedavia API keys now"
    action:
      - service: script.update_swedavia_keys_from_input
```

Then just say: "Hey Google, update swedavia keys"

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
    alias: "Update Swedavia API Keys"
    icon: mdi:key-chain
    sequence:
      - service: swedavia_flights.update_api_keys
        data:
          api_key: !secret swedavia_api_key_primary
          api_key_secondary: !secret swedavia_api_key_secondary
      - service: notify.persistent_notification
        data:
          title: "✅ API Keys Updated"
          message: "Swedavia API keys have been updated."

  update_swedavia_keys_from_input:
    alias: "Update from Input"
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
          title: "✅ API Keys Updated"
          message: "Swedavia API keys have been updated and input cleared."

automation:
  - alias: "Swedavia Key Rotation Alert"
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_api_key_rotation
    condition:
      - condition: template
        value_template: >
          {{ 'rotation' in trigger.to_state.state.lower() and 
             'OK' not in trigger.to_state.state }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Swedavia API Key Rotation"
          message: "{{ states('sensor.stockholm_arlanda_api_key_rotation') }}"
          data:
            actions:
              - action: "OPEN_PORTAL"
                title: "Get New Keys"
                uri: "https://apideveloper.swedavia.se/"
```

### 3. Add dashboard card:
```yaml
type: vertical-stack
cards:
  - type: markdown
    title: 🔑 Swedavia API Management
    content: |
      **Status:** {{ states('sensor.stockholm_arlanda_api_key_rotation') }}
      
      {% if state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_warning') %}
      ### ⚠️ Warning
      {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_warning') }}
      {% endif %}
      {% if state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_warning') %}
      {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_warning') }}
      {% endif %}
      
      [→ Get new keys](https://apideveloper.swedavia.se/)
  
  - type: conditional
    conditions:
      - condition: template
        value_template: >
          {{ 'rotation' in states('sensor.stockholm_arlanda_api_key_rotation').lower() 
             and 'OK' not in states('sensor.stockholm_arlanda_api_key_rotation') }}
    card:
      type: entities
      title: Update Keys
      entities:
        - entity: input_text.swedavia_primary_key
          name: New Primary Key
        - entity: input_text.swedavia_secondary_key
          name: New Secondary Key
  
  - type: horizontal-stack
    cards:
      - type: button
        name: Update from Secrets
        icon: mdi:key
        tap_action:
          action: call-service
          service: script.update_swedavia_keys
      - type: button
        name: Update from Input
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
2. Click "Get new keys" link
3. Copy keys from portal
4. Paste into input fields on dashboard
5. Click "Update from Input"
6. Done!

### Rotation Day
1. Get mobile notification
2. Tap "Get New Keys"
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
| Check status | View `sensor.{airport}_api_key_rotation` |

---

Choose the method that fits your workflow best! 🎯

**Recommended for most users:** Method 3 (Input Helper) with Method 4 (Complete Management Card)
