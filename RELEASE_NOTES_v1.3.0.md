# Release Notes - v1.3.0

**Release Date:** 2026-01-17  
**Type:** Major Documentation & Internationalization Update  
**Breaking Changes:** Yes - Sensor names and states now in English

---

## 🌍 Major Language Update

This release converts the entire project to **English as the primary language**, following open source best practices.

### BREAKING CHANGES ⚠️

**Sensor Names Changed:**
- Old: `sensor.{airport}_api_nyckel_rotation`
- New: `sensor.{airport}_api_key_rotation`

**Sensor States Changed:**
- Old: `"Primär nyckel roteras IDAG!"`
- New: `"Primary key rotates TODAY!"`
- Old: `"OK - Nästa rotation om X dagar (primär)"`
- New: `"OK - Next rotation in X days (primary)"`

**Migration Required:**
- Update dashboard cards with new sensor entity IDs
- Update automations referencing sensor states
- Update any templates using the old Swedish strings

---

## 📝 What's Changed

### Python Code
- ✅ All log messages now in English
- ✅ All warning messages now in English  
- ✅ All sensor states now in English
- ✅ Sensor entity names now in English
- ✅ Config flow descriptions now in English

**Files Updated:**
- `sensor.py` - Sensor name: "API-nyckel rotation" → "API Key Rotation"
- `sensor.py` - All state strings: "roteras", "primär", "sekundär" → English
- `key_rotation.py` - Warning messages: Swedish → English
- `config_flow.py` - Description placeholders: Swedish → English

### Documentation
All user guides completely rewritten in English:

1. **README.md** - Bilingual (English primary, Swedish secondary)
   - Full English documentation first
   - Swedish summary section
   - Navigation links between languages

2. **info.md** (HACS) - Bilingual (English primary, Swedish secondary)
   - English first, Swedish second
   - Proper internationalization

3. **KEY_ROTATION_MANAGEMENT.md** - Fully updated to English
   - Updated all sensor names
   - Updated all example code
   - Updated all YAML examples

4. **KEY_ROTATION_QUICK_ACCESS.md** - Complete rewrite in English
   - 8 access methods
   - 456 lines of English documentation
   - All examples translated

5. **LOVELACE_BAGGAGE_EXAMPLES.md** - Complete rewrite in English
   - 7 card variants
   - 366 lines of English documentation
   - Installation guides

6. **BAGGAGE_NOTIFICATIONS.md** - Complete rewrite in English
   - 7 notification automation variants
   - 482 lines of English documentation
   - Complete setup examples

### UI Translations
- ✅ `translations/en.json` - Complete English translations
- ✅ `translations/sv.json` - Complete Swedish translations
- Users see UI in their selected Home Assistant language

---

## 🔄 Migration Guide

### Step 1: Update Dashboards

**Find and replace in your dashboard YAML:**

Old entity ID:
```yaml
sensor.stockholm_arlanda_api_nyckel_rotation
```

New entity ID:
```yaml
sensor.stockholm_arlanda_api_key_rotation
```

### Step 2: Update Automations

**Update state conditions:**

Old automation:
```yaml
condition:
  - condition: state
    entity_id: sensor.stockholm_arlanda_api_nyckel_rotation
    state: "Primär nyckel roteras IDAG!"
```

New automation:
```yaml
condition:
  - condition: state
    entity_id: sensor.stockholm_arlanda_api_key_rotation
    state: "Primary key rotates TODAY!"
```

**Or use template conditions (recommended):**
```yaml
condition:
  - condition: template
    value_template: >
      {{ 'rotation' in states('sensor.stockholm_arlanda_api_key_rotation').lower() 
         and 'OK' not in states('sensor.stockholm_arlanda_api_key_rotation') }}
```

### Step 3: Restart Home Assistant

After updating:
1. Check Developer Tools → States
2. Verify new sensor entity IDs exist
3. Test automations
4. Verify dashboard cards display correctly

---

## 📊 Statistics

- **Commits:** 3 language-related commits
- **Python files updated:** 3
- **Documentation files rewritten:** 4
- **Lines changed:** +585, -627 (net -42 lines, more concise)
- **Language coverage:** 100% English in code, bilingual docs

