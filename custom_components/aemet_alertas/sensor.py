"""Sensors for AEMET Alertas."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .entity import AemetAlertEntity, area_slug


LEVELS = {
    "red": {
        "name": "rojas",
        "count_icon": "mdi:alert-octagon",
        "phenomena_icon": "mdi:weather-lightning-rainy",
    },
    "orange": {
        "name": "naranjas",
        "count_icon": "mdi:alert",
        "phenomena_icon": "mdi:weather-pouring",
    },
    "yellow": {
        "name": "amarillas",
        "count_icon": "mdi:alert-outline",
        "phenomena_icon": "mdi:weather-cloudy-alert",
    },
    "green": {
        "name": "verdes",
        "count_icon": "mdi:check-circle-outline",
        "phenomena_icon": "mdi:weather-partly-cloudy",
    },
}


def _phenomenon_name(alert) -> str:
    """Return a clean phenomenon name from an AEMET alert."""

    event = (alert.event or "").strip()

    known = {
        "lluvias": "Lluvias",
        "tormentas": "Tormentas",
        "costeros": "Costeros",
        "nevadas": "Nevadas",
        "vientos": "Vientos",
        "temperaturas máximas": "Temperaturas máximas",
        "temperaturas mínimas": "Temperaturas mínimas",
        "polvo en suspensión": "Polvo en suspensión",
        "nieblas": "Nieblas",
        "deshielos": "Deshielos",
        "aludes": "Aludes",
        "galernas": "Galernas",
        "rissagues": "Rissagues",
    }

    prefix = "Aviso de "
    suffix = " de nivel"

    if event.lower().startswith(prefix.lower()) and suffix.lower() in event.lower():
        phenomenon = event[len(prefix):].split(
            suffix,
            1,
        )[0].strip()

        return known.get(
            phenomenon.casefold(),
            phenomenon.capitalize(),
        )

    # Fallback: obtener el fenómeno desde el parámetro CAP.
    parameter = (alert.parameter or "").strip()

    if parameter:
        code = parameter.split(";", 1)[0].strip()

        parameter_names = {
            "TO": "Tormentas",
            "CO": "Costeros",
            "NE": "Nevadas",
            "VI": "Vientos",
            "AT": "Temperaturas máximas",
            "BT": "Temperaturas mínimas",
            "VS": "Polvo en suspensión",
            "NI": "Nieblas",
            "DH": "Deshielos",
            "AL": "Aludes",
            "GA": "Galernas",
            "RI": "Rissagues",
            "PR": "Lluvias",
        }

        if code in parameter_names:
            return parameter_names[code]

    return event or "-"


class AemetActiveAlertsSensor(
    AemetAlertEntity,
    SensorEntity,
):
    """Sensor with the total number of active alerts."""

    _attr_icon = "mdi:weather-lightning-rainy"

    def __init__(self, coordinator) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        slug = area_slug(coordinator.area_name)

        self._attr_name = "Total avisos activos"
        self._attr_unique_id = (
            f"aemet_alertas_{slug}_active"
        )

    @property
    def native_value(self) -> int:
        """Return the number of active alerts."""

        return len(self.coordinator.data or [])

    @property
    def extra_state_attributes(self):
        """Return detailed information about active alerts."""

        alerts = self.coordinator.data or []

        return {
            "area": self.coordinator.area_name,
            "total_avisos": len(alerts),
            "niveles": list(
                dict.fromkeys(
                    alert.level
                    for alert in alerts
                )
            ),
            "fenomenos": list(
                dict.fromkeys(
                    _phenomenon_name(alert)
                    for alert in alerts
                )
            ),
            "zonas": list(
                dict.fromkeys(
                    alert.area_desc
                    for alert in alerts
                )
            ),
            "avisos": [
                alert.as_dict()
                for alert in alerts
            ],
        }


class AemetAlertCountSensor(
    AemetAlertEntity,
    SensorEntity,
):
    """Sensor with the number of alerts at one level."""

    def __init__(
        self,
        coordinator,
        level: str,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self._level = level

        slug = area_slug(coordinator.area_name)
        level_info = LEVELS[level]

        self._attr_name = f"Nº alertas {level_info['name']}"
        self._attr_unique_id = (
            f"aemet_alertas_{slug}_{level}_count"
        )
        self._attr_icon = level_info["count_icon"]

    @property
    def native_value(self) -> int:
        """Return the number of alerts at this level."""

        return sum(
            alert.level == self._level
            for alert in (self.coordinator.data or [])
        )


class AemetAlertPhenomenaSensor(
    AemetAlertEntity,
    SensorEntity,
):
    """Sensor with the phenomena active at one level."""

    def __init__(
        self,
        coordinator,
        level: str,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self._level = level

        slug = area_slug(coordinator.area_name)
        level_info = LEVELS[level]

        self._attr_name = f"Fenómenos {level_info['name']}"
        self._attr_unique_id = (
            f"aemet_alertas_{slug}_{level}_phenomena"
        )
        self._attr_icon = level_info["phenomena_icon"]

    @property
    def native_value(self) -> str:
        """Return the active phenomena at this level."""

        alerts = [
            alert
            for alert in (self.coordinator.data or [])
            if alert.level == self._level
        ]

        phenomena = []

        for alert in alerts:
            phenomenon = _phenomenon_name(alert)

            if (
                phenomenon != "-"
                and phenomenon not in phenomena
            ):
                phenomena.append(phenomenon)

        if not phenomena:
            return "-"

        return ", ".join(phenomena)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Set up AEMET Alertas sensors."""

    coordinator = entry.runtime_data

    entities = [
        AemetActiveAlertsSensor(coordinator),
    ]

    for level in (
        "red",
        "orange",
        "yellow",
        "green",
    ):
        entities.append(
            AemetAlertCountSensor(
                coordinator,
                level,
            )
        )

        entities.append(
            AemetAlertPhenomenaSensor(
                coordinator,
                level,
            )
        )

    async_add_entities(entities)