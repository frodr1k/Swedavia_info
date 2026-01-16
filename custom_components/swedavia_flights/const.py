"""Constants for the Swedavia Flight Information integration."""

DOMAIN = "swedavia_flights"

# API Configuration
API_BASE_URL = "https://api.swedavia.se/flightinfo/v2"
API_TIMEOUT = 30
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Configuration Keys
CONF_AIRPORT = "airport"
CONF_FLIGHT_TYPE = "flight_type"
CONF_HOURS_AHEAD = "hours_ahead"
CONF_HOURS_BACK = "hours_back"
CONF_API_KEY = "api_key"

# Flight Types
FLIGHT_TYPE_ARRIVALS = "arrivals"
FLIGHT_TYPE_DEPARTURES = "departures"
FLIGHT_TYPE_BOTH = "both"

# Swedish Airports (IATA codes)
SWEDISH_AIRPORTS = {
    "ARN": "Stockholm Arlanda",
    "BMA": "Stockholm Bromma",
    "GOT": "Göteborg Landvetter",
    "MMX": "Malmö",
    "LLA": "Luleå",
    "UME": "Umeå",
    "VBY": "Visby",
    "KRN": "Kiruna",
    "RNB": "Ronneby",
    "VST": "Stockholm Västerås",
    "ORB": "Örebro",
    "NYO": "Stockholm Skavsta",
}

# Sensor Types
SENSOR_TYPE_ARRIVALS = "arrivals"
SENSOR_TYPE_DEPARTURES = "departures"

# Flight Status Codes
FLIGHT_STATUS_SCHEDULED = "SCH"
FLIGHT_STATUS_DELAYED = "DEL"
FLIGHT_STATUS_CANCELLED = "CNL"
FLIGHT_STATUS_LANDED = "LND"
FLIGHT_STATUS_DEPARTED = "DEP"

# Attributes
ATTR_FLIGHT_ID = "flight_id"
ATTR_AIRLINE = "airline"
ATTR_AIRLINE_IATA = "airline_iata"
ATTR_AIRLINE_ICAO = "airline_icao"
ATTR_SCHEDULED_TIME = "scheduled_time"
ATTR_ESTIMATED_TIME = "estimated_time"
ATTR_ACTUAL_TIME = "actual_time"
ATTR_STATUS = "status"
ATTR_TERMINAL = "terminal"
ATTR_GATE = "gate"
ATTR_GATE_ACTION = "gate_action"
ATTR_GATE_OPEN = "gate_open"
ATTR_GATE_CLOSE = "gate_close"
ATTR_BAGGAGE_CLAIM = "baggage_claim"
ATTR_FIRST_BAG = "first_bag"
ATTR_LAST_BAG = "last_bag"
ATTR_ESTIMATED_FIRST_BAG = "estimated_first_bag"
ATTR_CODE_SHARE = "code_share_flights"
ATTR_REMARKS = "remarks"
ATTR_ORIGIN = "origin"
ATTR_DESTINATION = "destination"
ATTR_CHECK_IN_FROM = "check_in_from"
ATTR_CHECK_IN_TO = "check_in_to"
ATTR_CHECK_IN_STATUS = "check_in_status"
