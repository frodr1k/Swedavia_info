# Release Notes v1.5.0 - Smart Scheduler & Boost Mode

**Release Date:** 2026-01-20

> **⚠️ IMPORTANT:** Swedavia's API has a strict limit of **10,001 calls per 30 days**. This release includes smart scheduling and monitoring to ensure you stay within this limit.

## 🎉 New Features

### 1. Smart Update Scheduler ⚙️

Automatically optimizes update intervals based on your configuration to maximize update frequency while staying within API limits.

**Key Features:**
- **Adaptive intervals:** 5-30 minutes depending on configuration
- **Staggered updates:** Multiple airports update at different times
- **85% safety margin:** Leaves buffer for unexpected situations
- **Automatic optimization:** No manual configuration needed

**Examples:**
- Single airport, arrivals only: 10 min intervals
- Single airport, both types: 20 min intervals
- Two airports, both types: 25-30 min intervals (staggered)

### 2. Boost Mode ⚡

Temporarily increase update frequency to 2 minutes when you need real-time updates at the airport.

**Features:**
- **2-minute intervals:** Real-time gate and baggage updates
- **Configurable duration:** 1-12 hours (default: 4 hours)
- **Automatic shutoff:** Returns to normal schedule after duration
- **Persistent:** Survives Home Assistant restarts

**Services:**
```yaml
# Enable boost
service: swedavia_flights.enable_boost_mode
data:
  airport: "ARN"
  duration: 4

# Disable boost
service: swedavia_flights.disable_boost_mode
data:
  airport: "ARN"
```

**⚠️ WARNING:** Boost mode uses 7.5x more API calls. Recommended max 3-4 sessions per month.

### 3. Enhanced API Counter Sensor

New attributes for monitoring and scheduling:
- `total_airports`: Number of configured airports
- `update_interval_minutes`: Current update interval
- `calls_per_update`: API calls per update cycle
- `updates_per_day`: Total updates per day
- `estimated_daily_calls`: Estimated daily API usage
- `estimated_monthly_calls`: Estimated monthly API usage
- `estimated_usage_percentage`: Projected usage percentage

## 🔧 Technical Improvements

### New Files
- `boost_mode.py` - Boost mode manager
- `update_scheduler.py` - Smart scheduler implementation

### Modified Files
- `coordinator.py` - Dynamic interval adjustment, boost mode support
- `__init__.py` - Boost mode and scheduler initialization
- `sensor.py` - Enhanced API counter with schedule info
- `services.py` - New boost mode services
- `services.yaml` - Service definitions
- `README.md` - Comprehensive documentation (all info in one file)

### Removed Files
All separate documentation files consolidated into README.md:
- `API_COUNTER_DOCUMENTATION.md`
- `API_EFFICIENCY_ANALYSIS.md`
- `BOOST_MODE_DOCUMENTATION.md`
- `SMART_SCHEDULER_DOCUMENTATION.md`
- `SMART_SCHEDULER_SUMMARY.md`
- `IMPLEMENTATION_SUMMARY.md`

## 📊 API Usage Comparison

### Before v1.5.0
- Fixed 15-minute intervals
- One airport, both types: ~8,640 calls/month (86%)
- Two airports, both types: ~17,280 calls/month (❌ EXCEEDS LIMIT)

### After v1.5.0
- Dynamic intervals
- One airport, arrivals only: ~8,640 calls/month (86%)
- One airport, both types: ~8,640 calls/month (86%)
- Two airports, both types: ~8,448 calls/month (84%)

## 🚀 Upgrade Instructions

### From v1.4.0 to v1.5.0

1. **Update via HACS or manually**
2. **Restart Home Assistant**
3. **Check logs for schedule information:**
   ```
   === Swedavia Flight Info - Update Schedule ===
   Total airports configured: X
   Update interval: X minutes
   ...
   ```
4. **New services available:**
   - `swedavia_flights.enable_boost_mode`
   - `swedavia_flights.disable_boost_mode`

**No breaking changes** - all existing configurations will work with optimized intervals.

## 📝 Usage Examples

### Boost Mode Automation
```yaml
automation:
  - alias: "Auto Boost When At Airport"
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

### Boost Mode Button
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

### Monitor API Usage
```yaml
type: entities
title: API Usage & Schedule
entities:
  - entity: sensor.api_call_counter
  - type: attribute
    entity: sensor.api_call_counter
    attribute: update_interval_minutes
    name: Update Interval
    suffix: " min"
  - type: attribute
    entity: sensor.api_call_counter
    attribute: estimated_monthly_calls
    name: Est. Monthly Calls
```

## ⚠️ Important Notes

### API Limit Enforcement
- Swedavia **strictly enforces** 10,001 calls per 30 days
- Exceeding the limit results in 429 errors
- Monitor usage with `sensor.api_call_counter`

### Boost Mode Best Practices
✅ DO:
- Use only when at the airport
- Limit to 2-4 hours per session
- Maximum 3-4 boost sessions per month

❌ DON'T:
- Leave boost active overnight
- Activate for multiple airports simultaneously
- Use for daily monitoring

### Safety Margins
- Normal operation uses max 85% of API limit
- Leaves 15% buffer (~1,361 calls) for:
  - Boost mode sessions
  - Network retries
  - Unexpected situations

## 🐛 Bug Fixes

None - this is a feature release.

## 📚 Documentation

All documentation consolidated into README.md:
- ⚠️ API usage limits and warnings
- ⚙️ Smart update scheduler
- ⚡ Boost mode
- 📊 API counter sensor
- 🔧 Services
- 📝 Examples and best practices

English and Swedish sections available in single file.

## 🔮 Future Improvements

Potential features for future releases:
- UI configuration for safety margin
- Schedule-based updates (rush hour vs night)
- Priority airports
- Historical usage graphs
- Predictive analysis

## 🙏 Credits

Thank you to all users and testers!

Special thanks to Swedavia for providing an open API.

---

**Version:** 1.5.0  
**Compatibility:** Home Assistant 2024.1+  
**Breaking Changes:** None  
**Migration Required:** No
