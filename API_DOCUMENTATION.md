# Swedavia FlightInfo API - Documentation

## API Overview

The FlightInfo API offers information about arriving and departing flights to and from Swedavia's airports.

**Base URL**: `https://api.swedavia.se/flightinfo/v2`

## Authentication

All API requests require authentication via subscription key:

**Header**: `Ocp-Apim-Subscription-Key: {your-api-key}`

### Getting API Keys

1. Register at https://apideveloper.swedavia.se/
2. Subscribe to FlightInfo API (free)
3. Get your Primary and Secondary keys from Profile → Subscriptions

### Key Rotation

- **Primary key**: Rotated every April
- **Secondary key**: Rotated every October
- See [KEY_ROTATION_GUIDE.md](KEY_ROTATION_GUIDE.md) for details

## IATA Airport Codes

| Airport | IATA Code |
|---------|-----------|
| Stockholm Arlanda Airport | ARN |
| Bromma Stockholm Airport | BMA |
| Göteborg Landvetter Airport | GOT |
| Malmö Airport | MMX |
| Luleå Airport | LLA |
| Umeå Airport | UME |
| Åre Östersund Airport | OSD |
| Visby Airport | VBY |
| Ronneby Airport | RNB |
| Kiruna Airport | KRN |
| Stockholm Västerås Airport | VST |
| Örebro Airport | ORB |
| Stockholm Skavsta Airport | NYO |

**Note**: This integration currently supports 12 of the 13 airports (OSD - Åre Östersund not yet included).

## Date and Time

All datetimes are returned in **UTC format**.

### Date Format
- Request parameter: `yyyy-mm-dd` (e.g., `2026-01-16`)
- Response times: ISO 8601 UTC format

## Response Headers

### Last-Modified

All responses contain headers indicating when data was last updated:

- **Last-Modified**: Timestamp in UTC format
- **Last-Modified-In-Minutes**: Time in minutes (calculated server-side)

These values reflect when the underlying flight data globally was updated.

## Endpoints

### 1. Arrivals

Get list of arriving flights at a specific airport and date.

```
GET /flightinfo/v2/{airportIATA}/arrivals/{date}
```

**Parameters:**
- `airportIATA` (required): IATA code (e.g., "ARN")
- `date` (required): Date in format yyyy-mm-dd (UTC)

**Data Retention**: 7 days back to 90 days into the future

**Example:**
```
GET /flightinfo/v2/ARN/arrivals/2026-01-16
```

### 2. Departures

Get list of departing flights from a specific airport and date.

```
GET /flightinfo/v2/{airportIATA}/departures/{date}
```

**Parameters:**
- `airportIATA` (required): IATA code (e.g., "ARN")
- `date` (required): Date in format yyyy-mm-dd (UTC)

**Data Retention**: 7 days back to 90 days into the future

**Example:**
```
GET /flightinfo/v2/ARN/departures/2026-01-16
```

### 3. Query (Advanced)

Flexible endpoint with filtering capabilities using OData expressions.

```
GET /flightinfo/v2/query?filter={expression}&continuationtoken={token}&count={number}
```

**Parameters:**
- `filter` (optional): OData filter expression
- `continuationtoken` (optional): Token for pagination or getting changed flights
- `count` (optional): Number of items to return (default: 1000, max: 1000)

**Filterable Fields:**
- `Airport` - Airport IATA code
- `FlightType` - "A" (arrivals) or "D" (departures)
- `Scheduled` - Date in format "yymmdd" (e.g., "260116")
- `FlightId` - Flight number (e.g., "SK007")

**Supported Operators:**
- `and` - Logical AND
- `or` - Logical OR
- `eq` - Equals

**Examples:**

Departures from Arlanda on 2026-01-16:
```
airport eq 'ARN' and scheduled eq '260116' and flightType eq 'D'
```

Arrivals from Arlanda and Visby on 2026-01-16:
```
(airport eq 'ARN' or airport eq 'VBY') and flightType eq 'A' and scheduled eq '260116'
```

Get single flight:
```
airport eq 'ARN' and scheduled eq '260116' and flightType eq 'D' and flightId eq 'SK007'
```

