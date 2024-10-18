"""Platform for BinarySensor integration."""

from __future__ import annotations

import logging

from homelink.provider import Provider

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
    p = Provider(
        # TODO: URL temporarily hardcoded
        "https://d1f2mm2dg61j0w.cloudfront.net/services/v2/home-assistant/fulfillment"
    )
    await p.enable(config_entry.runtime_data)

    device_data = await p.discover(config_entry.runtime_data)

    logging.info(device_data)

    for device in device_data:
        device_info = DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, device.id)
            },
            name=device.name,
        )

        async_add_entities(
            [HomelinkBinarySensor(b.id, b.name, device_info) for b in device.buttons]
        )


class HomelinkBinarySensor(BinarySensorEntity):
    """Binary sensor."""

    def __init__(self, id, name, device_info) -> None:
        """Initialize the button."""

        self.name = name
        self.unique_id = f"{DOMAIN}.{id}"
        self.device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return True
