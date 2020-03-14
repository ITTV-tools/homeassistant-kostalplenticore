import kostalplenticore
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
"""Platform for sensor integration."""
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD
)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    host = config[CONF_HOST]
    password = config[CONF_PASSWORD]

    """ Login to Kostal Plenticore """
    con = kostalplenticore.connect(host, password)
    con.login()

    add_entities([plenticore(con, "Kostal Battery", "devices:local:battery", "SoC", "%")])
    add_entities([plenticore(con, "Kostal HomeGridPower", "devices:local", "HomeGrid_P", "W")])


class plenticore(Entity):
    """Representation of a Sensor."""

    def __init__(self, con, sensorname, moduleid, id, unit):
        """Initialize the sensor."""
        self.api = con
        self.sensorname = sensorname
        self.moduleid = moduleid
        self.id = id
        self.unit = unit
        self._state = int(self.api.getProcessdata(self.moduleid, [self.id])[0]["value"])

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.sensorname

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self.unit

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        #self._state = 23
        self._state = int(self.api.getProcessdata(self.moduleid, [self.id])[0]["value"])