## Flight Data Models

### Arrivals Response

```json
{
  "To": "Arriving to",
  "ArrivalAirportIata": "ARN",
  "ArrivalAirportIcao": "ESSA",
  "ArrivalAirportSwedish": "Stockholm Arlanda",
  "ArrivalAirportEnglish": "Stockholm Arlanda",
  "FlightArrivalDate": "2026-01-16",
  "NumberOfFlights": 42,
  "Flights": [...]
}
```

### Arrivals Flight Object

```json
{
  "FlightId": "SK1234",
  "DepartureAirportSwedish": "Oslo",
  "DepartureAirportEnglish": "Oslo",
  "AirlineOperator": {
    "IATA": "SK",
    "ICAO": "SAS",
    "Name": "SAS"
  },
  "ArrivalTime": {
    "ScheduledUtc": "2026-01-16T10:30:00Z",
    "EstimatedUtc": "2026-01-16T10:45:00Z",
    "ActualUtc": "2026-01-16T10:42:00Z"
  },
  "LocationAndStatus": {
    "Terminal": "5",
    "Gate": "23",
    "FlightLegStatus": "LAN",
    "FlightLegStatusSwedish": "Landat",
    "FlightLegStatusEnglish": "Landed"
  },
  "Baggage": {
    "EstimatedFirstBagUtc": "2026-01-16T11:00:00Z",
    "BaggageClaimUnit": "12",
    "FirstBagUtc": "2026-01-16T11:05:00Z",
    "LastBagUtc": "2026-01-16T11:25:00Z"
  },
  "CodeShareData": ["SK1234", "LH9876"],
  "FlightLegIdentifier": {...},
  "RemarksEnglish": [...],
  "RemarksSwedish": [...],
  "ViaDestinations": [...],
  "DIIndicator": "I"
}
```

### Departures Response

```json
{
  "From": "Departure from",
  "DepartureAirportIata": "ARN",
  "DepartureAirportIcao": "ESSA",
  "DepartureAirportSwedish": "Stockholm Arlanda",
  "DepartureAirportEnglish": "Stockholm Arlanda",
  "FlightDepartureDate": "2026-01-16",
  "NumberOfFlights": 38,
  "Flights": [...]
}
```

### Departures Flight Object

```json
{
  "FlightId": "SK1425",
  "ArrivalAirportSwedish": "Köpenhamn",
  "ArrivalAirportEnglish": "Copenhagen",
  "AirlineOperator": {
    "IATA": "SK",
    "ICAO": "SAS",
    "Name": "SAS"
  },
  "DepartureTime": {
    "ScheduledUtc": "2026-01-16T14:30:00Z",
    "EstimatedUtc": "2026-01-16T14:35:00Z",
    "ActualUtc": null
  },
  "LocationAndStatus": {
    "Terminal": "5",
    "Gate": "42",
    "GateAction": "O",
    "GateActionSwedish": "Öppen",
    "GateActionEnglish": "Open",
    "GateOpenUtc": "2026-01-16T13:00:00Z",
    "GateCloseUtc": "2026-01-16T14:00:00Z",
    "FlightLegStatus": "SCH",
    "FlightLegStatusSwedish": "Schemalagd",
    "FlightLegStatusEnglish": "Scheduled"
  },
  "CheckIn": {
    "CheckInStatus": "C",
    "CheckInStatusSwedish": "Stängd",
    "CheckInStatusEnglish": "Closed",
    "CheckInDeskFrom": 201,
    "CheckInDeskTo": 205
  },
  "CodeShareData": ["SK1425", "DL7845"],
  "FlightLegIdentifier": {...},
  "RemarksEnglish": [...],
  "RemarksSwedish": [...],
  "ViaDestinations": [...],
  "DIIndicator": "I"
}
```

## Flight Status Codes

| Code | Swedish | English |
|------|---------|---------|
| SCH | Schemalagd | Scheduled |
| FPL | Flygplan | Flight Plan |
| FLS | Flygningen inställd | Flight Suspended |
| SEQ | Sekvenserad | Sequenced |
| ACT | Aktiv | Active |
| CAN | Inställd | Cancelled |
| LAN | Landat | Landed |
| RER | Omdirigerad | Rerouted |
| DIV | Avledd | Diverted |
| DEL | Raderad | Deleted |

