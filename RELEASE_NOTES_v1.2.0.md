# Release Notes - v1.2.0

## 🎉 Major Update: Key Rotation Management

### New Features

#### 🔑 Automated Key Rotation System

**1. Key Rotation Sensor**

A new diagnostic sensor that monitors API key rotation status!

- **Entity**: `sensor.{airport}_api_nyckel_rotation`
- **Updates**: Real-time monitoring of rotation schedule
- **Icon Changes**: Visual indication of urgency
  - 🔑 `mdi:key-chain` - Normal (>3 days)
  - 🔓 `mdi:key-remove` - Warning (1-3 days)
  - ⚠️ `mdi:key-alert` - Critical (today)

**Sensor States:**
- `OK - Nästa rotation om X dagar (primär/sekundär)` - Normal operation
- `Primär/Sekundär nyckel roteras om X dagar` - Warning period
- `Primär/Sekundär nyckel roteras IDAG!` - Rotation day

**Attributes Include:**
- `primary_key_next_rotation`: Next primary key rotation date
- `primary_key_days_until`: Days until primary key rotation
- `primary_key_warning`: Warning message (if active)
- `secondary_key_next_rotation`: Next secondary key rotation date
- `secondary_key_days_until`: Days until secondary key rotation  
- `secondary_key_warning`: Warning message (if active)
- `update_service`: Service name for updating keys
- `developer_portal`: Link to get new keys

**2. Automatic Warning System**

Proactive warnings to prevent service interruption!

- **Warning Period**: 3 days before rotation
- **Check Frequency**: Every 6 hours
- **Warning Locations**:
  - Home Assistant logs (WARNING level)
  - Key rotation sensor state
  - Sensor attributes

**Warning Messages:**
- 3 days before: "ℹ️ Påminnelse: Din primär API-nyckel kommer att roteras om 3 dagar..."
- 1 day before: "⚠️ VARNING: Din primär API-nyckel roteras IMORGON..."
- Rotation day: "⚠️ VIKTIGT: Din primär API-nyckel roteras IDAG!"

**3. Update Service**

Easily update API keys without reconfiguring!

**Service**: `swedavia_flights.update_api_keys`

**Parameters:**
- `api_key` (optional): New primary subscription key
- `api_key_secondary` (optional): New secondary subscription key

**Example:**
```yaml
service: swedavia_flights.update_api_keys
data:
  api_key: "your_new_primary_key"
  api_key_secondary: "your_new_secondary_key"
```

**Benefits:**
- Updates all Swedavia integrations at once
- Automatically reloads integrations
- No need to reconfigure through UI
- Perfect for automations

#### 🔄 Smart API Key Reuse

Simplified configuration for multiple airports!

**How it works:**
1. First integration: Enter API keys
2. Additional integrations: Keys automatically reused!
3. No need to re-enter keys for each airport

**User Experience:**
- Two-step config flow: API keys → Airport selection
- Shows friendly message: "✅ Återanvänder API-nycklar från befintlig integration"
- Reduces configuration time
- Ensures consistency across integrations

**Benefits:**
- One-time API key entry
- Manage multiple airports easily
- Less risk of typos
- Cleaner configuration process

### Complete Rotation Schedule (2025-2030)

#### Primary Key Rotations (April)
- 2025-04-09
- 2026-04-08
- 2027-04-07
- 2028-04-12
- 2029-04-11
- 2030-04-10

#### Secondary Key Rotations (October)
- 2025-10-03
- 2026-10-02
- 2027-10-01
- 2028-10-06
- 2029-10-05
- 2030-10-03

### Usage Examples

#### Dashboard Monitoring

```yaml
type: entities
title: API-nyckel Status
entities:
  - entity: sensor.stockholm_arlanda_api_nyckel_rotation
    name: Rotation Status
```

#### Automation for Notifications

```yaml
automation:
  - alias: "Notifiera om API-nyckel rotation"
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
          title: "⚠️ Swedavia API-nyckel behöver uppdateras"
          message: "{{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}"
```

#### Detailed Status Card

```yaml
type: markdown
content: |
  ## 🔑 API-nyckel Rotation
  
  **Status:** {{ states('sensor.stockholm_arlanda_api_nyckel_rotation') }}
  
  ### Primär Nyckel
  - Nästa rotation: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_next_rotation')[:10] }}
  - Dagar kvar: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'primary_key_days_until') }}
  
  ### Sekundär Nyckel
  - Nästa rotation: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_next_rotation')[:10] }}
  - Dagar kvar: {{ state_attr('sensor.stockholm_arlanda_api_nyckel_rotation', 'secondary_key_days_until') }}
  
  [Hämta nya nycklar](https://apideveloper.swedavia.se/)
```

### Configuration Workflow

**First Airport:**
1. Add Integration → "Swedavia Flight Information"
2. **Step 1**: Enter API keys (primary + secondary)
3. **Step 2**: Select airport and flight type
4. Done!

**Additional Airports:**
1. Add Integration → "Swedavia Flight Information"
2. ✅ Message: "Återanvänder API-nycklar från befintlig integration"
3. **Step 1**: Select airport and flight type (API keys skipped!)
4. Done!

### Technical Implementation

**New Files:**
- `key_rotation.py`: Rotation schedule and warning logic
- `services.py`: Service definitions and handlers
- `services.yaml`: Service documentation
- `KEY_ROTATION_MANAGEMENT.md`: Complete management guide

**Modified Files:**
- `__init__.py`: Service setup and periodic warning checks
- `sensor.py`: New key rotation sensor
- `config_flow.py`: Multi-step flow with key reuse
- `translations/`: Updated Swedish and English translations

### Documentation

**New Guide:** [KEY_ROTATION_MANAGEMENT.md](KEY_ROTATION_MANAGEMENT.md)

Complete documentation including:
- Detailed feature explanations
- Usage workflows
- Automation examples
- Dashboard cards
- Troubleshooting guide
- Best practices

### Performance

- **No additional API calls**: Rotation logic is local
- **Minimal overhead**: 6-hour check interval
- **Efficient service**: Updates all integrations in one call
- **Smart caching**: Keys reused across config flows

### Upgrade Notes

**Automatic Changes:**
1. New sensor appears for each integration: `sensor.{airport}_api_nyckel_rotation`
2. Warning system starts automatically
3. Service `swedavia_flights.update_api_keys` becomes available

**No Action Required:**
- Existing configurations continue to work
- No need to reconfigure
- Warnings will start appearing if rotation is near

**Recommended Actions:**
1. Add key rotation sensor to your dashboard
2. Set up notification automation
3. Note next rotation dates from sensor attributes
4. Configure both primary and secondary keys for failover

### Breaking Changes

None! Fully backwards compatible.

### Bug Fixes

No bugs fixed in this release (feature-only update).

### Known Limitations

- Rotation schedule hard-coded (2025-2030)
- Update service affects all integrations (by design)
- Warning frequency cannot be customized (6 hours)

### Future Enhancements

Potential improvements for future versions:
- Binary sensor for "rotation imminent"
- Event triggers for rotation milestones
- Configurable warning thresholds
- API to fetch rotation schedule dynamically

---

**Full Changelog**: v1.1.0...v1.2.0

**GitHub Release**: https://github.com/frodr1k/Swedavia_info/releases/tag/v1.2.0
