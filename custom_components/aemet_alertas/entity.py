"""Base entities for AEMET Alertas."""
from __future__ import annotations

import re

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def area_slug(area: str) -> str:
    """Create a stable slug from the area name."""

    slug = (
        area.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
        .replace("ñ", "n")
    )

    return re.sub(
        r"[^a-z0-9]+",
        "_",
        slug,
    ).strip("_")


class AemetAlertEntity(CoordinatorEntity):
    """Base entity for AEMET Alertas."""

    _attr_has_entity_name = False

    def __init__(self, coordinator) -> None:
        """Initialize the AEMET entity."""

        super().__init__(coordinator)

        area = coordinator.area_name
        slug = area_slug(area)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, slug)},
            name=f"AEMET Alertas — {area}",
            manufacturer="AEMET",
            model="Avisos meteorológicos",
        )