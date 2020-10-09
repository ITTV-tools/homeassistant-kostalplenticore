"""Kostal Plenticore Inverter."""

import logging

import kostalplenticore
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_PASSWORD,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    MASS_GRAMS,
    FREQUENCY_HERTZ,
    ELECTRICAL_CURRENT_AMPERE,
    VOLT,
    PERCENTAGE,
    POWER_WATT,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

"""Platform for sensor integration."""

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "BatteryPercent": [
        "devices:local:battery",
        "SoC",
        "kostal battery",
        PERCENTAGE,
        "mdi:battery-high",
    ],
    "BatteryCycles": [
        "devices:local:battery",
        "Cycles",
        "kostal battery cycles",
        None,
        "mdi:recycle",
    ],
    "BatteryPower": [
        "devices:local:battery",
        "P",
        "kostal battery power",
        POWER_WATT,
        "mdi:recycle",
    ],
    "HomeOwnPower": [
        "devices:local",
        "Home_P",
        "kostal home power",
        POWER_WATT,
        "mdi:home",
    ],
    "HomePVPower": [
        "devices:local",
        "HomePv_P",
        "kostal home power from PV",
        POWER_WATT,
        "mdi:solar-power",
    ],
    "HomeBatteryPower": [
        "devices:local",
        "HomeBat_P",
        "Kostal home power from battery",
        POWER_WATT,
        "mdi:battery-charging-90",
    ],
    "HomeGridPower": [
        "devices:local",
        "HomeGrid_P",
        "Kostal home power from grid",
        POWER_WATT,
        "mdi:transmission-tower",
    ],
    "GridPower": [
        "devices:local",
        "Grid_P",
        "Kostal power grid",
        POWER_WATT,
        "mdi:transmission-tower",
    ],
    "PV1Power": [
        "devices:local:pv1",
        "P",
        "Kostal pv1 power",
        POWER_WATT,
        "mdi:solar-power",
    ],
    "PV1Voltage": [
        "devices:local:pv1",
        "U",
        "Kostal pv1 voltage",
        VOLT,
        "mdi:solar-power",
    ],
    "PV1Current": [
        "devices:local:pv1",
        "I",
        "Kostal pv1 current",
        ELECTRICAL_CURRENT_AMPERE,
        "mdi:solar-power",
    ],
    "PV2Power": [
        "devices:local:pv2",
        "P",
        "Kostal pv2 power",
        POWER_WATT,
        "mdi:solar-power",
    ],
    "PV2Voltage": [
        "devices:local:pv2",
        "U",
        "Kostal pv2 voltage",
        VOLT,
        "mdi:solar-power",
    ],
    "PV2Current": [
        "devices:local:pv2",
        "I",
        "Kostal pv2 current",
        ELECTRICAL_CURRENT_AMPERE,
        "mdi:solar-power",
    ],
    "PVPower": ["pv1+2", "P", "Kostal pv power", POWER_WATT, "mdi:solar-power"],
    "DCPower": [
        "devices:local",
        "Dc_P",
        "Kostal DC power",
        POWER_WATT,
        "mdi:power-cycle",
    ],
    "AutarkyDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:Autarky:Day",
        "Kostal autarky day",
        PERCENTAGE,
        "mdi:power-plug",
    ],
    "AutarkyMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:Autarky:Month",
        "Kostal autarky Month",
        PERCENTAGE,
        "mdi:power-plug",
    ],
    "AutarkyTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:Autarky:Total",
        "Kostal autarky Total",
        PERCENTAGE,
        "mdi:power-plug",
    ],
    "AutarkyYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:Autarky:Year",
        "Kostal autarky Year",
        PERCENTAGE,
        "mdi:power-plug",
    ],
    "HomeConsumptionDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHome:Day",
        "Kostal Home consumption Day",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHome:Month",
        "Kostal Home consumption Month",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHome:Total",
        "Kostal Home consumption Total",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHome:Year",
        "Kostal Home consumption Year",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromBatDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeBat:Day",
        "Kostal Home consumption from Battery Day",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromBatMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeBat:Month",
        "Kostal Home consumption from Battery Month",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromBatTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeBat:Total",
        "Kostal Home consumption from Battery Total",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromBatYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeBat:Year",
        "Kostal Home consumption from Battery Year",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromGridDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeGrid:Day",
        "Kostal Home consumption from Grid Day",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromGridMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeGrid:Month",
        "Kostal Home consumption from Grid Month",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromGridTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeGrid:Total",
        "Kostal Home consumption from Grid Total",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromGridYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomeGrid:Year",
        "Kostal Home consumption from Grid Year",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromPVDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomePv:Day",
        "Kostal Home consumption from PV Day",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromPVMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomePv:Month",
        "Kostal Home consumption from PV Month",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromPVTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomePv:Total",
        "Kostal Home consumption from PV Total",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionFromPVYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:EnergyHomePv:Year",
        "Kostal Home consumption from PV Year",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionYieldDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:Yield:Day",
        "Kostal Yield Day",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionYieldMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:Yield:Month",
        "Kostal Yield Month",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionYieldTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:Yield:Total",
        "Kostal Yield Total",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "HomeConsumptionYieldYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:Yield:Year",
        "Kostal Yield Year",
        ENERGY_KILO_WATT_HOUR,
        "mdi:power-plug",
    ],
    "CO2SavingDay": [
        "scb:statistic:EnergyFlow",
        "Statistic:CO2Saving:Day",
        "Kostal CO2 Saving Day",
        MASS_GRAMS,
        "mdi:molecule-co2",
    ],
    "CO2SavingMonth": [
        "scb:statistic:EnergyFlow",
        "Statistic:CO2Saving:Month",
        "Kostal CO2 Saving Month",
        MASS_GRAMS,
        "mdi:molecule-co2",
    ],
    "CO2SavingTotal": [
        "scb:statistic:EnergyFlow",
        "Statistic:CO2Saving:Total",
        "Kostal CO2 Saving Total",
        MASS_GRAMS,
        "mdi:molecule-co2",
    ],
    "CO2SavingYear": [
        "scb:statistic:EnergyFlow",
        "Statistic:CO2Saving:Year",
        "Kostal CO2 Saving Year",
        MASS_GRAMS,
        "mdi:molecule-co2",
    ],
    "ACFrequency": [
        "devices:local:ac",
        "Frequency",
        "Kostal Frequency",
        FREQUENCY_HERTZ,
        "mdi:power-plug",
    ],
    "ACL1Current": [
        "devices:local:ac",
        "L1_I",
        "Kostal L1 Current",
        ELECTRICAL_CURRENT_AMPERE,
        "mdi:power-plug",
    ],
    "ACL1Power": [
        "devices:local:ac",
        "L1_P",
        "Kostal L1 Power",
        POWER_WATT,
        "mdi:power-plug",
    ],
    "ACL1Voltage": [
        "devices:local:ac",
        "L1_U",
        "Kostal L1 Voltage",
        VOLT,
        "mdi:power-plug",
    ],
    "ACL2Current": [
        "devices:local:ac",
        "L2_I",
        "Kostal L2 Current",
        ELECTRICAL_CURRENT_AMPERE,
        "mdi:power-plug",
    ],
    "ACL2Power": [
        "devices:local:ac",
        "L2_P",
        "Kostal L2 Power",
        POWER_WATT,
        "mdi:power-plug",
    ],
    "ACL2Voltage": [
        "devices:local:ac",
        "L2_U",
        "Kostal L2 Voltage",
        VOLT,
        "mdi:power-plug",
    ],
    "ACL3Current": [
        "devices:local:ac",
        "L3_I",
        "Kostal L3 Current",
        ELECTRICAL_CURRENT_AMPERE,
        "mdi:power-plug",
    ],
    "ACL3Power": [
        "devices:local:ac",
        "L3_P",
        "Kostal L3 Power",
        POWER_WATT,
        "mdi:power-plug",
    ],
    "ACL3Voltage": [
        "devices:local:ac",
        "L3_U",
        "Kostal L3 Voltage",
        VOLT,
        "mdi:power-plug",
    ],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_MONITORED_CONDITIONS, default=[]): vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    host = config[CONF_HOST]
    password = config[CONF_PASSWORD]
    monitoredcondition = config[CONF_MONITORED_CONDITIONS]

    """ Login to Kostal Plenticore """
    con = kostalplenticore.connect(host, password)
    con.login()
    if len(monitoredcondition) == 0:
        monitoredcondition = SENSOR_TYPES.keys()
    for sensor in monitoredcondition:
        add_entities(
            [
                plenticore(
                    con,
                    SENSOR_TYPES[sensor][2],
                    SENSOR_TYPES[sensor][0],
                    SENSOR_TYPES[sensor][1],
                    SENSOR_TYPES[sensor][3],
                    SENSOR_TYPES[sensor][4],
                )
            ]
        )


