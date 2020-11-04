"""The kostal_plenticore integration."""
import asyncio
import logging
import voluptuous as vol
from datetime import timedelta
import requests
from async_timeout import timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import HomeAssistant
from .const import DOMAIN, SENSOR_TYPES
import kostalplenticore
_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the kostal_plenticore component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up kostal_plenticore from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    """ Login to Kostal Plenticore """
    #try:
    #    con = kostalplenticore.connect(entry.data['host'], entry.data['password'])
    #    con.login()
    #except Exception as err:
    #    _LOGGER.error('Could not connect to kostal plenticore, please restart HA')
    async def async_update_data():
        _LOGGER.info('Test')
        return True

    api = hass.async_create_task(api_setup(
        hass,
        entry.data['host'],
        entry.data['password'],
        )
    )
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=30),
    )
    hass.data[DOMAIN] = {
        coordinator: coordinator
    }
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def api_setup(hass, host, password):
    """Create a instance only once."""

    #session = hass.helpers.aiohttp_client.async_get_clientsession()
    try:
        con = kostalplenticore.connect(host, password)
        con.login()
        _LOGGER.error(con.getBatteryPercent())
    except requests.exceptions.ConnectTimeout as err:
        _LOGGER.debug("Connection to %s timed out", host)
        raise ConfigEntryNotReady from err
    except ConnectionError as err:
        _LOGGER.debug("ClientConnectionError to %s", host)
        raise ConfigEntryNotReady from err
    except Exception:  # pylint: disable=broad-except
        _LOGGER.error("Unexpected error creating device %s", host)
        return None


    return con
