"""The Swedavia Flight Information integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .api import SwedaviaFlightAPI
from .api_counter import APICallCounter
from .boost_mode import BoostMode
from .const import CONF_API_KEY, CONF_API_KEY_SECONDARY, CONF_AIRPORT, DOMAIN
from .coordinator import SwedaviaFlightCoordinator
from .key_rotation import should_warn_about_rotation, get_rotation_warning_message
from .services import async_setup_services, async_unload_services
from .update_scheduler import UpdateScheduler

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

# Check for key rotation warnings every 6 hours
KEY_ROTATION_CHECK_INTERVAL = timedelta(hours=6)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Swedavia Flight Information from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Set up services (only once)
    if not hass.data[DOMAIN]:
        await async_setup_services(hass)

    # Initialize API call counter (shared across all entries)
    if "api_counter" not in hass.data[DOMAIN]:
        api_counter = APICallCounter(hass)
        await api_counter.async_initialize()
        hass.data[DOMAIN]["api_counter"] = api_counter
    else:
        api_counter = hass.data[DOMAIN]["api_counter"]

    # Initialize boost mode manager (shared across all entries)
    if "boost_mode" not in hass.data[DOMAIN]:
        boost_mode = BoostMode(hass)
        await boost_mode.async_initialize()
        hass.data[DOMAIN]["boost_mode"] = boost_mode
        
        # Cleanup expired boosts on start
        expired_count = await boost_mode.cleanup_expired()
        if expired_count > 0:
            _LOGGER.info("Cleaned up %d expired boost mode(s) on startup", expired_count)
    else:
        boost_mode = hass.data[DOMAIN]["boost_mode"]

    # Create API client
    session = async_get_clientsession(hass)
    api_key = entry.data.get(CONF_API_KEY)
    api_key_secondary = entry.data.get(CONF_API_KEY_SECONDARY)
    api = SwedaviaFlightAPI(session, api_key, api_key_secondary, api_counter)

    # Create coordinator
    coordinator = SwedaviaFlightCoordinator(hass, api, entry)
    
    # Set boost mode manager
    coordinator.set_boost_mode(boost_mode)

    # Apply staggered start if there's an offset
    if hasattr(coordinator, '_update_offset') and coordinator._update_offset.total_seconds() > 0:
        offset_seconds = int(coordinator._update_offset.total_seconds())
        _LOGGER.info(
            "Scheduling initial update for %s with %d second delay for load distribution",
            entry.data.get(CONF_AIRPORT, "unknown"),
            offset_seconds,
        )
        # Schedule delayed first refresh
        async def delayed_first_refresh():
            await asyncio.sleep(offset_seconds)
            await coordinator.async_config_entry_first_refresh()
        
        hass.async_create_task(delayed_first_refresh())
    else:
        # Fetch initial data immediately
        await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Log schedule information after all entries are loaded
    if "schedule_logged" not in hass.data[DOMAIN]:
        async def log_schedule_info():
            """Log schedule information after a short delay to ensure all entries are loaded."""
            await asyncio.sleep(5)
            scheduler = UpdateScheduler(hass)
            schedule_info = scheduler.get_schedule_info()
            
            _LOGGER.info(
                "=== Swedavia Flight Info - Update Schedule ===\n"
                "Total airports configured: %d\n"
                "Update interval: %d minutes\n"
                "Calls per update cycle: %d\n"
                "Updates per day: %d\n"
                "Estimated daily API calls: %d\n"
                "Estimated monthly API calls: %d (%.1f%% of limit)\n"
                "API limit: %d calls per 30 days\n"
                "==========================================",
                schedule_info["total_entries"],
                schedule_info["update_interval_minutes"],
                schedule_info["total_calls_per_update"],
                schedule_info["updates_per_day"],
                schedule_info["estimated_daily_calls"],
                schedule_info["estimated_monthly_calls"],
                schedule_info["percentage_of_limit"],
                schedule_info["api_limit"],
            )
        
        hass.async_create_task(log_schedule_info())
        hass.data[DOMAIN]["schedule_logged"] = True

    # Set up key rotation warning checker
    async def check_key_rotation_warnings(_now=None):
        """Check and log warnings about upcoming key rotations."""
        # Check primary key
        if should_warn_about_rotation("primary"):
            message = get_rotation_warning_message("primary")
            _LOGGER.warning(message)
        
        # Check secondary key
        if should_warn_about_rotation("secondary"):
            message = get_rotation_warning_message("secondary")
            _LOGGER.warning(message)

    # Run initial check
    await check_key_rotation_warnings()
    
    # Schedule periodic checks every 6 hours
    entry.async_on_unload(
        async_track_time_interval(
            hass, check_key_rotation_warnings, KEY_ROTATION_CHECK_INTERVAL
        )
    )

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Unload services if this is the last entry
        if not hass.data[DOMAIN]:
            await async_unload_services(hass)

    return unload_ok
