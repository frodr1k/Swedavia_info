"""Sensor platform for Swedavia Flight Information."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_ACTUAL_TIME,
    ATTR_AIRLINE,
    ATTR_AIRLINE_IATA,
    ATTR_AIRLINE_ICAO,
    ATTR_BAGGAGE_CLAIM,
    ATTR_CHECK_IN_FROM,
    ATTR_CHECK_IN_STATUS,
    ATTR_CHECK_IN_TO,
    ATTR_CODE_SHARE,
    ATTR_DESTINATION,
    ATTR_ESTIMATED_FIRST_BAG,
    ATTR_ESTIMATED_TIME,
    ATTR_FIRST_BAG,
    ATTR_FLIGHT_ID,
    ATTR_GATE,
    ATTR_GATE_ACTION,
    ATTR_GATE_CLOSE,
    ATTR_GATE_OPEN,
    ATTR_LAST_BAG,
    ATTR_ORIGIN,
    ATTR_REMARKS,
    ATTR_SCHEDULED_TIME,
    ATTR_STATUS,
    ATTR_TERMINAL,
    CONF_AIRPORT,
    CONF_FLIGHT_TYPE,
    DOMAIN,
    FLIGHT_TYPE_ARRIVALS,
    FLIGHT_TYPE_BOTH,
    FLIGHT_TYPE_DEPARTURES,
    SENSOR_TYPE_ARRIVALS,
    SENSOR_TYPE_BAGGAGE,
    SENSOR_TYPE_DEPARTURES,
    SENSOR_TYPE_KEY_ROTATION,
    SWEDISH_AIRPORTS,
)
from .coordinator import SwedaviaFlightCoordinator
from .key_rotation import get_all_rotation_info

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Swedavia Flight sensors from a config entry."""
    coordinator: SwedaviaFlightCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    flight_type = entry.data.get(CONF_FLIGHT_TYPE, FLIGHT_TYPE_BOTH)

    # Add arrivals sensor
    if flight_type in (FLIGHT_TYPE_ARRIVALS, FLIGHT_TYPE_BOTH):
        entities.append(
            SwedaviaFlightSensor(
                coordinator,
                entry,
                SENSOR_TYPE_ARRIVALS,
            )
        )

    # Add departures sensor
    if flight_type in (FLIGHT_TYPE_DEPARTURES, FLIGHT_TYPE_BOTH):
        entities.append(
            SwedaviaFlightSensor(
                coordinator,
                entry,
                SENSOR_TYPE_DEPARTURES,
            )
        )

    # Add baggage claim sensor (only for arrivals)
    if flight_type in (FLIGHT_TYPE_ARRIVALS, FLIGHT_TYPE_BOTH):
        entities.append(
            SwedaviaBaggageSensor(
                coordinator,
                entry,
            )
        )

    # Add key rotation sensor (one per integration instance)
    entities.append(
        SwedaviaKeyRotationSensor(
            entry,
        )
    )

    async_add_entities(entities)


