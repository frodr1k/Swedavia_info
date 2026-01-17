# API Key Rotation Management

> **⚡ Quick Access:** Looking for easy ways to update keys? See [KEY_ROTATION_QUICK_ACCESS.md](KEY_ROTATION_QUICK_ACCESS.md) for ready-to-use dashboard buttons, scripts, and automation examples!

## Overview

Swedavia rotates API keys every 6 months for security. This integration includes automated warning systems and tools to manage key rotation seamlessly.

## Features

### 🔔 Automatic Warnings

- **Warning Period**: 3 days before rotation
- **Check Frequency**: Every 6 hours
- **Warning Locations**:
  - Home Assistant logs
  - Key Rotation sensor state
  - Sensor attributes

### 📊 Key Rotation Sensor

A dedicated sensor (`sensor.{airport}_api_key_rotation`) that monitors key rotation status.

**Sensor States:**
- `OK - Next rotation in X days (primary/secondary)` - Normal operation
- `Primary/Secondary key rotates in X days` - Warning period (≤3 days)
- `Primary/Secondary key rotates TODAY!` - Rotation day

**Sensor Icon Changes:**
- 🔑 `mdi:key-chain` - Normal (>3 days)
- 🔓 `mdi:key-remove` - Warning (1-3 days)  
- ⚠️ `mdi:key-alert` - Critical (today)

**Attributes:**
```yaml
primary_key_next_rotation: "2026-04-08T00:00:00+00:00"
primary_key_days_until: 82
primary_key_warning: null
secondary_key_next_rotation: "2026-10-02T00:00:00+00:00"
secondary_key_days_until: 259
secondary_key_warning: null
update_service: "swedavia_flights.update_api_keys"
developer_portal: "https://apideveloper.swedavia.se/"
```

### 🛠️ Update Service

Update API keys without reconfiguring the integration.

**Service**: `swedavia_flights.update_api_keys`

**Parameters:**
- `api_key` (optional): New primary key
- `api_key_secondary` (optional): New secondary key

**Example Service Call:**
```yaml
service: swedavia_flights.update_api_keys
data:
  api_key: "new_primary_key_here"
  api_key_secondary: "new_secondary_key_here"
```

**What it does:**
1. Updates API keys for all Swedavia Flight Information integrations
2. Automatically reloads integrations with new keys
3. Logs success/failure to Home Assistant logs

## Rotation Schedule 2025-2030

### Primary Key Rotations (April)
| Date | Action |
|------|--------|
| 2025-04-09 | Update before this date |
| 2026-04-08 | Update before this date |
| 2027-04-07 | Update before this date |
| 2028-04-12 | Update before this date |
| 2029-04-11 | Update before this date |
| 2030-04-10 | Update before this date |

### Secondary Key Rotations (October)
| Date | Action |
|------|--------|
| 2025-10-03 | Update before this date |
| 2026-10-02 | Update before this date |
| 2027-10-01 | Update before this date |
| 2028-10-06 | Update before this date |
| 2029-10-05 | Update before this date |
| 2030-10-03 | Update before this date |

## Usage Workflows

### Workflow 1: Proactive Key Update (Recommended)

**3 days before rotation:**

1. **Check sensor**: `sensor.stockholm_arlanda_api_key_rotation`
2. **See warning** in Home Assistant logs (every 6 hours)
3. **Get new key** from https://apideveloper.swedavia.se/
4. **Update via service**:
   ```yaml
   service: swedavia_flights.update_api_keys
   data:
     api_key: "your_new_primary_key"  # or api_key_secondary
   ```
5. **Verify**: Check logs for success message

### Workflow 2: Automatic Failover (Dual Keys)

If you have both keys configured:

1. **Primary key expires** → Automatic failover to secondary
2. **Warning logged**: "Primary API key failed (401), trying secondary key"
3. **Update expired key** at your convenience using the service
4. **System continues** without downtime

### Workflow 3: Automation-Based Update

Create an automation to notify you:

```yaml
automation:
  - alias: "API Key Rotation Notification"
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
          title: "⚠️ Swedavia API Key Needs Update"
          message: >
            {{ states('sensor.stockholm_arlanda_api_key_rotation') }}
            
            Get new key from: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'developer_portal') }}
            
            Update with service: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'update_service') }}
```