class plenticore(Entity):
    """Representation of a Sensor."""

    def getData(self):
        """Get sensor data."""
        if self.moduleid == "pv1+2":
            pv1 = int(
                self.api.getProcessdata("devices:local:pv1", [self.id])[0]["value"]
            )
            pv2 = int(
                self.api.getProcessdata("devices:local:pv2", [self.id])[0]["value"]
            )
            value = pv1 + pv2
        elif (
            self.id == "Frequency"
            or self.id == "L3_I"
            or self.id == "L2_I"
            or self.id == "L1_I"
        ):
            value = (
                "%.2f" % self.api.getProcessdata(self.moduleid, [self.id])[0]["value"]
            )
        elif self._unit_of_measurement == ENERGY_KILO_WATT_HOUR:
            try:
                value = "%.2f" % (
                    self.api.getProcessdata(self.moduleid, [self.id])[0]["value"] / 1000
                )
            except:
                value = 0
        else:
            try:
                value = int(
                    self.api.getProcessdata(self.moduleid, [self.id])[0]["value"]
                )
            except:
                value = 0
        return value

    def __init__(self, con, sensorname, moduleid, id, unit, icon):
        """Initialize the sensor."""
        self.api = con
        self.sensorname = sensorname
        self.moduleid = moduleid
        self.id = id
        self.mdi = icon
        self._unit_of_measurement = unit
        self._state = self.getData()

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
        return True

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # self._state = 23
        self._state = self.getData()
