# home-assistant-aquahawk

[![GitHub Release][releases-shield]][releases]
[![hacs][hacsbadge]][hacs]

This custom component for Home Assistant adds support for for reading water usage data from AquaHawk.

## Installation instruction

### HACS

The easiest way to install this integration is with [HACS][hacs]. First, install [HACS][hacs-download] if you don't have it yet. In Home Assistant, go to `HACS -> Integrations`, click on `+ Explore & Download Repositories`, search for `AquaHawk`, and click download. After download, restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ablyler&repository=home-assistant-aquahawk&category=integration)

Once the integration is installed, you can add it to the Home Assistant by going to `Configuration -> Devices & Services`, clicking `+ Add Integration` and searching for `AquaHawk` or, using My Home Assistant service, you can click on:

[![Add AquaHawk][add-integration-badge]][add-integration]

### Manual installation

1. Update Home Assistant to version 2021.12 or newer.
2. Clone this repository.
3. Copy the `custom_components/aquahawk` folder into your Home Assistant's `custom_components` folder.

### Configuring

1. Add `AquaHawk` integration via UI.
2. Enter AquaHawk cloud hostname, account id, username, and password.

## Known issues

- Sensor values are delayed due to the infrequent sending of data from the water meters to the cloud. The delay is usually many hours to a day in my experience.

## Supported entities

This custom component creates following entities for each discovered dehumidifier:

| Platform | Description                       |
| -------- | --------------------------------- |
| `sensor` | Sensor for water usage today.     |
| `sensor` | Sensor for water usage this year. |

## Energy dashboard

This integration supports energy dashboard. To enable it, go to `Settings -> Dashboards -> Energy`, click on `Add Water Source`, and select `AquaHawk Yearly` (using the daily sensor will not work correctly). Once added, you can see water usage in the energy dashboard.

## Troubleshooting

If there are problems while using integration setup, an advanced debug logging can be activated via `Advanced settings` page.

Once activated, logs can be see by clicking at:

Select `Load Full Home Assistant Log` to see all debug mode logs. Please include as much logs as possible if you open an [issue](https://github.com/ablyler/home-assistant-aquahawk/issues/new?assignees=&labels=&template=issue.md).

[![Home Assistant Logs][ha-logs-badge]][ha-logs]

Debug logging can be activated without going through setup process:

[![Logging service][ha-service-badge]][ha-service]

On entry page, paste following content:

```yaml
service: logger.set_level
data:
  custom_components.aquahawk: DEBUG
```

It is possible to activate debug logging on Home Assistent start. To do this, open Home Assistant's `configuration.yaml` file on your machine, and add following to `logger` configuration:

```yaml
logger:
  # Begging of lines to add
  logs:
    custom_components.aquahawk: debug
  # End of lines to add
```

Home Assistant needs to be restarted after this change.

## Notice

AquaHawk and other names are trademarks of their respective owners.

[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=aquahawk
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
[hacs]: https://hacs.xyz
[hacs-download]: https://hacs.xyz/docs/setup/download
[hacsbadge]: https://img.shields.io/badge/HACS-Default-blue.svg?style=flat
[ha-logs]: https://my.home-assistant.io/redirect/logs
[ha-logs-badge]: https://my.home-assistant.io/badges/logs.svg
[ha-service]: https://my.home-assistant.io/redirect/developer_call_service/?service=logger.set_level
[ha-service-badge]: https://my.home-assistant.io/badges/developer_call_service.svg
[releases-shield]: https://img.shields.io/github/release/ablyler/home-assistant-aquahawk.svg?style=flat
[releases]: https://github.com/ablyler/home-assistant-aquahawk/releases
