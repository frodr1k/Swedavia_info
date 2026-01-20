"""Swedavia Flight Information API Client."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
import logging
from typing import Any, TYPE_CHECKING

import aiohttp
import async_timeout

from .const import API_BASE_URL, API_TIMEOUT

if TYPE_CHECKING:
    from .api_counter import APICallCounter

_LOGGER = logging.getLogger(__name__)


class SwedaviaAPIError(Exception):
    """Base exception for Swedavia API errors."""


class SwedaviaAPIConnectionError(SwedaviaAPIError):
    """Exception for connection errors."""


class SwedaviaAPIRateLimitError(SwedaviaAPIError):
    """Exception for rate limit errors."""


class SwedaviaFlightAPI:
    """Swedavia Flight Information API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_key: str | None = None,
        api_key_secondary: str | None = None,
        api_counter: APICallCounter | None = None,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._api_key = api_key
        self._api_key_secondary = api_key_secondary
        self._current_key = api_key  # Start with primary key
        self._last_request_time = None
        self._min_request_interval = 1  # Minimum 1 second between requests
        self._api_counter = api_counter

    async def _rate_limit(self) -> None:
        """Implement rate limiting."""
        if self._last_request_time:
            time_since_last = datetime.now() - self._last_request_time
            if time_since_last.total_seconds() < self._min_request_interval:
                await asyncio.sleep(
                    self._min_request_interval - time_since_last.total_seconds()
                )
        self._last_request_time = datetime.now()

    async def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a request to the Swedavia API."""
        await self._rate_limit()

        # Increment API counter
        if self._api_counter:
            await self._api_counter.increment()

        url = f"{API_BASE_URL}/{endpoint}"
        headers = {
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-SwedaviaFlights/1.0",
        }
        
        # Add subscription key if provided
        if self._current_key:
            headers["Ocp-Apim-Subscription-Key"] = self._current_key

        _LOGGER.debug("Requesting %s with params %s", url, params)

        try:
            async with async_timeout.timeout(API_TIMEOUT):
                async with self._session.get(
                    url, headers=headers, params=params
                ) as response:
                    if response.status == 401:
                        # Invalid API key - try secondary key if available
                        if (
                            self._api_key_secondary
                            and self._current_key != self._api_key_secondary
                        ):
                            _LOGGER.warning(
                                "Primary API key failed (401), trying secondary key"
                            )
                            self._current_key = self._api_key_secondary
                            headers["Ocp-Apim-Subscription-Key"] = self._current_key
                            
                            # Retry with secondary key
                            async with self._session.get(
                                url, headers=headers, params=params
                            ) as retry_response:
                                if retry_response.status == 401:
                                    raise SwedaviaAPIError(
                                        "API authentication failed with both primary and secondary keys. "
                                        "Please update your API keys from https://apideveloper.swedavia.se/"
                                    )
                                if retry_response.status != 200 and retry_response.status != 204:
                                    text = await retry_response.text()
                                    _LOGGER.error(
                                        "API request failed with status %s: %s",
                                        retry_response.status,
                                        text,
                                    )
                                    raise SwedaviaAPIError(
                                        f"API request failed with status {retry_response.status}"
                                    )
                                
                                if retry_response.status == 204:
                                    return {}
                                
                                return await retry_response.json()
                        else:
                            raise SwedaviaAPIError(
                                "API authentication failed. Invalid subscription key. "
                                "Please update your API key from https://apideveloper.swedavia.se/"
                            )
                    
                    if response.status == 429:
                        raise SwedaviaAPIRateLimitError(
                            "API rate limit exceeded"
                        )
                    
                    if response.status == 204:
                        # No content - no flights available
                        return {}
                    
                    if response.status != 200:
                        text = await response.text()
                        _LOGGER.error(
                            "API request failed with status %s: %s",
                            response.status,
                            text,
                        )
                        raise SwedaviaAPIError(
                            f"API request failed with status {response.status}"
                        )

                    return await response.json()

        except asyncio.TimeoutError as err:
            raise SwedaviaAPIConnectionError(
                "Timeout connecting to Swedavia API"
            ) from err
        except aiohttp.ClientError as err:
            raise SwedaviaAPIConnectionError(
                f"Error connecting to Swedavia API: {err}"
            ) from err

    async def get_arrivals(
        self, airport_iata: str, date: str | None = None
    ) -> dict[str, Any]:
        """Get arrivals for an airport."""
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        endpoint = f"{airport_iata}/arrivals/{date}"
        return await self._request(endpoint)

    async def get_departures(
        self, airport_iata: str, date: str | None = None
    ) -> dict[str, Any]:
        """Get departures for an airport."""
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        endpoint = f"{airport_iata}/departures/{date}"
        return await self._request(endpoint)

    async def get_flights_by_date_range(
        self,
        airport_iata: str,
        flight_type: str,
        hours_back: int = 0,
        hours_ahead: int = 24,
    ) -> list[dict[str, Any]]:
        """Get flights within a date range."""
        flights = []
        now = datetime.now(timezone.utc)
        today = now.date()
        
        # Calculate date range
        start_date = today - timedelta(hours=hours_back) if hours_back > 0 else today
        end_date = today + timedelta(hours=hours_ahead) if hours_ahead > 0 else today
        
        # Get flights for each date in range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            
            try:
                if flight_type == "arrivals":
                    data = await self.get_arrivals(airport_iata, date_str)
                else:
                    data = await self.get_departures(airport_iata, date_str)
                
                if data and "flights" in data:
                    flights.extend(data["flights"])
                    
            except SwedaviaAPIError as err:
                _LOGGER.warning(
                    "Failed to get %s for %s on %s: %s",
                    flight_type,
                    airport_iata,
                    date_str,
                    err,
                )
            
            current_date += timedelta(days=1)
        
        # Filter by time window
        now = datetime.now(timezone.utc)
        filtered_flights = []
        
        for flight in flights:
            # Get the relevant time field
            if flight_type == "arrivals":
                time_data = flight.get("arrivalTime", {})
            else:
                time_data = flight.get("departureTime", {})
            
            # Try to get the most accurate time
            time_str = (
                time_data.get("actualUtc")
                or time_data.get("estimatedUtc")
                or time_data.get("scheduledUtc")
            )
            
            if time_str:
                try:
                    flight_time = datetime.fromisoformat(
                        time_str.replace("Z", "+00:00")
                    )
                    
                    # Check if within time window
                    time_diff = (flight_time - now).total_seconds() / 3600
                    if -hours_back <= time_diff <= hours_ahead:
                        filtered_flights.append(flight)
                        
                except (ValueError, AttributeError) as err:
                    _LOGGER.debug("Failed to parse time %s: %s", time_str, err)
        
        return filtered_flights

    async def validate_connection(self, airport_iata: str) -> bool:
        """Validate the API connection and airport code."""
        try:
            await self.get_departures(airport_iata)
            return True
        except SwedaviaAPIError:
            return False