## Gate and Check-in Status

### Gate Action
- **O** (Open / Öppen) - Boarding in progress
- **C** (Closed / Stängd) - Gate closed

### Check-in Status
- **O** (Open / Öppen) - Check-in open
- **C** (Closed / Stängd) - Check-in closed

## Domestic/International Indicator

**DIIndicator** field shows flight type:
- **D** - Domestic (Inrikes)
- **I** - International (Utrikes)
- **S** - Schengen

## Via Destinations

Flights with multiple stops include `ViaDestinations` array:

```json
"ViaDestinations": [
  {
    "AirportIATA": "GOT",
    "AirportSwedish": "Göteborg Landvetter",
    "AirportEnglish": "Gothenburg Landvetter"
  }
]
```

## Remarks

Flight-specific information in both languages:

```json
"RemarksEnglish": [
  {
    "Text": "Gate closes 15 minutes before departure",
    "Indicator": "INFO"
  }
],
"RemarksSwedish": [
  {
    "Text": "Gate stänger 15 minuter före avgång",
    "Indicator": "INFO"
  }
]
```

## Rate Limiting

**Recommended**: Minimum 1 second between requests

This integration implements:
- 1 second minimum delay between API calls
- 5-minute update interval (default)
- Automatic retry on rate limit errors (HTTP 429)

## Error Handling

### HTTP Status Codes

- **200 OK** - Success
- **401 Unauthorized** - Invalid or expired API key
- **404 Not Found** - Invalid airport code or date
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Swedavia API error

### Automatic Failover

This integration supports automatic failover:

1. Request fails with HTTP 401 (Unauthorized)
2. If secondary key is configured, retry with secondary key
3. Log warning about failover
4. If both keys fail, report error to Home Assistant

See [KEY_ROTATION_GUIDE.md](KEY_ROTATION_GUIDE.md) for configuration.

## Integration Implementation

### Endpoints Used

This integration uses the **Arrivals** and **Departures** endpoints:

```
GET /flightinfo/v2/{airport}/arrivals/{date}
GET /flightinfo/v2/{airport}/departures/{date}
```

### Data Flow

1. **Configuration**: User provides API keys and selects airport
2. **Date Range**: Calculate dates based on hours_back and hours_ahead
3. **API Calls**: Fetch data for each date in range
4. **Parsing**: Extract relevant flight information
5. **Filtering**: Keep flights within time window
6. **Sensors**: Update Home Assistant sensors with flight data

### Update Interval

- **Default**: 5 minutes (300 seconds)
- **Configurable**: Can be adjusted in future releases
- **Rate Limiting**: Enforced 1 second between requests

## Best Practices

### API Usage

1. **Use both keys**: Configure primary + secondary for automatic failover
2. **Respect rate limits**: Don't poll more frequently than needed
3. **Handle errors**: Expect occasional API unavailability
4. **Cache responses**: Use Last-Modified headers to detect changes

### Key Management

1. **Rotation schedule**: Update keys according to schedule
2. **Test before expiry**: Verify new keys work before old ones expire
3. **Monitor logs**: Check for failover warnings
4. **Secondary key**: Always configure for zero downtime

### Time Windows

1. **Hours back**: Keep reasonable (2-4 hours) to reduce API load
2. **Hours ahead**: Balance between data freshness and API calls
3. **Multiple dates**: Integration automatically handles date ranges

## Resources

- **Developer Portal**: https://apideveloper.swedavia.se/
- **API Status**: Check developer portal for service announcements
- **Support**: Contact Swedavia via developer portal
- **Integration Issues**: https://github.com/frodr1k/Swedavia_info/issues

## Version Information

- **API Version**: 2.0.0
- **Integration Version**: 1.0.0
- **Documentation Generated**: 2026-01-16
- **Last Updated**: 2026-01-16

---

**Note**: This documentation is based on Swedavia's official API documentation dated 2019-03-25. Always refer to the official developer portal for the most current information.
