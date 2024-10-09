"""Platform for BinarySensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Import the device class from the component that you want to support
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
#     {
#         vol.Required(CONF_HOST): cv.string,
#         vol.Optional(CONF_USERNAME, default="admin"): cv.string,
#         vol.Optional(CONF_PASSWORD): cv.string,
#     }
# )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up homelink from a config entry."""
    device_info = DeviceInfo(
        identifiers={
            # Serial numbers are unique identifiers within a specific domain
            (DOMAIN, "ABC-123")
        },
        name="Superdevice",
    )

    async_add_entities(
        [
            HomelinkBinarySensor("Button 1", device_info),
            HomelinkBinarySensor("Button 2", device_info),
            HomelinkBinarySensor("Button 3", device_info),
        ]
    )


class HomelinkBinarySensor(BinarySensorEntity):
    """Binary sensor."""

    def __init__(self, name, device_info) -> None:
        """Initialize the button."""

        self.name = name
        self.unique_id = f"{DOMAIN}.{name}"
        self.device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return True
