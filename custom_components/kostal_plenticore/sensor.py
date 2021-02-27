"""Kostal Plenticore Inverter."""

import logging

import kostalplenticore
import voluptuous as vol
import json

from homeassistant.exceptions import PlatformNotReady
from homeassistant.components.sensor import PLATFORM_SCHEMA
from .const import (
    CONF_DCINPUTS, 
    CONF_DCINPUTS_DEFAULT, 
    SENSOR_TYPES, 
    SENSORS_DC2, 
    SENSORS_DC3
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_PASSWORD,
    ENERGY_KILO_WATT_HOUR
)

"""Platform for sensor integration."""

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_DCINPUTS, default=CONF_DCINPUTS_DEFAULT): vol.In([1, 2, 3]),
        vol.Optional(CONF_MONITORED_CONDITIONS, default=[]): vol.All(
            cv.ensure_list, [vol.In({**SENSOR_TYPES, **SENSORS_DC2, **SENSORS_DC3})]
        ),
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    host = config[CONF_HOST]
    password = config[CONF_PASSWORD]
    monitoredcondition = config[CONF_MONITORED_CONDITIONS]

    """ Login to Kostal Plenticore """
    try:
        con = kostalplenticore.connect(host, password)
        con.login()
    except Exception as e:
        _LOGGER.warning('Could not connect to kostal plenticore %s: %s', host, str(e))
        raise PlatformNotReady

    """ All sensors """
    allSensors = {**SENSOR_TYPES, **SENSORS_DC2, **SENSORS_DC3}

    """ If there're no monitored conditions use all possible values """
    if len(monitoredcondition) == 0:
    	if(config[CONF_DCINPUTS] == 2):
    	    monitoredcondition = {**SENSOR_TYPES, **SENSORS_DC2}
    	elif(config[CONF_DCINPUTS] == 3):
    		monitoredcondition = allSensors
    	else:
        	monitoredcondition = SENSOR_TYPES.keys()
    else:
        """ Remove keys that do not match dccount """
        if(config[CONF_DCINPUTS] < 3):
            for dc3sensorKey in SENSORS_DC3.keys():
                if(dc3sensorKey in monitoredcondition):
                	_LOGGER.warning('Ignoring monitored condition %s due to dc_inputs: %d', dc3sensorKey, config[CONF_DCINPUTS])
                	monitoredcondition.remove(dc3sensorKey)
        if(config[CONF_DCINPUTS] < 2):
            for dc2sensorKey in SENSORS_DC2.keys():
                if(dc3sensorKey in monitoredcondition):
                	monitoredcondition.remove(dc2sensorKey)
                	_LOGGER.warning('Ignoring monitored condition %s due to dc_inputs: %d', dc2sensorKey, config[CONF_DCINPUTS])


    for sensor in monitoredcondition:
        add_entities(
            [
                plenticore(
                    con,
                    allSensors[sensor][2],
                    allSensors[sensor][0],
                    allSensors[sensor][1],
                    allSensors[sensor][3],
                    allSensors[sensor][4],
                    config,
                )
            ]
        )


class plenticore(Entity):
    """Representation of a Sensor."""

    def getData(self):
        """Get sensor data."""
        if self.moduleid == "pvcombined":
            dccount = self.config[CONF_DCINPUTS]
            try:
                pv1 = int(
                    self.api.getProcessdata("devices:local:pv1", [self.id])[0]["value"]
                )
            except:
                pv1 = "error"

            try:
                pv2 = 0
                if(dccount > 1):
                    pv2 = int(
                        self.api.getProcessdata("devices:local:pv2", [self.id])[0]["value"]
                    )
            except:
                pv2 = "error"

            try:
                pv3 = 0
                if(dccount > 2):
                    pv3 = int(
                        self.api.getProcessdata("devices:local:pv3", [self.id])[0]["value"]
                    )
            except:
                pv3 = "error"

            if(pv1 != "error" and pv2 != "error" and pv3 != "error"):
                value = pv1 + pv2 + pv3
            else:
                value= "error"

        elif (
            self.id == "Frequency"
            or self.id == "L3_I"
            or self.id == "L2_I"
            or self.id == "L1_I"
        ):
            try:
                value = (
                    "%.2f" % self.api.getProcessdata(self.moduleid, [self.id])[0]["value"]
                    )
            except:
                value = "error"
        elif (self.id == "ProductName"):
            try:
                settingsVals = self.api.getSettings(self.moduleid, ["Branding:ProductName1", "Branding:ProductName2"])
                value = settingsVals[0]["value"] + " " + settingsVals[1]["value"]
                value = value.strip()
            except:
                value = "error"
        
        elif (
            self.id == "Properties:SerialNo"
            or self.id == "Properties:ArtNo"
        ):
            try:
                value = self.api.getSettings(self.moduleid, [self.id])[0]["value"]
            except:
                value = "error"        
        elif (
            self.id == "Battery:MinSoc"
            or self.id == "Battery:SmartBatteryControl:Enable"
            ):
            try:
                value = int(
                    self.api.getSettings(self.moduleid, [self.id])[0]["value"]
                )
            except:
                value = "error"
        elif self._unit_of_measurement == ENERGY_KILO_WATT_HOUR:
            try:
                value = "%.2f" % (
                    self.api.getProcessdata(self.moduleid, [self.id])[0]["value"] / 1000
                )
            except:
                value = "error"
        else:
            try:
                value = int(
                    self.api.getProcessdata(self.moduleid, [self.id])[0]["value"]
                )
            except:
                value = "error"
        return value

    def __init__(self, apiConnection, sensorname, moduleid, id, unit, icon, config):
        """Initialize the sensor."""
        self.api = apiConnection
        self.sensorname = sensorname
        self.moduleid = moduleid
        self.id = id
        self.mdi = icon
        self._unit_of_measurement = unit
        self.config = config
        value = self.getData()
        if(value != "error"):
            self._state = value
            self._available = True
        else:
            self._available = False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.sensorname

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.mdi

    @property
    def state(self):
        """Return State."""
        return self._state

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._available

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """
        Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        value = self.getData()
        if(value != "error"):
            self._state = value
            self._available = True
        else:
            self._available = False
