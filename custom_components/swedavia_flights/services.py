"""Services for Swedavia Flight Information."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import CONF_API_KEY, CONF_API_KEY_SECONDARY, DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_UPDATE_API_KEYS = "update_api_keys"

SERVICE_UPDATE_API_KEYS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_API_KEY): cv.string,
        vol.Optional(CONF_API_KEY_SECONDARY): cv.string,
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

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_API_KEYS,
        handle_update_api_keys,
        schema=SERVICE_UPDATE_API_KEYS_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for Swedavia Flight Information."""
    hass.services.async_remove(DOMAIN, SERVICE_UPDATE_API_KEYS)
