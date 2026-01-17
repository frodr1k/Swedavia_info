# Automatic Notifications for Baggage Delivery

Guide to receive push notifications on your mobile when bags start arriving from a flight.

## Prerequisites

1. **Home Assistant Companion App** installed on your mobile
   - [iOS App](https://apps.apple.com/app/home-assistant/id1099568401)
   - [Android App](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android)

2. **Baggage sensor** configured in Swedavia integration
   - You need to have selected **Arrivals** or **Both** during configuration

3. **Notification service** configured
   - Set up automatically when you connect the mobile app

---

## Variant 1: Notify on ALL New Baggage Belts ⭐ Simplest

This automation sends a notification every time a new baggage belt is activated.

```yaml
automation:
  - alias: "Notify When Baggage Belt Activated"
    description: "Send notification when bags start arriving on a belt"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      # Check that there are more belts delivering now than before
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🛄 Baggage Belt Activated!"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Belt {{ latest.baggage_claim_belt }} - Flight {{ latest.flight_number }}
            from {{ latest.arrival_airport_swedish }}
            
            {% if latest.baggage_claim_first_bag %}
            First bag: {{ latest.baggage_claim_first_bag }}
            {% endif %}
          data:
            tag: "baggage_alert"
            group: "baggage"
            notification_icon: "mdi:bag-suitcase"
            color: "#2196F3"
            actions:
              - action: "VIEW_BAGGAGE"
                title: "View All Belts"
```

**Replace:** `notify.mobile_app_your_phone` with your mobile notification service name.

**Find the name:**
1. Go to **Developer Tools** → **Services**
2. Search for "notify"
3. The service is named something like: `notify.mobile_app_iphone_fredrik` or `notify.mobile_app_samsung_galaxy`

---

## Variant 2: Notify for SPECIFIC Flight

If you're waiting for a specific flight:

```yaml
automation:
  - alias: "Notify When My Flight Gets Bags"
    description: "Notification when my specific flight starts delivering bags"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    variables:
      my_flight: "SK1425"  # Change to your flight number
    
    condition:
      # Check that our flight exists and status changed to delivering
      - condition: template
        value_template: >
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set my_flight_data = new_flights | selectattr('flight_number', 'search', my_flight) | list %}
          {{ my_flight_data | length > 0 and 
             my_flight_data[0].baggage_claim_status == 'delivering' }}
    
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🎉 Your Flight's Bags Are Here!"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set my_flight_data = new_flights | selectattr('flight_number', 'search', my_flight) | list | first %}
            Flight {{ my_flight }} from {{ my_flight_data.arrival_airport_swedish }}
            
            Belt: {{ my_flight_data.baggage_claim_belt }}
            {% if my_flight_data.baggage_claim_first_bag %}
            First bag: {{ my_flight_data.baggage_claim_first_bag }}
            {% endif %}
          data:
            tag: "my_flight_baggage"
            notification_icon: "mdi:airplane-landing"
            color: "#4CAF50"
            actions:
              - action: "NAVIGATE"
                title: "Navigate to Airport"
                uri: "geo:0,0?q={{ state_attr('sensor.stockholm_arlanda_arrivals_baggage', 'airport_name') }}"
```

**Perfect for:** Picking someone up from the airport

---

## Variant 3: Multiple Notification Services

Send to multiple phones simultaneously:

```yaml
automation:
  - alias: "Notify Family of Baggage Delivery"
    description: "Notify all family members when bags arrive"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      # Send to person 1
      - service: notify.mobile_app_iphone_mom
        data:
          title: "🛄 Baggage Arriving"
          message: "Bags starting to arrive at baggage claim"
      
      # Send to person 2
      - service: notify.mobile_app_android_dad
        data:
          title: "🛄 Baggage Arriving"
          message: "Bags starting to arrive at baggage claim"
      
      # Send to person 3
      - service: notify.mobile_app_tablet
        data:
          title: "🛄 Baggage Arriving"
          message: "Bags starting to arrive at baggage claim"
```

---

## Variant 4: Notification with Action Buttons

Advanced notification with interactive buttons:

```yaml
automation:
  - alias: "Baggage Alert with Actions"
    description: "Baggage notification with action buttons"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🛄 Baggage Belt Active"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Flight {{ latest.flight_number }} - Belt {{ latest.baggage_claim_belt }}
          data:
            tag: "baggage_action"
            group: "baggage"
            notification_icon: "mdi:bag-suitcase"
            color: "#2196F3"
            actions:
              - action: "VIEW_DASHBOARD"
                title: "View Dashboard"
                uri: "/lovelace/airport"
              - action: "NAVIGATE_AIRPORT"
                title: "Navigate"
                uri: "geo:59.651944,17.918611"  # Arlanda coordinates
              - action: "DISMISS"
                title: "Dismiss"
                destructive: true
```

**Buttons do:**
- **View Dashboard**: Opens your airport dashboard in HA app
- **Navigate**: Opens Maps app with directions to airport
- **Dismiss**: Removes notification

---

## Variant 5: Time-Limited Notifications

Only notify during specific hours (e.g., when picking someone up):

```yaml
automation:
  - alias: "Baggage Notification - Time Limited"
    description: "Only notify between 14:00-16:00"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      # Only between 14:00 and 16:00
      - condition: time
        after: "14:00:00"
        before: "16:00:00"
      
      # And new bags are being delivered
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🛄 Expected Flight - Bags Arriving"
          message: "Bags are being delivered at the expected time!"
          data:
            tag: "expected_baggage"
            notification_icon: "mdi:bag-checked"
            color: "#4CAF50"
```

**Perfect for:** When you're picking someone up and only want alerts around their arrival time

---

## Variant 6: Notification with Image/Camera

If you have a camera at the airport or want to include an image:

```yaml
automation:
  - alias: "Baggage Notification with Camera"
    description: "Send notification with camera snapshot"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      # Take camera snapshot first
      - service: camera.snapshot
        target:
          entity_id: camera.airport_baggage_area
        data:
          filename: "/config/www/snapshots/baggage_snapshot.jpg"
      
      # Wait for snapshot to be saved
      - delay:
          seconds: 2
      
      # Send notification with image
      - service: notify.mobile_app_your_phone
        data:
          title: "🛄 Baggage Arriving"
          message: "Check the camera feed"
          data:
            image: "/local/snapshots/baggage_snapshot.jpg"
            tag: "baggage_camera"
            notification_icon: "mdi:camera"
```

**Requires:**
- Camera entity configured
- `www/snapshots/` folder created in config directory

---

## Variant 7: Critical Alert (iOS)

For important pickups, use iOS critical alerts (bypass Do Not Disturb):

```yaml
automation:
  - alias: "Critical Baggage Alert (iOS)"
    description: "Critical notification that bypasses DND"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    variables:
      important_flight: "SK1425"
    
    condition:
      - condition: template
        value_template: >
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set my_flight_data = new_flights | selectattr('flight_number', 'search', important_flight) | list %}
          {{ my_flight_data | length > 0 and 
             my_flight_data[0].baggage_claim_status == 'delivering' }}
    
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "🚨 IMPORTANT: Flight Bags Arriving"
          message: >
            Flight {{ important_flight }} bags are now being delivered!
            Belt: {{ (new_flights | selectattr('flight_number', 'search', important_flight) | list | first).baggage_claim_belt }}
          data:
            push:
              sound:
                name: "default"
                critical: 1
                volume: 1.0
            tag: "critical_baggage"
            group: "baggage"
```

**iOS Only** - Critical alerts require special permission in iOS settings

---

## Complete Example - All Features Combined

```yaml
automation:
  - alias: "Complete Baggage Notification"
    description: "Full-featured baggage notification system"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_arrivals_baggage
        attribute: flights
    
    condition:
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      # Calculate new belt info
      - variables:
          new_belt: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {{ delivering | last }}
      
      # Send rich notification
      - service: notify.mobile_app_your_phone
        data:
          title: "🛄 Baggage Belt {{ new_belt.baggage_claim_belt }} Active"
          message: >
            **Flight {{ new_belt.flight_number }}**
            From: {{ new_belt.arrival_airport_swedish }}
            
            {% if new_belt.baggage_claim_first_bag %}
            Started: {{ new_belt.baggage_claim_first_bag }}
            {% endif %}
            {% if new_belt.baggage_claim_last_bag %}
            Expected end: {{ new_belt.baggage_claim_last_bag }}
            {% endif %}
          data:
            tag: "baggage_{{ new_belt.baggage_claim_belt }}"
            group: "airport_baggage"
            notification_icon: "mdi:bag-suitcase"
            color: "#2196F3"
            ttl: 0
            priority: high
            actions:
              - action: "VIEW_DASHBOARD"
                title: "View All Belts"
                uri: "/lovelace/airport"
              - action: "NAVIGATE"
                title: "Navigate to Airport"
                uri: "geo:59.651944,17.918611"
              - action: "SNOOZE"
                title: "Remind in 5 min"
              - action: "DISMISS"
                title: "Dismiss"
                destructive: true
      
      # Log to Home Assistant
      - service: logbook.log
        data:
          name: "Baggage Notification"
          message: "Sent notification for belt {{ new_belt.baggage_claim_belt }}"
          entity_id: sensor.stockholm_arlanda_arrivals_baggage
```

---

## Troubleshooting

### Notification not arriving
- Check notification service name is correct
- Verify mobile app is connected to Home Assistant
- Test notification service in Developer Tools → Services
- Check mobile app notification permissions

### Too many notifications
- Add cooldown with `mode: single` and `max_exceeded: silent`
- Use condition to filter specific flights
- Add time restrictions with `condition: time`

### Notification delayed
- Check Home Assistant is running
- Verify sensor updates every 5 minutes
- Consider using `ttl: 0` for immediate delivery

### Action buttons not working
- Verify action names match in notification and automation
- Check URI syntax for navigation
- iOS and Android have different action capabilities

---

## Tips & Best Practices

1. **Replace entity names**: Change `stockholm_arlanda` to your airport
2. **Test first**: Use Developer Tools → Services to test notifications
3. **Cooldown period**: Add `mode: single` to prevent spam
4. **Battery friendly**: Don't use critical alerts unless necessary
5. **Combine with Lovelace**: See [LOVELACE_BAGGAGE_EXAMPLES.md](LOVELACE_BAGGAGE_EXAMPLES.md)
6. **Location services**: Enable for "Navigate" buttons to work

---

**Recommended starter:** Begin with Variant 1 (notify on all belts), then customize to Variant 2 (specific flight) when picking someone up.
