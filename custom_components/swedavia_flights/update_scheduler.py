"""Smart Update Scheduler for Swedavia Flight Information."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import TYPE_CHECKING

from homeassistant.core import HomeAssistant

from .const import (
    CONF_AIRPORT,
    CONF_FLIGHT_TYPE,
    DOMAIN,
    FLIGHT_TYPE_ARRIVALS,
    FLIGHT_TYPE_BOTH,
    FLIGHT_TYPE_DEPARTURES,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

# API limit: 10,001 calls per 30 days
API_LIMIT = 10001
DAYS_IN_MONTH = 30
SAFETY_MARGIN = 0.85  # Use only 85% of limit for safety

# Calculate available calls per day
MAX_CALLS_PER_DAY = int((API_LIMIT * SAFETY_MARGIN) / DAYS_IN_MONTH)  # ~283 calls/day


class UpdateScheduler:
    """Calculate optimal update intervals based on configuration."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the scheduler."""
        self._hass = hass

    def calculate_optimal_interval(self, entry: ConfigEntry) -> timedelta:
        """
        Calculate optimal update interval for a single config entry.
        
        Returns the update interval in seconds as a timedelta.
        """
        # Get all entries to count total airports and configurations
        all_entries = self._hass.config_entries.async_entries(DOMAIN)
        
        # Calculate calls per update for this entry
        calls_per_update = self._calculate_calls_per_update(entry)
        
        # Calculate total calls per update across all entries
        total_calls_per_update = sum(
            self._calculate_calls_per_update(e) for e in all_entries
        )
        
        # Calculate optimal interval to stay under daily limit
        # We want: (86400 seconds / interval) * total_calls_per_update < MAX_CALLS_PER_DAY
        # Therefore: interval > (86400 * total_calls_per_update) / MAX_CALLS_PER_DAY
        
        min_interval = (86400 * total_calls_per_update) / MAX_CALLS_PER_DAY
        
        # Round up to nearest 5 minutes for cleaner intervals
        min_interval_minutes = int(min_interval / 60) + 1
        rounded_interval_minutes = ((min_interval_minutes + 4) // 5) * 5
        
        # Set minimum interval to 5 minutes, maximum to 30 minutes
        final_interval_minutes = max(5, min(30, rounded_interval_minutes))
        
        interval = timedelta(minutes=final_interval_minutes)
        
        _LOGGER.info(
            "Calculated update interval for %s: %d minutes "
            "(calls per update: %d, total calls per update across all airports: %d)",
            entry.data.get(CONF_AIRPORT, "unknown"),
            final_interval_minutes,
            calls_per_update,
            total_calls_per_update,
        )
        
        return interval

    def calculate_offset(self, entry: ConfigEntry) -> timedelta:
        """
        Calculate time offset for staggered updates across multiple airports.
        
        This ensures that if you have multiple airports configured,
        they don't all update at the same time.
        """
        all_entries = self._hass.config_entries.async_entries(DOMAIN)
        
        if len(all_entries) <= 1:
            return timedelta(seconds=0)
        
        # Find the index of this entry
        try:
            entry_index = all_entries.index(entry)
        except ValueError:
            entry_index = 0
        
        # Calculate the update interval
        interval = self.calculate_optimal_interval(entry)
        
        # Distribute offsets evenly across the interval
        offset_seconds = (interval.total_seconds() / len(all_entries)) * entry_index
        
        offset = timedelta(seconds=int(offset_seconds))
        
        _LOGGER.info(
            "Calculated update offset for %s: %d seconds "
            "(entry %d of %d)",
            entry.data.get(CONF_AIRPORT, "unknown"),
            int(offset_seconds),
            entry_index + 1,
            len(all_entries),
        )
        
        return offset

    def _calculate_calls_per_update(self, entry: ConfigEntry) -> int:
        """
        Calculate expected API calls per update for a config entry.
        
        Assumes:
        - With hours_ahead=24, hours_back=2: typically 2 dates (today + tomorrow)
        - Arrivals only: 2 calls
        - Departures only: 2 calls
        - Both: 4 calls
        """
        flight_type = entry.data.get(CONF_FLIGHT_TYPE, FLIGHT_TYPE_BOTH)
        
        # Estimate 2 date ranges (today + tomorrow) for 24h ahead window
        dates_per_type = 2
        
        if flight_type == FLIGHT_TYPE_BOTH:
            return dates_per_type * 2  # Both arrivals and departures
        else:
            return dates_per_type  # Only arrivals or departures

    def get_schedule_info(self) -> dict:
        """Get information about the current update schedule."""
        all_entries = self._hass.config_entries.async_entries(DOMAIN)
        
        if not all_entries:
            return {
                "total_entries": 0,
                "total_calls_per_update": 0,
                "estimated_daily_calls": 0,
                "estimated_monthly_calls": 0,
                "percentage_of_limit": 0.0,
            }
        
        # Calculate for first entry (they all have same interval)
        interval = self.calculate_optimal_interval(all_entries[0])
        total_calls_per_update = sum(
            self._calculate_calls_per_update(e) for e in all_entries
        )
        
        updates_per_day = 86400 / interval.total_seconds()
        estimated_daily_calls = int(updates_per_day * total_calls_per_update)
        estimated_monthly_calls = estimated_daily_calls * DAYS_IN_MONTH
        percentage = (estimated_monthly_calls / API_LIMIT) * 100
        
        return {
            "total_entries": len(all_entries),
            "update_interval_minutes": int(interval.total_seconds() / 60),
            "total_calls_per_update": total_calls_per_update,
            "updates_per_day": int(updates_per_day),
            "estimated_daily_calls": estimated_daily_calls,
            "estimated_monthly_calls": estimated_monthly_calls,
            "percentage_of_limit": round(percentage, 1),
            "api_limit": API_LIMIT,
        }


def calculate_update_schedule(
    hass: HomeAssistant, entry: ConfigEntry
) -> tuple[timedelta, timedelta]:
    """
    Calculate optimal update interval and offset for a config entry.
    
    Returns:
        tuple: (update_interval, offset)
    """
    scheduler = UpdateScheduler(hass)
    interval = scheduler.calculate_optimal_interval(entry)
    offset = scheduler.calculate_offset(entry)
    
    return interval, offset
