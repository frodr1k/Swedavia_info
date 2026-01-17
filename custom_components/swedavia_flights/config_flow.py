"""Config flow for Swedavia Flight Information integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import SwedaviaAPIError, SwedaviaFlightAPI
from .const import (
    CONF_API_KEY,
    CONF_API_KEY_SECONDARY,
    CONF_AIRPORT,
    CONF_FLIGHT_TYPE,
    CONF_HOURS_AHEAD,
    CONF_HOURS_BACK,
    DOMAIN,
    FLIGHT_TYPE_ARRIVALS,
    FLIGHT_TYPE_BOTH,
    FLIGHT_TYPE_DEPARTURES,
    SWEDISH_AIRPORTS,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api_key = data.get(CONF_API_KEY)
    api_key_secondary = data.get(CONF_API_KEY_SECONDARY)
    api = SwedaviaFlightAPI(session, api_key, api_key_secondary)

    airport = data[CONF_AIRPORT]

    # Validate connection
    if not await api.validate_connection(airport):
        raise SwedaviaAPIError("Cannot connect to Swedavia API")

    return {"title": f"Swedavia - {SWEDISH_AIRPORTS.get(airport, airport)}"}


class SwedaviaFlightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swedavia Flight Information."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._existing_api_keys: dict[str, str] | None = None

    def _get_existing_api_keys(self) -> dict[str, str] | None:
        """Get API keys from existing config entries."""
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            api_key = entry.data.get(CONF_API_KEY)
            if api_key:
                return {
                    CONF_API_KEY: api_key,
                    CONF_API_KEY_SECONDARY: entry.data.get(CONF_API_KEY_SECONDARY),
                }
        return None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if we have existing API keys
        existing_keys = self._get_existing_api_keys()
        
        if existing_keys:
            # Skip to airport selection if we have valid keys
            return await self.async_step_airport(user_input, existing_keys)
        else:
            # Show API key input step
            return await self.async_step_api_keys(user_input)

    async def async_step_api_keys(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle API key configuration step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Store API keys and move to airport selection
            self._existing_api_keys = {
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_API_KEY_SECONDARY: user_input.get(CONF_API_KEY_SECONDARY),
            }
            return await self.async_step_airport()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_API_KEY_SECONDARY): cv.string,
            }
        )

        return self.async_show_form(
            step_id="api_keys",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "api_key_desc": "Primär subscription key från Swedavias developer portal (https://apideveloper.swedavia.se). Obligatorisk.",
                "api_key_secondary_desc": "Sekundär subscription key (valfritt men rekommenderat). Vid nyckelrotation växlar integrationen automatiskt till sekundär nyckel om primär misslyckas.",
            },
        )

    async def async_step_airport(
        self, user_input: dict[str, Any] | None = None,
        existing_keys: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle airport and flight type selection."""
        errors: dict[str, str] = {}

        # Use provided existing keys or stored keys
        if existing_keys:
            self._existing_api_keys = existing_keys
        
        if user_input is not None:
            # Combine API keys with user input
            complete_data = {
                **self._existing_api_keys,
                **user_input,
            }

            try:
                info = await validate_input(self.hass, complete_data)
            except SwedaviaAPIError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create unique ID based on airport and flight type
                await self.async_set_unique_id(
                    f"{user_input[CONF_AIRPORT]}_{user_input[CONF_FLIGHT_TYPE]}"
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=complete_data)

        # Show message if reusing existing API keys
        description_placeholders = {}
        if self._existing_api_keys:
            description_placeholders["info"] = "✅ Återanvänder API-nycklar från befintlig integration"

        # Build schema with airport selector
        # Create airport selection with "Name (IATA)" format
        airport_options = {
            code: f"{name} ({code})" 
            for code, name in SWEDISH_AIRPORTS.items()
        }
        
        data_schema = vol.Schema(
            {
                vol.Required(CONF_AIRPORT, default="ARN"): vol.In(airport_options),
                vol.Required(CONF_FLIGHT_TYPE, default=FLIGHT_TYPE_BOTH): vol.In(
                    {
                        FLIGHT_TYPE_ARRIVALS: "Ankomster",
                        FLIGHT_TYPE_DEPARTURES: "Avgångar",
                        FLIGHT_TYPE_BOTH: "Både ankomster och avgångar",
                    }
                ),
                vol.Optional(CONF_HOURS_BACK, default=2): cv.positive_int,
                vol.Optional(CONF_HOURS_AHEAD, default=24): cv.positive_int,
            }
        )

        return self.async_show_form(
            step_id="airport",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SwedaviaFlightOptionsFlow:
        """Get the options flow for this handler."""
        return SwedaviaFlightOptionsFlow(config_entry)


class SwedaviaFlightOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Swedavia Flight Information."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Update config entry data
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={**self._config_entry.data, **user_input},
            )
            return self.async_create_entry(title="", data={})

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_HOURS_BACK,
                    default=self._config_entry.data.get(CONF_HOURS_BACK, 2),
                ): cv.positive_int,
                vol.Optional(
                    CONF_HOURS_AHEAD,
                    default=self._config_entry.data.get(CONF_HOURS_AHEAD, 24),
                ): cv.positive_int,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