---

## 🎯 Benefits

1. **International Audience:** English-first makes integration accessible globally
2. **Open Source Standards:** Follows Home Assistant and HACS guidelines
3. **Better Maintainability:** Single language in code reduces complexity
4. **HACS Bronze Ready:** Meets all requirements for wider distribution
5. **Preserved Swedish UI:** Swedish users still see Swedish interface via translations

---

## 🐛 Bug Fixes

None - this is purely a language/documentation update.

---

## 📚 Documentation

All documentation now available in English:
- [README.md](README.md) - Bilingual setup guide
- [KEY_ROTATION_MANAGEMENT.md](KEY_ROTATION_MANAGEMENT.md) - Key rotation guide
- [KEY_ROTATION_QUICK_ACCESS.md](KEY_ROTATION_QUICK_ACCESS.md) - 8 easy access methods
- [LOVELACE_BAGGAGE_EXAMPLES.md](LOVELACE_BAGGAGE_EXAMPLES.md) - 7 card examples
- [BAGGAGE_NOTIFICATIONS.md](BAGGAGE_NOTIFICATIONS.md) - 7 notification automations
- [LANGUAGE_VERIFICATION.md](LANGUAGE_VERIFICATION.md) - Full language audit report

---

## ⚙️ Technical Details

### Sensor Entity ID Change
- **Pattern:** `sensor.{airport}_api_nyckel_rotation` → `sensor.{airport}_api_key_rotation`
- **Reason:** Consistency with English naming
- **Impact:** Manual update required in dashboards and automations

### State String Changes
All sensor states now use English:
- `"Primary key rotates TODAY!"` (was: "Primär nyckel roteras IDAG!")
- `"Primary key rotates tomorrow"` (was: "Primär nyckel roteras imorgon")
- `"Primary key rotates in X days"` (was: "Primär nyckel roteras om X dagar")
- `"Secondary key rotates TODAY!"` (was: "Sekundär nyckel roteras IDAG!")
- `"Secondary key rotates tomorrow"` (was: "Sekundär nyckel roteras imorgon")
- `"Secondary key rotates in X days"` (was: "Sekundär nyckel roteras om X dagar")
- `"OK - Next rotation in X days (primary)"` (was: "OK - Nästa rotation om X dagar (primär)")
- `"OK - Next rotation in X days (secondary)"` (was: "OK - Nästa rotation om X dagar (sekundär)")

### Log Message Changes
All warning messages now in English:
- `"⚠️ IMPORTANT: Your primary API key rotates TODAY!"`
- `"⚠️ WARNING: Your primary API key rotates TOMORROW..."`
- `"ℹ️ Reminder: Your primary API key will rotate in X days..."`

---

## 🔜 What's Next

- ✅ English-first documentation complete
- ✅ HACS Bronze requirements met
- 🔄 Submit to HACS default repository (pending)
- 🔄 Submit icons to Home Assistant Brands (pending)

---

## 💬 Feedback

If you encounter any issues with the language update or migration:
1. Check [LANGUAGE_VERIFICATION.md](LANGUAGE_VERIFICATION.md) for details
2. Open an issue on [GitHub](https://github.com/frodr1k/Swedavia_info/issues)
3. Include your Home Assistant version and error logs

---

## 👏 Contributors

- @frodr1k - Complete language update and documentation rewrite

---

## 📦 Installation

### Via HACS (Recommended)
1. Open HACS → Integrations
2. Search for "Swedavia Flight Information"
3. Click Install
4. Restart Home Assistant
5. Update dashboards and automations if upgrading from v1.2.x

### Manual Installation
1. Download latest release
2. Copy `custom_components/swedavia_flights` to your HA config
3. Restart Home Assistant
4. Add integration via UI

---

**Full Changelog:** [v1.2.1...v1.3.0](https://github.com/frodr1k/Swedavia_info/compare/v1.2.1...v1.3.0)

---

**⚠️ Important:** This is a breaking change release. Please review the migration guide above before upgrading.
