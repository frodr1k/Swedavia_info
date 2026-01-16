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
- ✅ **Dual API key support** (primary + secondary)
- ✅ **Automatic failover** between keys on HTTP 401 errors
- ✅ **Key rotation support** with zero downtime

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
- ✅ **Automatic API key failover** (primary → secondary on errors)
- ✅ **Key rotation ready** with dual key configuration

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

#### Prerequisites
1. Register at https://apideveloper.swedavia.se/
2. Subscribe to FlightInfo API (free)
3. Copy your **Primary key** and **Secondary key**

**💡 Tip**: Using both keys provides automatic failover during key rotation!

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
- **Authentication**: API subscription keys (Ocp-Apim-Subscription-Key header)
- **Key Rotation**: Every 6 months (alternating primary/secondary keys)

### 🔄 API Key Rotation

**Important**: Swedavia rotates API keys every 6 months for security:
- **Primary key**: Rotated in April each year
- **Secondary key**: Rotated in October each year

**Automatic Failover**: Configure both primary and secondary keys for:
- ✅ Zero downtime during key rotation
- ✅ Automatic switching to secondary key if primary fails
- ✅ Warning logs when failover occurs
- ✅ Time to update expired keys at your convenience

**Rotation Schedule 2025-2030**: See [KEY_ROTATION_GUIDE.md](KEY_ROTATION_GUIDE.md) for complete schedule and best practices.

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
