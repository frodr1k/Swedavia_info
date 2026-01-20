"""API Call Counter for Swedavia Flight Information."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "swedavia_flights_api_counter"
API_CALL_LIMIT = 10001
ROLLING_WINDOW_DAYS = 30


class APICallCounter:
    """Track API calls with a 30-day rolling window."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the API call counter."""
        self._hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._call_timestamps: list[float] = []
        self._initialized = False

    async def async_initialize(self) -> None:
        """Load stored data from disk."""
        if self._initialized:
            return

        data = await self._store.async_load()
        if data and "call_timestamps" in data:
            self._call_timestamps = data["call_timestamps"]
            _LOGGER.info(
                "Loaded %d API call records from storage",
                len(self._call_timestamps)
            )
            # Clean up old entries on load
            await self._cleanup_old_entries()
        else:
            _LOGGER.info("No previous API call data found, starting fresh")
            self._call_timestamps = []

        self._initialized = True

    async def _cleanup_old_entries(self) -> None:
        """Remove entries older than 30 days."""
        cutoff_time = (
            datetime.now(timezone.utc) - timedelta(days=ROLLING_WINDOW_DAYS)
        ).timestamp()
        
        old_count = len(self._call_timestamps)
        self._call_timestamps = [
            ts for ts in self._call_timestamps if ts > cutoff_time
        ]
        
        removed_count = old_count - len(self._call_timestamps)
        if removed_count > 0:
            _LOGGER.debug(
                "Cleaned up %d old API call records (older than %d days)",
                removed_count,
                ROLLING_WINDOW_DAYS
            )
            await self._save()

    async def _save(self) -> None:
        """Save data to disk."""
        await self._store.async_save({"call_timestamps": self._call_timestamps})

    async def increment(self) -> None:
        """Increment the API call counter."""
        if not self._initialized:
            await self.async_initialize()

        # Add current timestamp
        current_time = datetime.now(timezone.utc).timestamp()
        self._call_timestamps.append(current_time)
        
        # Cleanup old entries
        await self._cleanup_old_entries()
        
        # Log warning if approaching limit
        count = self.get_count()
        if count >= API_CALL_LIMIT:
            _LOGGER.error(
                "API call limit reached! %d calls in the last %d days. "
                "Limit is %d calls per 30 days.",
                count,
                ROLLING_WINDOW_DAYS,
                API_CALL_LIMIT
            )
        elif count >= API_CALL_LIMIT * 0.9:  # 90% threshold
            _LOGGER.warning(
                "API call limit warning: %d calls in the last %d days. "
                "Limit is %d calls per 30 days.",
                count,
                ROLLING_WINDOW_DAYS,
                API_CALL_LIMIT
            )
        elif count >= API_CALL_LIMIT * 0.75:  # 75% threshold
            _LOGGER.info(
                "API call usage: %d calls in the last %d days. "
                "Limit is %d calls per 30 days.",
                count,
                ROLLING_WINDOW_DAYS,
                API_CALL_LIMIT
            )

    def get_count(self) -> int:
        """Get the number of API calls in the last 30 days."""
        if not self._initialized:
            return 0

        cutoff_time = (
            datetime.now(timezone.utc) - timedelta(days=ROLLING_WINDOW_DAYS)
        ).timestamp()
        
        return sum(1 for ts in self._call_timestamps if ts > cutoff_time)

    def get_remaining(self) -> int:
        """Get the number of remaining API calls before hitting the limit."""
        return max(0, API_CALL_LIMIT - self.get_count())

    def get_percentage_used(self) -> float:
        """Get the percentage of API calls used."""
        return (self.get_count() / API_CALL_LIMIT) * 100

    def get_oldest_call_date(self) -> datetime | None:
        """Get the date of the oldest API call in the rolling window."""
        if not self._call_timestamps:
            return None
        
        cutoff_time = (
            datetime.now(timezone.utc) - timedelta(days=ROLLING_WINDOW_DAYS)
        ).timestamp()
        
        valid_timestamps = [ts for ts in self._call_timestamps if ts > cutoff_time]
        if not valid_timestamps:
            return None
        
        return datetime.fromtimestamp(min(valid_timestamps), tz=timezone.utc)

    def get_stats(self) -> dict[str, Any]:
        """Get comprehensive statistics about API usage."""
        count = self.get_count()
        oldest = self.get_oldest_call_date()
        
        return {
            "total_calls_30_days": count,
            "remaining_calls": self.get_remaining(),
            "percentage_used": round(self.get_percentage_used(), 2),
            "limit": API_CALL_LIMIT,
            "rolling_window_days": ROLLING_WINDOW_DAYS,
            "oldest_call": oldest.isoformat() if oldest else None,
        }
