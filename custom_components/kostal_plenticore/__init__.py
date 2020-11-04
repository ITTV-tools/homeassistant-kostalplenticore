"""The kostal_plenticore integration."""
import asyncio
import logging
import voluptuous as vol
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from .const import DOMAIN, SENSOR_TYPES, DATA_COORDINATOR
from .coordinator import KostalDataUpdateCoordinator
_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


PLATFORMS = ["sensor"]


async def async_setup(hass, config):
    """Platform setup, do nothing."""
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN not in config:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=dict(config[DOMAIN])
        )
    )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up kostal_plenticore from a config entry."""

    coordinator = KostalDataUpdateCoordinator(
        hass,
        config=entry.data,
        options=entry.options,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_COORDINATOR: coordinator,
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