class SwedaviaFlightSensor(CoordinatorEntity[SwedaviaFlightCoordinator], SensorEntity):
    """Representation of a Swedavia Flight sensor."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SwedaviaFlightCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._airport = entry.data[CONF_AIRPORT]
        self._airport_name = SWEDISH_AIRPORTS.get(self._airport, self._airport)

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"

        # Set name
        if sensor_type == SENSOR_TYPE_ARRIVALS:
            self._attr_name = f"{self._airport_name} Ankomster"
            self._attr_icon = "mdi:airplane-landing"
        else:
            self._attr_name = f"{self._airport_name} Avgångar"
            self._attr_icon = "mdi:airplane-takeoff"

    @property
    def native_value(self) -> int:
        """Return the number of flights."""
        if self.coordinator.data is None:
            return 0

        if self._sensor_type == SENSOR_TYPE_ARRIVALS:
            return len(self.coordinator.data.get("arrivals", []))
        return len(self.coordinator.data.get("departures", []))

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "flyg"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data is None:
            return {}

        flights_key = (
            "arrivals" if self._sensor_type == SENSOR_TYPE_ARRIVALS else "departures"
        )
        flights = self.coordinator.data.get(flights_key, [])

        # Process flights
        processed_flights = []
        for flight in flights[:50]:  # Limit to 50 flights
            processed_flight = self._process_flight(flight)
            processed_flights.append(processed_flight)

        # Sort by scheduled time
        processed_flights.sort(
            key=lambda x: x.get(ATTR_SCHEDULED_TIME, ""), reverse=False
        )

        return {
            "airport": self._airport,
            "airport_name": self._airport_name,
            "flights": processed_flights,
            "last_updated": datetime.now().isoformat(),
        }

    def _process_flight(self, flight: dict[str, Any]) -> dict[str, Any]:
        """Process a single flight into attributes."""
        is_arrival = self._sensor_type == SENSOR_TYPE_ARRIVALS

        # Get time data
        time_key = "arrivalTime" if is_arrival else "departureTime"
        time_data = flight.get(time_key, {})

        # Get airline data
        airline = flight.get("airlineOperator", {})

        # Get location data
        location = flight.get("locationAndStatus", {})

        # Get baggage data (arrivals only)
        baggage = flight.get("baggage", {}) if is_arrival else {}

        # Get check-in data (departures only)
        checkin = flight.get("checkIn", {}) if not is_arrival else {}

        # Get airport names
        if is_arrival:
            origin = flight.get("departureAirportSwedish", "")
            destination = self._airport_name
        else:
            origin = self._airport_name
            destination = flight.get("arrivalAirportSwedish", "")

        # Build processed flight
        processed = {
            ATTR_FLIGHT_ID: flight.get("flightId", ""),
            ATTR_AIRLINE: airline.get("name", ""),
            ATTR_AIRLINE_IATA: airline.get("iata", ""),
            ATTR_AIRLINE_ICAO: airline.get("icao", ""),
            ATTR_SCHEDULED_TIME: time_data.get("scheduledUtc", ""),
            ATTR_ESTIMATED_TIME: time_data.get("estimatedUtc", ""),
            ATTR_ACTUAL_TIME: time_data.get("actualUtc", ""),
            ATTR_STATUS: location.get("flightLegStatusSwedish", ""),
            ATTR_TERMINAL: location.get("terminal", ""),
            ATTR_GATE: location.get("gate", ""),
            ATTR_ORIGIN: origin,
            ATTR_DESTINATION: destination,
            ATTR_CODE_SHARE: flight.get("codeShareData", []),
        }

        # Add gate actions for departures
        if not is_arrival:
            processed[ATTR_GATE_ACTION] = location.get("gateActionSwedish", "")
            processed[ATTR_GATE_OPEN] = location.get("gateOpenUtc", "")
            processed[ATTR_GATE_CLOSE] = location.get("gateCloseUtc", "")
            processed[ATTR_CHECK_IN_STATUS] = checkin.get("checkInStatusSwedish", "")
            processed[ATTR_CHECK_IN_FROM] = checkin.get("checkInDeskFrom")
            processed[ATTR_CHECK_IN_TO] = checkin.get("checkInDeskTo")

        # Add baggage info for arrivals
        if is_arrival:
            processed[ATTR_BAGGAGE_CLAIM] = baggage.get("baggageClaimUnit", "")
            processed[ATTR_ESTIMATED_FIRST_BAG] = baggage.get(
                "estimatedFirstBagUtc", ""
            )
            processed[ATTR_FIRST_BAG] = baggage.get("firstBagUtc", "")
            processed[ATTR_LAST_BAG] = baggage.get("lastBagUtc", "")

        # Add remarks
        remarks = []
        for remark in flight.get("remarksSwedish", []):
            if text := remark.get("text"):
                remarks.append(text)
        if remarks:
            processed[ATTR_REMARKS] = ", ".join(remarks)

        return processed


class SwedaviaBaggageSensor(CoordinatorEntity[SwedaviaFlightCoordinator], SensorEntity):
    """Sensor for baggage claim information."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SwedaviaFlightCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the baggage sensor."""
        super().__init__(coordinator)
        self._airport = entry.data[CONF_AIRPORT]
        self._airport_name = SWEDISH_AIRPORTS.get(self._airport, self._airport)
        
        self._attr_unique_id = f"{entry.entry_id}_baggage"
        self._attr_name = "Bagage"
        self._attr_icon = "mdi:bag-suitcase"

    @property
    def native_value(self) -> int:
        """Return the number of flights with baggage information."""
        if not self.coordinator.data:
            return 0

        arrivals = self.coordinator.data.get("arrivals", [])
        # Count flights that have baggage claim information
        count = sum(
            1 for flight in arrivals 
            if flight.get("baggage", {}).get("baggageClaimUnit")
        )
        return count

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        arrivals = self.coordinator.data.get("arrivals", [])
        baggage_events = []

        for flight in arrivals:
            baggage = flight.get("baggage", {})
            baggage_claim = baggage.get("baggageClaimUnit")
            
            # Only include flights with baggage claim information
            if not baggage_claim:
                continue

            airline = flight.get("airlineOperator", {})
            time_data = flight.get("arrivalTime", {})
            location = flight.get("locationAndStatus", {})

            # Get the most accurate arrival time
            arrival_time = (
                time_data.get("actualUtc")
                or time_data.get("estimatedUtc")
                or time_data.get("scheduledUtc", "")
            )

            event = {
                ATTR_FLIGHT_ID: flight.get("flightId", ""),
                ATTR_AIRLINE: airline.get("name", ""),
                ATTR_ORIGIN: flight.get("departureAirportSwedish", ""),
                ATTR_SCHEDULED_TIME: time_data.get("scheduledUtc", ""),
                ATTR_ACTUAL_TIME: time_data.get("actualUtc", ""),
                ATTR_STATUS: location.get("flightLegStatusSwedish", ""),
                ATTR_TERMINAL: location.get("terminal", ""),
                ATTR_BAGGAGE_CLAIM: baggage_claim,
                ATTR_ESTIMATED_FIRST_BAG: baggage.get("estimatedFirstBagUtc", ""),
                ATTR_FIRST_BAG: baggage.get("firstBagUtc", ""),
                ATTR_LAST_BAG: baggage.get("lastBagUtc", ""),
            }

            # Add code share flights
            code_share = flight.get("codeShareData", [])
            if code_share:
                event[ATTR_CODE_SHARE] = code_share

            baggage_events.append(event)

        # Sort by actual/estimated/scheduled time
        baggage_events.sort(
            key=lambda x: x.get(ATTR_ACTUAL_TIME) 
            or x.get(ATTR_SCHEDULED_TIME) 
            or ""
        )

        return {
            "airport": self._airport_name,
            "airport_iata": self._airport,
            "baggage_claims": baggage_events,
        }