### Workflow 4: Dashboard Card

Monitor rotation status on your dashboard:

```yaml
type: entities
title: API Key Status
entities:
  - entity: sensor.stockholm_arlanda_api_key_rotation
    name: Rotation Status
    icon: mdi:key-chain
```

Or detailed card:

```yaml
type: markdown
content: |
  ## 🔑 API Key Rotation
  
  **Status:** {{ states('sensor.stockholm_arlanda_api_key_rotation') }}
  
  ### Primary Key
  - Next rotation: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_next_rotation')[:10] }}
  - Days remaining: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'primary_key_days_until') }}
  
  ### Secondary Key
  - Next rotation: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_next_rotation')[:10] }}
  - Days remaining: {{ state_attr('sensor.stockholm_arlanda_api_key_rotation', 'secondary_key_days_until') }}
  
  ---
  
  [Get new keys](https://apideveloper.swedavia.se/)
```

## Log Messages

### Warning Messages (3 days before)

**3 days before:**
```
ℹ️ Reminder: Your primary API key will rotate in 3 days (2026-04-08). 
Prepare by getting new key from https://apideveloper.swedavia.se/
```

**1 day before:**
```
⚠️ WARNING: Your primary API key rotates TOMORROW (2026-04-08)! 
Update your key from https://apideveloper.swedavia.se/
```

**Rotation day:**
```
⚠️ IMPORTANT: Your primary API key rotates TODAY! 
Update your key from https://apideveloper.swedavia.se/ to avoid service interruption.
```

### Service Success Messages

```
INFO: Updated primary API key for Stockholm Arlanda
INFO: Successfully updated API keys for 1 integration(s)
```

## Best Practices

### ✅ Do's

1. **Configure both keys**: Primary + Secondary for automatic failover
2. **Monitor the sensor**: Add to your main dashboard
3. **Set up notifications**: Get alerted before rotation
4. **Update proactively**: Don't wait until expiry day
5. **Use the service**: Easier than reconfiguring integration

### ❌ Don'ts

1. **Don't ignore warnings**: Update keys when prompted
2. **Don't wait until expiry**: Update within the 3-day warning window
3. **Don't reconfigure**: Use the update service instead
4. **Don't use only one key**: Always configure both for failover

## Troubleshooting

### Sensor shows "OK" but I see 401 errors

**Solution**: Your key may have already expired. Update immediately:
```yaml
service: swedavia_flights.update_api_keys
data:
  api_key: "new_key_from_portal"
```

### Service not updating keys

**Check:**
1. Service call syntax is correct
2. At least one key provided
3. Check Home Assistant logs for error messages
4. Verify keys are valid on developer portal

### No warnings appearing

**Check:**
1. Sensor `sensor.{airport}_api_key_rotation` exists
2. Check Home Assistant logs (warnings appear every 6 hours)
3. Verify current date relative to rotation schedule

### Both keys expired

**Solution**:
1. Get fresh keys from https://apideveloper.swedavia.se/
2. Call update service with both keys:
   ```yaml
   service: swedavia_flights.update_api_keys
   data:
     api_key: "new_primary_key"
     api_key_secondary: "new_secondary_key"
   ```

## Technical Details

### Warning Check Frequency

- **Initial check**: When integration loads
- **Recurring checks**: Every 6 hours
- **Warning threshold**: 3 days before rotation

### Service Behavior

1. Validates at least one key provided
2. Updates all Swedavia integration config entries
3. Reloads each integration with new keys
4. Logs success/failure per integration

### Rotation Data Source

Hard-coded schedule from Swedavia's key rotation policy (2025-2030). Dates are stored in `key_rotation.py`.

## Developer Portal

Get your API keys: https://apideveloper.swedavia.se/

**Steps:**
1. Log in to portal
2. Go to **Profile** → **Subscriptions**
3. Select **FlightInfo** subscription
4. Copy **Primary key** and **Secondary key**
5. Use update service to add them to integration

---

**Note**: This rotation schedule is based on Swedavia's published rotation policy. If Swedavia changes their schedule, update `key_rotation.py` with new dates.
