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

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
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

                return self.async_create_entry(title=info["title"], data=user_input)

        # Build schema with airport selector
        # Create airport selection with "Name (IATA)" format
        airport_options = {
            code: f"{name} ({code})" 
            for code, name in SWEDISH_AIRPORTS.items()
        }
        
        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_API_KEY_SECONDARY): cv.string,
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
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "api_key_desc": "Primary subscription key från Swedavias developer portal (https://apideveloper.swedavia.se)",
                "api_key_secondary_desc": "Secondary key (valfritt men rekommenderat för automatisk failover vid key rotation)",
                "hours_back_desc": "Antal timmar bakåt i tiden att visa flyg för",
                "hours_ahead_desc": "Antal timmar framåt i tiden att visa flyg för",
            },
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
