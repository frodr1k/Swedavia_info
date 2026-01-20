"""DataUpdateCoordinator for Swedavia Flight Information."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SwedaviaAPIError, SwedaviaFlightAPI
from .const import (
    CONF_AIRPORT,
    CONF_FLIGHT_TYPE,
    CONF_HOURS_AHEAD,
    CONF_HOURS_BACK,
    DOMAIN,
    FLIGHT_TYPE_ARRIVALS,
    FLIGHT_TYPE_BOTH,
    FLIGHT_TYPE_DEPARTURES,
)
from .update_scheduler import calculate_update_schedule

if TYPE_CHECKING:
    from .boost_mode import BoostMode

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

        # Calculate optimal update interval and offset using smart scheduler
        update_interval, update_offset = calculate_update_schedule(hass, entry)
        
        _LOGGER.info(
            "Initializing coordinator for %s with %d minute interval and %d second offset",
            self.airport,
            int(update_interval.total_seconds() / 60),
            int(update_offset.total_seconds()),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.airport}",
            update_interval=update_interval,
        )
        
        # Store offset for initial delay
        self._update_offset = update_offset
        self._normal_interval = update_interval
        self._boost_mode: BoostMode | None = None

    def set_boost_mode(self, boost_mode: BoostMode) -> None:
        """Set the boost mode manager."""
        self._boost_mode = boost_mode

    async def async_request_refresh(self) -> None:
        """Request a refresh and check for boost mode."""
        # Check if boost mode is active and adjust interval
        if self._boost_mode and self._boost_mode.is_boost_active(self.entry.entry_id):
            boost_interval = self._boost_mode.get_boost_interval(self.entry.entry_id)
            if boost_interval:
                new_interval = timedelta(seconds=boost_interval)
                if self.update_interval != new_interval:
                    self.update_interval = new_interval
                    _LOGGER.info(
                        "⚡ Boost mode active for %s - interval: %d seconds",
                        self.airport,
                        boost_interval,
                    )
        else:
            # Restore normal interval if boost ended
            if self.update_interval != self._normal_interval:
                self.update_interval = self._normal_interval
                _LOGGER.info(
                    "Normal mode restored for %s - interval: %d minutes",
                    self.airport,
                    int(self._normal_interval.total_seconds() / 60),
                )

        await super().async_request_refresh()

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
