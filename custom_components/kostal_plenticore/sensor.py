"""Kostal Sensors integration."""

import logging
from homeassistant.const import CONF_MONITORED_CONDITIONS
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from .const import SENSOR_TYPES, DOMAIN, CONF_MONITORED_CONDITIONS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Add Sensor entry."""
    #coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    #for sensor in entry.data[CONF_MONITORED_CONDITIONS]:
    #    entities.append(MypvDevice(coordinator, sensor, entry.title))
    #async_add_entities(entities)
