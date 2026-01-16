"""DataUpdateCoordinator for Swedavia Flight Information."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SwedaviaAPIError, SwedaviaFlightAPI
from .const import (
    CONF_AIRPORT,
    CONF_FLIGHT_TYPE,
    CONF_HOURS_AHEAD,
    CONF_HOURS_BACK,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    FLIGHT_TYPE_ARRIVALS,
    FLIGHT_TYPE_BOTH,
    FLIGHT_TYPE_DEPARTURES,
)

_LOGGER = logging.getLogger(__name__)


class SwedaviaFlightCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Swedavia flight data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: SwedaviaFlightAPI,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self.api = api
        self.entry = entry
        self.airport = entry.data[CONF_AIRPORT]
        self.flight_type = entry.data.get(CONF_FLIGHT_TYPE, FLIGHT_TYPE_BOTH)
        self.hours_ahead = entry.data.get(CONF_HOURS_AHEAD, 24)
        self.hours_back = entry.data.get(CONF_HOURS_BACK, 2)

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.airport}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            data = {
                "airport": self.airport,
                "arrivals": [],
                "departures": [],
            }

            # Fetch arrivals
            if self.flight_type in (FLIGHT_TYPE_ARRIVALS, FLIGHT_TYPE_BOTH):
                _LOGGER.debug("Fetching arrivals for %s", self.airport)
                arrivals = await self.api.get_flights_by_date_range(
                    self.airport,
                    "arrivals",
                    hours_back=self.hours_back,
                    hours_ahead=self.hours_ahead,
                )
                data["arrivals"] = arrivals
                _LOGGER.debug("Got %d arrivals", len(arrivals))

            # Fetch departures
            if self.flight_type in (FLIGHT_TYPE_DEPARTURES, FLIGHT_TYPE_BOTH):
                _LOGGER.debug("Fetching departures for %s", self.airport)
                departures = await self.api.get_flights_by_date_range(
                    self.airport,
                    "departures",
                    hours_back=self.hours_back,
                    hours_ahead=self.hours_ahead,
                )
                data["departures"] = departures
                _LOGGER.debug("Got %d departures", len(departures))

            return data

        except SwedaviaAPIError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
