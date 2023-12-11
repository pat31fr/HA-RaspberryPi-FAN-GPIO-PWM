"""Support for Fan that can be controlled using PWM."""
from __future__ import annotations

import logging

from gpiozero import PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory

import voluptuous as vol

from homeassistant.components.fan import (
    ATTR_PERCENTAGE,
    PLATFORM_SCHEMA,
    SUPPORT_SET_SPEED,
    FanEntity,
)
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, STATE_ON, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

CONF_FANS = "fans"
CONF_PIN = "pin"

DEFAULT_PERCENTAGE = 100

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888

SUPPORT_SIMPLE_FAN = SUPPORT_SET_SPEED

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FANS): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required(CONF_NAME): cv.string,
                    vol.Required(CONF_PIN): cv.positive_int,
                    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                    vol.Optional(CONF_UNIQUE_ID): cv.string
               }
            ],
        )
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the PWM FAN."""
    fans = []
    for fan_conf in config[CONF_FANS]:
        pin = fan_conf[CONF_PIN]
        opt_args = {}
        opt_args["pin_factory"] = PiGPIOFactory(host=fan_conf[CONF_HOST], port= fan_conf[CONF_PORT])
        fan = PwmSimpleFan(PWMOutputDevice(pin, **opt_args), fan_conf[CONF_NAME],led_conf.get(CONF_UNIQUE_ID))
        fans.append(fan)

    add_entities(fans)


class PwmSimpleFan(FanEntity, RestoreEntity):
    """Representation of a simple PWM FAN."""

    def __init__(self, fan, name, unique_id=None):
        """Initialize PWM FAN."""
        self._fan = fan
        self._name = name
        self._is_on = False
        self._percentage = DEFAULT_PERCENTAGE
        self._attr_unique_id = unique_id

    async def async_added_to_hass(self):
        """Handle entity about to be added to hass event."""
        await super().async_added_to_hass()
        if last_state := await self.async_get_last_state():
            self._is_on = last_state.state == STATE_ON
            self._percentage = last_state.attributes.get(
                "percentage", DEFAULT_PERCENTAGE
            )

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the group."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._is_on

    @property
    def percentage(self):
        """Return the percentage property."""
        return self._percentage

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_SIMPLE_FAN

    def turn_on(self, percentage: Optional[int] = None, preset_mode: Optional[str] = None, **kwargs: Any) -> None:
        """Turn on the fan."""
        if percentage != None:
            self._percentage = percentage
        elif ATTR_PERCENTAGE in kwargs:
            self._percentage = kwargs[ATTR_PERCENTAGE]
        self._fan.value = self._percentage / 100
        self._is_on = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the fan off."""
        if self.is_on:
            self._fan.off()
        self._is_on = False
        self.schedule_update_ha_state()

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        self._percentage = percentage
        self._fan.value = self._percentage / 100
        self._is_on = True
        self.schedule_update_ha_state()
