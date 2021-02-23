# homeassistant-kostalplenticore

Home Assistant Component for Kostal Plenticore

<a href="https://www.buymeacoffee.com/ittv" target="_blank"><img height="41px" width="167px" src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee"></a>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

### Installation

Copy this folder to `<config_dir>/custom_components/kostal_plenticore/`.

### HACS
Search for Kostal Plenticore

### Configuration

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
    - platform: kostal_plenticore
      host: <IP>
      password: <Password>
      DC_Inputs: 2 #Optional Default 2 (2,3)
      monitored_conditions:
        - BatteryPercent
        - BatteryCycles
        - BatteryPower
        - HomeGridPower
        - HomeOwnPower
        - HomePVPower
        - HomeBatteryPower
        - GridPower
        - DCPower
        - PVPower
        - AutarkyDay
        - AutarkyMonth
        - AutarkyTotal
        - AutarkyYear
        - CO2SavingDay
        - CO2SavingMonth
        - CO2SavingTotal
        - CO2SavingYear
        - PV1Power
        - PV1Voltage
        - PV1Current
        - PV2Power
        - PV2Voltage
        - PV2Current
        - PV3Power
        - PV3Voltage
        - PV3Current
        - ACFrequency
        - ACL1Current
        - ACL1Power
        - ACL1Voltage
        - ACL2Current
        - ACL2Power
        - ACL2Voltage
        - ACL3Current
        - ACL3Power
        - ACL3Voltage
        - HomeConsumptionDay
        - HomeConsumptionMonth
        - HomeConsumptionTotal
        - HomeConsumptionYear
        - HomeConsumptionFromBatDay
        - HomeConsumptionFromBatMonth
        - HomeConsumptionFromBatTotal
        - HomeConsumptionFromBatYear
        - HomeConsumptionFromGridDay
        - HomeConsumptionFromGridMonth
        - HomeConsumptionFromGridTotal
        - HomeConsumptionFromGridYear
        - HomeConsumptionFromPVDay
        - HomeConsumptionFromPVMonth
        - HomeConsumptionFromPVTotal
        - HomeConsumptionFromPVYear
        - HomeConsumptionYieldDay
        - HomeConsumptionYieldMonth
        - HomeConsumptionYieldTotal
        - HomeConsumptionYieldYear
        - OwnConsumptionRateDay
        - OwnConsumptionRateMonth
        - OwnConsumptionRateTotal
        - OwnConsumptionRateYear
        - MinSoC
        - SmartBatteryControl
        - InverterState
        - LimitEvuAbs


```
