# Release Notes v1.2.1

**Release Date:** 2026-01-17

## 🐛 Bug Fix Release

### Fixed Issues

#### Config Flow API Key Reuse Bug
- **Problem**: När man lade till en andra flygplats krävdes API-nyckeln fortfarande som obligatorisk input, trots att integrationen skulle återanvända befintliga nycklar
- **Solution**: Fixat logiken i config flow så att befintliga API-nycklar nu korrekt sparas och återanvänds automatiskt
- **Impact**: Nu kan du lägga till flera flygplatser utan att behöva mata in API-nycklarna igen

### Technical Details

**Changed Files:**
- `custom_components/swedavia_flights/config_flow.py`
  - Fixed `async_step_user()` to properly store existing keys in `self._existing_api_keys`
  - Simplified `async_step_airport()` by removing unnecessary `existing_keys` parameter
  - Ensured keys are available when validating airport connection

**Workflow nu:**
1. **Första flygplatsen**: Ange API-nycklar → Välj flygplats ✅
2. **Andra flygplatsen**: Välj flygplats direkt (nycklar återanvänds automatiskt) ✅
3. **Tredje flygplatsen**: Välj flygplats direkt (nycklar återanvänds automatiskt) ✅

## 📦 Installation

### Uppgradera från v1.2.0

1. **Via HACS:**
   - Gå till HACS → Integrationer
   - Hitta "Swedavia Flight Information"
   - Klicka på "Update"
   - Starta om Home Assistant

2. **Manuellt:**
   ```bash
   cd custom_components/swedavia_flights
   git pull
   # Starta om Home Assistant
   ```

### Ny Installation

Se [README.md](README.md) för fullständiga installationsinstruktioner.

## ✅ Verification

Efter uppgradering, testa genom att:
1. Gå till Inställningar → Enheter & Tjänster
2. Klicka på "+ LÄGG TILL INTEGRATION"
3. Sök efter "Swedavia"
4. Du ska **inte** behöva mata in API-nycklar om du redan har en flygplats konfigurerad
5. Välj en ny flygplats och bekräfta att det fungerar

## 🔗 Related Documentation

- [KEY_ROTATION_QUICK_ACCESS.md](KEY_ROTATION_QUICK_ACCESS.md) - Enkla sätt att uppdatera API-nycklar
- [KEY_ROTATION_MANAGEMENT.md](KEY_ROTATION_MANAGEMENT.md) - Komplett rotation management guide
- [QUICK_SETUP.yaml](QUICK_SETUP.yaml) - Färdiga konfigurationsexempel

## 📝 Complete Changelog

### v1.2.1 (2026-01-17)
- 🐛 **FIX**: API keys now properly reused when adding multiple airports
- 📚 **DOCS**: Added quick access documentation for key rotation service

### v1.2.0 (2026-01-17)
- ✨ **NEW**: Key rotation sensor with automatic warnings
- ✨ **NEW**: `update_api_keys` service for runtime key updates
- ✨ **NEW**: Multi-step config flow with smart API key reuse
- ✨ **NEW**: Complete rotation schedule 2025-2030
- 📚 **DOCS**: Comprehensive key rotation management documentation

### v1.1.0 (2026-01-15)
- ✨ **NEW**: Baggage claim sensor for tracking baggage-only events

### v1.0.1 (2026-01-14)
- 🐛 **FIX**: Timezone-aware datetime handling
- 🐛 **FIX**: OptionsFlow configuration error

### v1.0.0 (2026-01-13)
- 🎉 **INITIAL**: First stable release
- ✨ API key authentication with automatic failover
- ✨ Support for all Swedish Swedavia airports
- ✨ Arrivals and departures sensors

## 🙏 Feedback

Om du hittar några problem eller har förslag, [skapa ett issue på GitHub](https://github.com/frodr1k/Swedavia_info/issues).

---

**Tack för att du använder Swedavia Flight Information!** ✈️
