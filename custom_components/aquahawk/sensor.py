"""AquaHawk sensor platform."""

from datetime import timedelta
import logging

from aquahawk_client import AquaHawkClient
from homeassistant import config_entries, core
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfVolume
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
    Period,
)

_LOGGER = logging.getLogger(__name__)
# Time between updating data from AquaHawk
SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HOSTNAME): cv.string,
        vol.Required(CONF_ACCOUNT_NUMBER): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)

WATER_ICON = "mdi:water"


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    # Update our config to include new repos and remove those that have been removed.
    if config_entry.options:
        config.update(config_entry.options)
    aquahawk = AquaHawkClient(
        config.get(CONF_ACCOUNT_NUMBER),
        config.get(CONF_HOSTNAME),
        config.get(CONF_USERNAME),
        config.get(CONF_PASSWORD),
    )
    sensors = [
        AquaHawkSensor(aquahawk, Period.PERIOD_TODAY),
        AquaHawkSensor(aquahawk, Period.PERIOD_THIS_YEAR),
    ]

    async_add_entities(sensors, update_before_add=True)


class AquaHawkSensor(SensorEntity):
    """Representation of a AquaHawk usage sensor."""

    _attr_icon = WATER_ICON
    _attr_native_unit_of_measurement = UnitOfVolume.GALLONS
    _attr_state_class: SensorStateClass = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.WATER
    _attr_suggested_unit_of_measurement = UnitOfVolume.GALLONS
    _attr_suggested_display_precision = 1

    def __init__(self, aquahawk: AquaHawkClient, period: Period) -> None:
        super().__init__()
        self.aquahawk = aquahawk
        self.period = period
        self._attr_unique_id = f"aquahawk-{self.aquahawk.account_number}-{self.period}"

        if self.period == Period.PERIOD_THIS_YEAR:
            self._attr_name = f"AquaHawk Yearly (account: {aquahawk.account_number})"
        elif self.period == Period.PERIOD_TODAY:
            self._attr_name = f"AquaHawk Today (account: {aquahawk.account_number})"

        self._attr_available = True

    async def async_update(self):
        try:
            if self.period == Period.PERIOD_THIS_YEAR:
                usage = await self.aquahawk.get_usage_this_year()
            elif self.period == Period.PERIOD_TODAY:
                usage = await self.aquahawk.get_usage_today()

            # ensure usage is not None and that the last timeseries has a water_use
            if usage is None or usage.timeseries[-1].water_use is None:
                self._attr_available = False
                return

            self._attr_native_value = usage.timeseries[-1].water_use.gallons
            self._attr_available = True
        # trunk-ignore(flake8/E722)
        # trunk-ignore(ruff/E722)
        except:
            self._attr_available = False
            _LOGGER.exception("Error retrieving data from AquaHawk")
