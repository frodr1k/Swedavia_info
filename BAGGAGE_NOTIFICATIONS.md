# Automatiska Notifieringar för Bagageutlämning

Guide för att få push-notiser till din mobil när väskor börjar komma ut från ett flyg.

## Förutsättningar

1. **Home Assistant Companion App** installerad på din mobil
   - [iOS App](https://apps.apple.com/app/home-assistant/id1099568401)
   - [Android App](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android)

2. **Bagagesensor** konfigurerad i Swedavia-integrationen
   - Du behöver ha valt **Ankomster** eller **Både** vid konfiguration

3. **Notifieringstjänst** konfigurerad
   - Sätts upp automatiskt när du kopplar mobil-appen

---

## Variant 1: Notifiera vid ALLA nya bagageband ⭐ Enklast

Denna automation skickar en notis varje gång ett nytt bagageband aktiveras.

```yaml
automation:
  - alias: "Notifiera när bagageband aktiveras"
    description: "Skicka notis när väskor börjar komma ut på ett band"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
        attribute: flights
    
    condition:
      # Kontrollera att det finns fler band som lämnar ut nu än tidigare
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
    
    action:
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat!"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Band {{ latest.baggage_claim_belt }} - Flight {{ latest.flight_number }}
            från {{ latest.arrival_airport_swedish }}
            
            {% if latest.baggage_claim_first_bag %}
            Första väska: {{ latest.baggage_claim_first_bag }}
            {% endif %}
          data:
            tag: "baggage_alert"
            group: "baggage"
            notification_icon: "mdi:bag-suitcase"
            color: "#2196F3"
            actions:
              - action: "VIEW_BAGGAGE"
                title: "Visa alla band"
```

**Byt ut:** `notify.mobile_app_din_telefon` mot namnet på din mobil-notifieringstjänst.

**Hitta namnet:**
1. Gå till **Developer Tools** → **Services**
2. Sök efter "notify"
3. Tjänsten heter något liknande: `notify.mobile_app_iphone_fredrik` eller `notify.mobile_app_samsung_galaxy`

---

## Variant 2: Notifiera för SPECIFIKT flyg

Om du väntar på ett specifikt flyg:

```yaml
automation:
  - alias: "Notifiera när mitt flyg får väskor"
    description: "Notis när mitt specifika flyg börjar lämna ut väskor"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
        attribute: flights
    
    variables:
      my_flight: "SK1425"  # Ändra till ditt flightnummer
    
    condition:
      # Kontrollera att vårt flyg finns och status ändrat till delivering
      - condition: template
        value_template: >
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set my_flight_data = new_flights | selectattr('flight_number', 'search', my_flight) | list %}
          {{ my_flight_data | length > 0 and 
             my_flight_data[0].baggage_claim_status == 'delivering' }}
      
      # Kontrollera att det INTE var delivering innan
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set old_flight_data = old_flights | selectattr('flight_number', 'search', my_flight) | list %}
          {{ old_flight_data | length == 0 or
             old_flight_data[0].baggage_claim_status != 'delivering' }}
    
    action:
      - service: notify.mobile_app_din_telefon
        data:
          title: "🎉 Ditt flyg {{ my_flight }} - väskor på väg!"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set my_flight_data = new_flights | selectattr('flight_number', 'search', my_flight) | first %}
            Bagageband: {{ my_flight_data.baggage_claim_belt }}
            Terminal: {{ my_flight_data.terminal }}
            
            {% if my_flight_data.baggage_claim_first_bag %}
            Första väska ute kl: {{ my_flight_data.baggage_claim_first_bag }}
            {% endif %}
            
            {% if my_flight_data.baggage_claim_last_bag %}
            Sista väska (est): {{ my_flight_data.baggage_claim_last_bag }}
            {% endif %}
          data:
            tag: "my_flight"
            group: "baggage"
            notification_icon: "mdi:airplane-landing"
            color: "#4CAF50"
            importance: "high"
            ttl: 0
            priority: high
            channel: "Baggage Alerts"
            actions:
              - action: "NAVIGATE_TERMINAL"
                title: "Navigera till terminal"
              - action: "DISMISS"
                title: "OK"
```

---

## Variant 3: Notifiera med LJUD och VIBRATION

För att inte missa när väskorna kommer:

```yaml
automation:
  - alias: "Notifiera med ljud - bagageband"
    description: "Notis med ljud och vibration när väskor börjar komma ut"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
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
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat!"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Band {{ latest.baggage_claim_belt }} - {{ latest.flight_number }}
          data:
            tag: "baggage_urgent"
            group: "baggage"
            notification_icon: "mdi:bag-suitcase"
            color: "#FF5722"
            importance: "high"
            ttl: 0
            priority: high
            
            # Android-specifikt
            channel: "Baggage Alerts"
            vibrationPattern: "100, 1000, 100, 1000, 100"
            ledColor: "blue"
            
            # iOS-specifikt
            sound: 
              name: "default"
              critical: 1
              volume: 1.0
            
            # Gemensamt
            actions:
              - action: "VIEW_BAGGAGE"
                title: "Visa band"
              - action: "SNOOZE_10"
                title: "Påminn om 10 min"
```

---

## Variant 4: Notifiera med POSITION/GEO-fence

Skicka bara notis om du är nära flygplatsen:

```yaml
automation:
  - alias: "Notifiera baggage när på plats"
    description: "Notis om baggage endast när du är på flygplatsen"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
        attribute: flights
    
    condition:
      # Kolla att fler band är aktiva
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
      
      # Kolla att du är på eller nära Arlanda
      - condition: zone
        entity_id: person.fredrik  # Ändra till din person-entity
        zone: zone.arlanda  # Skapa en zon för flygplatsen
    
    action:
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat!"
          message: "Du är på Arlanda - väskor börjar komma ut!"
          data:
            tag: "baggage_location"
            group: "baggage"
```

**För att skapa zon:**
1. Gå till **Inställningar** → **Områden och zoner**
2. Klicka **Lägg till zon**
3. Namn: "Arlanda"
4. Sätt markör på flygplatsen
5. Radie: 1000 meter

---

## Variant 5: Med TTS (Text-to-Speech) hemma

Spela upp meddelande hemma via högtalare:

```yaml
automation:
  - alias: "Meddela baggage via TTS"
    description: "Spela upp meddelande om baggage via högtalare"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
        attribute: flights
    
    condition:
      - condition: template
        value_template: >
          {% set old_flights = trigger.from_state.attributes.flights | default([]) %}
          {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
          {% set old_delivering = old_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {% set new_delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list | length %}
          {{ new_delivering > old_delivering }}
      
      # Spela bara upp om någon är hemma
      - condition: state
        entity_id: group.family
        state: "home"
    
    action:
      # Push-notis
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat"
          message: "Väskor börjar komma ut"
      
      # TTS hemma
      - service: tts.google_translate_say
        data:
          entity_id: media_player.vardagsrum
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Bagageband {{ latest.baggage_claim_belt }} är aktiverat. 
            Flight {{ latest.flight_number }} från {{ latest.arrival_airport_swedish }}. 
            Väskor börjar komma ut nu.
          language: "sv"
```

---

## Variant 6: Med actionable notifications

Notis med knappar för olika åtgärder:

```yaml
automation:
  - alias: "Baggage notis med actions"
    description: "Notis med actionable buttons"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
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
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Band {{ latest.baggage_claim_belt }} - {{ latest.flight_number }}
          data:
            tag: "baggage_action"
            group: "baggage"
            actions:
              - action: "OPEN_MAP"
                title: "📍 Navigera"
              - action: "CALL_TAXI"
                title: "🚕 Ring taxi"
              - action: "REMIND_10"
                title: "⏰ Påminn om 10 min"
              - action: "DISMISS"
                title: "✓ OK"

  # Hantera action: Navigera
  - alias: "Baggage action - Navigera"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "OPEN_MAP"
    action:
      - service: notify.mobile_app_din_telefon
        data:
          message: "command_broadcast_intent"
          data:
            intent_package_name: "com.google.android.apps.maps"
            intent_action: "android.intent.action.VIEW"
            intent_uri: "geo:59.651667,17.918611?q=Stockholm+Arlanda+Airport"

  # Hantera action: Påminn om 10 min
  - alias: "Baggage action - Påminn"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "REMIND_10"
    action:
      - delay: "00:10:00"
      - service: notify.mobile_app_din_telefon
        data:
          title: "⏰ Påminnelse: Bagageband"
          message: "Dina väskor borde vara ute nu!"
```

---

## Variant 7: Persistent notification + Push

Både på mobil och i Home Assistant:

```yaml
automation:
  - alias: "Baggage - Dubbel notis"
    description: "Notis både på mobil och i HA"
    
    trigger:
      - platform: state
        entity_id: sensor.stockholm_arlanda_ankomster_bagage
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
      # Push till mobil
      - service: notify.mobile_app_din_telefon
        data:
          title: "🛄 Bagageband aktiverat"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Band {{ latest.baggage_claim_belt }} - {{ latest.flight_number }}
      
      # Persistent notification i HA
      - service: notify.persistent_notification
        data:
          title: "🛄 Bagageband aktiverat"
          message: >
            {% set new_flights = trigger.to_state.attributes.flights | default([]) %}
            {% set delivering = new_flights | selectattr('baggage_claim_status', 'eq', 'delivering') | list %}
            {% set latest = delivering | last %}
            Band {{ latest.baggage_claim_belt }} - Flight {{ latest.flight_number }}
            från {{ latest.arrival_airport_swedish }}
            
            {% if latest.baggage_claim_first_bag %}
            Första väska: {{ latest.baggage_claim_first_bag }}
            {% endif %}
          notification_id: "baggage_latest"
```

---

## Installation

1. **Kopiera koden** för den variant du vill ha
2. Gå till **Inställningar** → **Automationer & scener**
3. Klicka **Skapa automation** → **Starta med tomt**
4. Klicka på **⋮** → **Redigera i YAML**
5. **Klistra in** koden
6. **Ändra** `entity_id` och `notify.mobile_app_din_telefon`
7. **Spara**

### Hitta din notify-tjänst:

```yaml
# Developer Tools → Services → Sök "notify"
# Välj en tjänst och testa:

service: notify.mobile_app_iphone_fredrik
data:
  title: "Test"
  message: "Funkar det?"
```

---

## Felsökning

### "Får inga notiser"
- Kontrollera att mobil-appen är inloggad
- Testa notify-tjänsten manuellt i Developer Tools
- Kolla att notiser är tillåtna i mobilens inställningar

### "Notiser kommer för sent"
- Sensorn uppdateras var 5:e minut
- Du kan inte få notiser snabbare än API:et uppdateras

### "Får notis för alla flyg"
- Använd Variant 2 med specifikt flightnummer
- Lägg till condition för att filtrera

### "Automation triggar inte"
- Kontrollera att bagagesensorn existerar
- Kolla att `attribute: flights` är rätt stavat
- Verifiera conditions i Developer Tools → Template

---

## Tips

- **Testa först** med en persistent notification innan du använder push
- **Använd tag** för att gruppera relaterade notiser
- **Lägg till actions** för snabb interaktion
- **Kombinera med geo-fence** för smart notis
- **Spara notification_id** för att uppdatera samma notis

---

**Rekommendation:** Börja med **Variant 1** för att testa, sedan uppgradera till **Variant 3** eller **Variant 6** för bästa upplevelse! 🎯
