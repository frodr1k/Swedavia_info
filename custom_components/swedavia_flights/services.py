"""Services for Swedavia Flight Information."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import CONF_API_KEY, CONF_API_KEY_SECONDARY, CONF_AIRPORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_UPDATE_API_KEYS = "update_api_keys"
SERVICE_ENABLE_BOOST = "enable_boost_mode"
SERVICE_DISABLE_BOOST = "disable_boost_mode"

SERVICE_UPDATE_API_KEYS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_API_KEY): cv.string,
        vol.Optional(CONF_API_KEY_SECONDARY): cv.string,
    }
)

SERVICE_ENABLE_BOOST_SCHEMA = vol.Schema(
    {
        vol.Required("airport"): cv.string,
        vol.Optional("duration", default=4): vol.All(vol.Coerce(int), vol.Range(min=1, max=12)),
    }
)

SERVICE_DISABLE_BOOST_SCHEMA = vol.Schema(
    {
        vol.Required("airport"): cv.string,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Swedavia Flight Information."""

    async def handle_update_api_keys(call: ServiceCall) -> None:
        """Handle the update_api_keys service call."""
        primary_key = call.data.get(CONF_API_KEY)
        secondary_key = call.data.get(CONF_API_KEY_SECONDARY)

        if not primary_key and not secondary_key:
            _LOGGER.error("At least one API key must be provided")
            return

        # Update all config entries
        updated_count = 0
        for entry in hass.config_entries.async_entries(DOMAIN):
            new_data = dict(entry.data)
            
            if primary_key:
                new_data[CONF_API_KEY] = primary_key
                _LOGGER.info("Updated primary API key for %s", entry.title)
            
            if secondary_key:
                new_data[CONF_API_KEY_SECONDARY] = secondary_key
                _LOGGER.info("Updated secondary API key for %s", entry.title)
            
            hass.config_entries.async_update_entry(entry, data=new_data)
            updated_count += 1

            # Reload the entry to use new keys
            await hass.config_entries.async_reload(entry.entry_id)

        _LOGGER.info(
            "Successfully updated API keys for %d integration(s)", updated_count
        )

    async def handle_enable_boost(call: ServiceCall) -> None:
        """Handle the enable_boost_mode service call."""
        airport = call.data["airport"].upper()
        duration = call.data.get("duration", 4)

        # Find the config entry for this airport
        entry = None
        for config_entry in hass.config_entries.async_entries(DOMAIN):
            if config_entry.data.get(CONF_AIRPORT) == airport:
                entry = config_entry
                break

        if not entry:
            _LOGGER.error("No configuration found for airport %s", airport)
            return

        # Get boost mode manager
        boost_mode = hass.data[DOMAIN].get("boost_mode")
        if not boost_mode:
            _LOGGER.error("Boost mode manager not initialized")
            return

        # Activate boost
        result = await boost_mode.activate_boost(entry.entry_id, duration)
        
        # Get coordinator and trigger immediate refresh
        coordinator = hass.data[DOMAIN].get(entry.entry_id)
        if coordinator:
            await coordinator.async_request_refresh()

        _LOGGER.info(
            "⚡ Boost mode enabled for %s - Duration: %d hours, Estimated API calls: %d",
            airport,
            duration,
            result.get("estimated_calls", 0),
        )

    async def handle_disable_boost(call: ServiceCall) -> None:
        """Handle the disable_boost_mode service call."""
        airport = call.data["airport"].upper()

        # Find the config entry for this airport
        entry = None
        for config_entry in hass.config_entries.async_entries(DOMAIN):
            if config_entry.data.get(CONF_AIRPORT) == airport:
                entry = config_entry
                break

        if not entry:
            _LOGGER.error("No configuration found for airport %s", airport)
            return

        # Get boost mode manager
        boost_mode = hass.data[DOMAIN].get("boost_mode")
        if not boost_mode:
            _LOGGER.error("Boost mode manager not initialized")
            return

        # Deactivate boost
        was_active = await boost_mode.deactivate_boost(entry.entry_id)
        
        if was_active:
            # Get coordinator and trigger immediate refresh to restore normal interval
            coordinator = hass.data[DOMAIN].get(entry.entry_id)
            if coordinator:
                await coordinator.async_request_refresh()
            
            _LOGGER.info("Boost mode disabled for %s", airport)
        else:
            _LOGGER.warning("Boost mode was not active for %s", airport)

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_API_KEYS,
        handle_update_api_keys,
        schema=SERVICE_UPDATE_API_KEYS_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_ENABLE_BOOST,
        handle_enable_boost,
        schema=SERVICE_ENABLE_BOOST_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DISABLE_BOOST,
        handle_disable_boost,
        schema=SERVICE_DISABLE_BOOST_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for Swedavia Flight Information."""
    hass.services.async_remove(DOMAIN, SERVICE_UPDATE_API_KEYS)
    hass.services.async_remove(DOMAIN, SERVICE_ENABLE_BOOST)
    hass.services.async_remove(DOMAIN, SERVICE_DISABLE_BOOST)
