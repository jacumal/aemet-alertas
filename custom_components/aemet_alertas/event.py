"""Events for AEMET Alertas."""
from __future__ import annotations

from homeassistant.components.event import EventEntity

from .entity import AemetAlertEntity, area_slug


class AemetAlertEvent(
    AemetAlertEntity,
    EventEntity,
):
    """Event entity for AEMET alert changes."""

    _attr_event_types = [
        "new_alert",
        "updated_alert",
        "ended_alert",
    ]

    _attr_icon = "mdi:bell-alert"

    def __init__(self, coordinator) -> None:
        """Initialize the event entity."""

        super().__init__(coordinator)

        slug = area_slug(coordinator.area_name)

        self._attr_name = "Eventos de alertas"
        self._attr_unique_id = (
            f"aemet_alertas_{slug}_event"
        )

        self._seen: dict[str, object] = {}

    def _handle_coordinator_update(self) -> None:
        """Detect changes in the active alerts."""

        current = {
            alert.key: alert
            for alert in (self.coordinator.data or [])
        }

        if self._seen:
            # Nuevos o modificados
            for key, alert in current.items():
                if key not in self._seen:
                    self._trigger_event(
                        "new_alert",
                        alert.as_dict(),
                    )

                elif (
                    alert.as_dict()
                    != self._seen[key].as_dict()
                ):
                    self._trigger_event(
                        "updated_alert",
                        alert.as_dict(),
                    )

            # Finalizados
            for key in self._seen.keys() - current.keys():
                old_alert = self._seen[key]

                self._trigger_event(
                    "ended_alert",
                    old_alert.as_dict(),
                )

        self._seen = current

        super()._handle_coordinator_update()


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Set up AEMET Alertas event entity."""

    async_add_entities(
        [
            AemetAlertEvent(
                entry.runtime_data,
            )
        ]
    )