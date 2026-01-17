"""The Swedavia Flight Information integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .api import SwedaviaFlightAPI
from .const import CONF_API_KEY, CONF_API_KEY_SECONDARY, DOMAIN
from .coordinator import SwedaviaFlightCoordinator
from .key_rotation import should_warn_about_rotation, get_rotation_warning_message
from .services import async_setup_services, async_unload_services

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

    # Create API client
    session = async_get_clientsession(hass)
    api_key = entry.data.get(CONF_API_KEY)
    api_key_secondary = entry.data.get(CONF_API_KEY_SECONDARY)
    api = SwedaviaFlightAPI(session, api_key, api_key_secondary)

    # Create coordinator
    coordinator = SwedaviaFlightCoordinator(hass, api, entry)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

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
