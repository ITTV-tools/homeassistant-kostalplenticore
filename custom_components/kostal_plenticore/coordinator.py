"""Provides the kostalplenticore DataUpdateCoordinator."""
from datetime import timedelta
import logging
import requests
import json

from async_timeout import timeout
from homeassistant.util.dt import utcnow
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import kostalplenticore

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)



class KostalDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MYPV data."""

    def __init__(self, hass: HomeAssistantType, *, config: dict, options: dict):
        """Initialize global kostalplenticore data updater."""
        self._host = config[CONF_HOST]
        self._password = config[CONF_PASSWORD]
        #self._info = None
        #self._setup = None
        self._next_update = 0
        update_interval = timedelta(seconds=10)
        try:
            con = kostalplenticore.connect(self._host, self._password)
            con.login()
            _LOGGER.error(con.getBatteryPercent())
        except requests.exceptions.ConnectTimeout as err:
            _LOGGER.debug("Connection to %s timed out", self._host)
            raise ConfigEntryNotReady from err
        except ConnectionError as err:
            _LOGGER.debug("ClientConnectionError to %s", self._host)
            raise ConfigEntryNotReady from err
        except Exception:  # pylint: disable=broad-except
            _LOGGER.error("Unexpected error creating device %s", self._host)
            return None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""

        def _update_data() -> dict:
            con.getBatteryPercent()

            return True

        try:
            async with timeout(4):
                return await self.hass.async_add_executor_job(_update_data)
        except Exception as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
