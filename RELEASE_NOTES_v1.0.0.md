# Release Notes - v1.0.0

## 🎉 Initial Release

First release of Swedavia Flight Information integration for Home Assistant!

### Features

#### Core Functionality
- ✅ Full integration with Swedavia Flight Information API v2
- ✅ Support for all 12 Swedish Swedavia airports
- ✅ GUI configuration via config flow
- ✅ Automatic updates every 5 minutes
- ✅ Proper error handling and API rate limiting

#### Flight Information
- ✅ **Arrivals sensor** with comprehensive data:
  - Flight numbers including code-share flights
  - Airline information (name, IATA, ICAO codes)
  - Time information (scheduled, estimated, actual)
  - Status in Swedish
  - Terminal and gate information
  - Origin airport
  - **Baggage claim information**:
    - Belt/carousel number
    - First bag time (estimated and actual)
    - Last bag time
  - Flight remarks and notifications

- ✅ **Departures sensor** with comprehensive data:
  - Flight numbers including code-share flights
  - Airline information
  - Time information
  - Status in Swedish
  - Terminal and gate information
  - Destination airport
  - **Gate information**:
    - Gate action/status
    - Gate opening time
    - Gate closing time
  - **Check-in information**:
    - Check-in status
    - Check-in desk numbers (from/to)
  - Flight remarks and notifications

#### Configuration Options
- ✅ Select airport (12 Swedish airports available)
- ✅ Choose flight type (arrivals, departures, or both)
- ✅ Configurable time window:
  - Hours back (default: 2 hours)
  - Hours ahead (default: 24 hours)
- ✅ Options flow for adjusting time windows

#### Technical Features
- ✅ Async/await implementation
- ✅ DataUpdateCoordinator for efficient updates
- ✅ API rate limiting (minimum 1 second between requests)
- ✅ Proper error handling and logging
- ✅ Swedish and English translations
- ✅ HACS compatible
- ✅ GitHub Actions validation (Hassfest + HACS)

### Supported Airports

| IATA | Airport |
|------|---------|
| ARN | Stockholm Arlanda |
| BMA | Stockholm Bromma |
| GOT | Göteborg Landvetter |
| MMX | Malmö |
| LLA | Luleå |
| UME | Umeå |
| VBY | Visby |
| KRN | Kiruna |
| RNB | Ronneby |
| VST | Stockholm Västerås |
| ORB | Örebro |
| NYO | Stockholm Skavsta |

### Installation

#### Via HACS (Recommended)
1. Add custom repository: `https://github.com/frodr1k/Swedavia_info`
2. Install "Swedavia Flight Information"
3. Restart Home Assistant
4. Add integration via UI

#### Manual Installation
1. Copy `custom_components/swedavia_flights` to your config directory
2. Restart Home Assistant
3. Add integration via UI

### Usage Examples

See the [README.md](README.md) for detailed usage examples including:
- Lovelace cards for displaying flight information
- Automation examples for notifications
- Template examples for custom cards

### Known Limitations

- Maximum 50 flights displayed per sensor (API typically returns fewer)
- API updates every 5 minutes (configurable in future releases)
- Requires internet connection to Swedavia API

### API Information

- **Base URL**: https://api.swedavia.se/flightinfo/v2
- **Update Interval**: 5 minutes
- **Rate Limiting**: 1 second minimum between requests
- **Authentication**: None required (public API)

### Requirements

- Home Assistant 2023.1.0 or newer
- aiohttp >= 3.8.0

### Credits

- API provided by Swedavia
- Inspired by other Home Assistant flight tracking integrations
- Thanks to the Home Assistant community

### Support

- Report issues: [GitHub Issues](https://github.com/frodr1k/Swedavia_info/issues)
- Discussions: [GitHub Discussions](https://github.com/frodr1k/Swedavia_info/discussions)

---

**Full Changelog**: https://github.com/frodr1k/Swedavia_info/commits/v1.0.0
