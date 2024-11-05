"""Platform for BinarySensor integration."""

from __future__ import annotations

from datetime import timedelta
import logging
import time

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

# Import the device class from the component that you want to support
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=5)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up homelink from a config entry."""
    coordinator = config_entry.runtime_data["coordinator"]
    provider = config_entry.runtime_data["provider"]

    await provider.enable()

    device_data = await provider.discover()

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
            [
                HomelinkBinarySensor(b.id, b.name, device_info, coordinator)
                for b in device.buttons
            ]
        )


class HomelinkBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor."""

    def __init__(self, id, name, device_info, coordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator, context=id)
        self.id = id
        self.name = name
        self.unique_id = f"{DOMAIN}.{id}"
        self.device_info = device_info
        self.on = False
        self.last_request_id = None

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.on

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update this button."""
        if self.id not in self.coordinator.data:
            self.on = False
        else:
            latest_update = self.coordinator.data[self.id]
            self.on = (time.time() - latest_update["timestamp"]) < 10 and latest_update[
                "requestId"
            ] != self.last_request_id
            self.last_request_id = latest_update["requestId"]
        logging.info(
            "%(button_name)s:%(button_state)s",
            extra={"button_name": self.name, "button_state": self.on},
        )
        self.async_write_ha_state()
