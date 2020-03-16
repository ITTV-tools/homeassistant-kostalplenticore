# homeassistant-kostalplenticore
=================================================
Home Assistant Component for Kostal Plenticore 
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

### Installation

Copy this folder to `<config_dir>/custom_components/kostal_plenticore/`.

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
    - platform: kostal_plenticore
      host: <IP>
      password: <Password>
      monitored_conditions:
        - BatteryPercent
        - BatteryCycles
        - HomeGridPower
        - HomeOwnPower
        - HomePVPower
        - HomeBatteryPower
        - PVPower
        - AutarkyDay
        - AutarkyMonth
        - AutarkyTotal
        - AutarkyYear
        - CO2SavingDay
        - CO2SavingMonth
        - CO2SavingTotal
        - CO2SavingYear
```

[buymecoffeebadge]: "https://cdn.buymeacoffee.com/buttons/default-blue.png"
[buymecoffee]: "https://www.buymeacoffee.com/ittv"