class SwedaviaKeyRotationSensor(SensorEntity):
    """Sensor for API key rotation status."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:key-chain"

    def __init__(
        self,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the key rotation sensor."""
        self._airport = entry.data[CONF_AIRPORT]
        self._attr_unique_id = f"{entry.entry_id}_key_rotation"
        self._attr_name = "API Key Rotation"
        self._attr_device_class = None

    @property
    def native_value(self) -> str:
        """Return the status of key rotation."""
        rotation_info = get_all_rotation_info()
        
        # Check if any warning is active
        primary_warning = rotation_info["primary_key"]["warning_active"]
        secondary_warning = rotation_info["secondary_key"]["warning_active"]
        
        if primary_warning:
            primary_days = rotation_info["primary_key"]["days_until_rotation"]
            if primary_days == 0:
                return "Primary key rotates TODAY!"
            elif primary_days == 1:
                return "Primary key rotates tomorrow"
            else:
                return f"Primary key rotates in {primary_days} days"
        elif secondary_warning:
            secondary_days = rotation_info["secondary_key"]["days_until_rotation"]
            if secondary_days == 0:
                return "Secondary key rotates TODAY!"
            elif secondary_days == 1:
                return "Secondary key rotates tomorrow"
            else:
                return f"Secondary key rotates in {secondary_days} days"
        else:
            # No immediate warnings
            primary_days = rotation_info["primary_key"]["days_until_rotation"]
            secondary_days = rotation_info["secondary_key"]["days_until_rotation"]
            
            if primary_days is not None and (secondary_days is None or primary_days < secondary_days):
                return f"OK - Next rotation in {primary_days} days (primary)"
            elif secondary_days is not None:
                return f"OK - Next rotation in {secondary_days} days (secondary)"
            else:
                return "OK - No rotation scheduled"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        rotation_info = get_all_rotation_info()
        
        return {
            "primary_key_next_rotation": rotation_info["primary_key"]["next_rotation"],
            "primary_key_days_until": rotation_info["primary_key"]["days_until_rotation"],
            "primary_key_warning": rotation_info["primary_key"]["warning_message"],
            "secondary_key_next_rotation": rotation_info["secondary_key"]["next_rotation"],
            "secondary_key_days_until": rotation_info["secondary_key"]["days_until_rotation"],
            "secondary_key_warning": rotation_info["secondary_key"]["warning_message"],
            "update_service": f"{DOMAIN}.update_api_keys",
            "developer_portal": "https://apideveloper.swedavia.se/",
        }

    @property
    def icon(self) -> str:
        """Return icon based on status."""
        rotation_info = get_all_rotation_info()
        
        # Check days until rotation
        primary_days = rotation_info["primary_key"]["days_until_rotation"]
        secondary_days = rotation_info["secondary_key"]["days_until_rotation"]
        
        min_days = None
        if primary_days is not None and secondary_days is not None:
            min_days = min(primary_days, secondary_days)
        elif primary_days is not None:
            min_days = primary_days
        elif secondary_days is not None:
            min_days = secondary_days
        
        if min_days is not None:
            if min_days == 0:
                return "mdi:key-alert"
            elif min_days <= 3:
                return "mdi:key-remove"
            else:
                return "mdi:key-chain"
        
        return "mdi:key-chain"
