"""Boost Mode for temporary increased update frequency."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "swedavia_flights_boost_mode"

# Boost mode configuration
BOOST_INTERVAL_SECONDS = 120  # 2 minutes
BOOST_DURATION_HOURS = 4  # 4 hours
NORMAL_INTERVAL_SECONDS = 900  # 15 minutes fallback


class BoostMode:
    """Manage temporary boost mode for increased update frequency."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize boost mode manager."""
        self._hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._active_boosts: dict[str, datetime] = {}
        self._initialized = False

    async def async_initialize(self) -> None:
        """Load stored boost mode data."""
        if self._initialized:
            return

        data = await self._store.async_load()
        if data and "active_boosts" in data:
            # Convert stored timestamps back to datetime objects
            now = datetime.now(timezone.utc)
            for entry_id, timestamp_str in data["active_boosts"].items():
                try:
                    boost_end = datetime.fromisoformat(timestamp_str)
                    # Only restore if boost is still active
                    if boost_end > now:
                        self._active_boosts[entry_id] = boost_end
                        _LOGGER.info(
                            "Restored active boost for %s until %s",
                            entry_id,
                            boost_end.isoformat(),
                        )
                except (ValueError, TypeError) as err:
                    _LOGGER.warning("Failed to restore boost for %s: %s", entry_id, err)

        self._initialized = True

    async def _save(self) -> None:
        """Save boost mode data to storage."""
        # Convert datetime objects to ISO strings for storage
        data = {
            "active_boosts": {
                entry_id: boost_end.isoformat()
                for entry_id, boost_end in self._active_boosts.items()
            }
        }
        await self._store.async_save(data)

    async def activate_boost(self, entry_id: str, duration_hours: int | None = None) -> dict[str, Any]:
        """
        Activate boost mode for a specific config entry.
        
        Args:
            entry_id: The config entry ID to boost
            duration_hours: Duration in hours (default: 4 hours)
        
        Returns:
            dict with boost information
        """
        if not self._initialized:
            await self.async_initialize()

        duration = duration_hours if duration_hours else BOOST_DURATION_HOURS
        boost_end = datetime.now(timezone.utc) + timedelta(hours=duration)
        
        self._active_boosts[entry_id] = boost_end
        await self._save()

        # Calculate expected API calls
        updates_during_boost = int((duration * 3600) / BOOST_INTERVAL_SECONDS)
        
        _LOGGER.warning(
            "⚡ BOOST MODE ACTIVATED for entry %s\n"
            "Duration: %d hours\n"
            "Update interval: %d seconds (2 minutes)\n"
            "Expected updates: ~%d\n"
            "Expected API calls: ~%d (2-4 calls per update)\n"
            "Boost ends at: %s UTC\n"
            "⚠️ WARNING: This will significantly increase API usage!",
            entry_id,
            duration,
            BOOST_INTERVAL_SECONDS,
            updates_during_boost,
            updates_during_boost * 3,  # Average estimate
            boost_end.strftime("%Y-%m-%d %H:%M:%S"),
        )

        return {
            "entry_id": entry_id,
            "boost_end": boost_end.isoformat(),
            "duration_hours": duration,
            "interval_seconds": BOOST_INTERVAL_SECONDS,
            "estimated_calls": updates_during_boost * 3,
        }

    async def deactivate_boost(self, entry_id: str) -> bool:
        """
        Deactivate boost mode for a specific config entry.
        
        Returns:
            True if boost was active and deactivated, False otherwise
        """
        if not self._initialized:
            await self.async_initialize()

        if entry_id in self._active_boosts:
            del self._active_boosts[entry_id]
            await self._save()
            
            _LOGGER.info("Boost mode deactivated for entry %s", entry_id)
            return True
        
        return False

    def is_boost_active(self, entry_id: str) -> bool:
        """Check if boost mode is active for a config entry."""
        if entry_id not in self._active_boosts:
            return False

        now = datetime.now(timezone.utc)
        boost_end = self._active_boosts[entry_id]

        if boost_end <= now:
            # Boost has expired, remove it
            del self._active_boosts[entry_id]
            # Save asynchronously (fire and forget)
            self._hass.async_create_task(self._save())
            _LOGGER.info("Boost mode expired for entry %s", entry_id)
            return False

        return True

    def get_boost_interval(self, entry_id: str) -> int | None:
        """
        Get the boost interval if boost is active.
        
        Returns:
            Interval in seconds if boost active, None otherwise
        """
        if self.is_boost_active(entry_id):
            return BOOST_INTERVAL_SECONDS
        return None

    def get_boost_info(self, entry_id: str) -> dict[str, Any] | None:
        """Get information about active boost for an entry."""
        if not self.is_boost_active(entry_id):
            return None

        boost_end = self._active_boosts[entry_id]
        now = datetime.now(timezone.utc)
        remaining = boost_end - now

        return {
            "active": True,
            "boost_end": boost_end.isoformat(),
            "remaining_seconds": int(remaining.total_seconds()),
            "remaining_minutes": int(remaining.total_seconds() / 60),
            "interval_seconds": BOOST_INTERVAL_SECONDS,
        }

    def get_all_active_boosts(self) -> dict[str, dict[str, Any]]:
        """Get information about all active boosts."""
        active = {}
        for entry_id in list(self._active_boosts.keys()):
            info = self.get_boost_info(entry_id)
            if info:
                active[entry_id] = info
        return active

    async def cleanup_expired(self) -> int:
        """
        Remove all expired boosts.
        
        Returns:
            Number of expired boosts removed
        """
        if not self._initialized:
            await self.async_initialize()

        now = datetime.now(timezone.utc)
        expired = []

        for entry_id, boost_end in list(self._active_boosts.items()):
            if boost_end <= now:
                expired.append(entry_id)

        for entry_id in expired:
            del self._active_boosts[entry_id]
            _LOGGER.info("Cleaned up expired boost for entry %s", entry_id)

        if expired:
            await self._save()

        return len(expired)
