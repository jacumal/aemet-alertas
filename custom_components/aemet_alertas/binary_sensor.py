"""Binary sensors for AEMET Alertas."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import AemetAlertEntity, area_slug


LEVELS = {
    "red": {
        "name": "Alerta roja",
        "icon": "mdi:alert-octagon",
    },
    "orange": {
        "name": "Alerta naranja",
        "icon": "mdi:alert",
    },
    "yellow": {
        "name": "Alerta amarilla",
        "icon": "mdi:alert-outline",
    },
    "green": {
        "name": "Alerta verde",
        "icon": "mdi:check-circle",
    },
}


class AemetAlertLevelSensor(
    AemetAlertEntity,
    BinarySensorEntity,
):
    """Binary sensor indicating whether an alert level is active."""

    def __init__(
        self,
        coordinator,
        level: str,
    ) -> None:
        """Initialize the binary sensor."""

        super().__init__(coordinator)

        self._level = level

        slug = area_slug(coordinator.area_name)
        level_info = LEVELS[level]

        self._attr_name = level_info["name"]
        self._attr_unique_id = (
            f"aemet_alertas_{slug}_{level}"
        )
        self._attr_icon = level_info["icon"]

    @property
    def is_on(self) -> bool:
        """Return whether this alert level is active."""

        return any(
            alert.level == self._level
            for alert in (self.coordinator.data or [])
        )

    @property
    def extra_state_attributes(self):
        """Return details for alerts at this level."""

        alerts = [
            alert
            for alert in (self.coordinator.data or [])
            if alert.level == self._level
        ]

        return {
            "area": self.coordinator.area_name,
            "nivel": self._level,
            "total_avisos": len(alerts),
            "avisos": [
                alert.as_dict()
                for alert in alerts
            ],
        }


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Set up AEMET Alertas binary sensors."""

    coordinator = entry.runtime_data

    async_add_entities(
        [
            AemetAlertLevelSensor(
                coordinator,
                level,
            )
            for level in (
                "red",
                "orange",
                "yellow",
                "green",
            )
        ]
    )