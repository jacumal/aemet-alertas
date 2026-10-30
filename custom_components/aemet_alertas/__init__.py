"""AEMET Alertas integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .coordinator import AemetAlertasCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.EVENT,
]


async def async_update_options(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload the integration after option changes."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up AEMET Alertas from a config entry."""

    coordinator = AemetAlertasCoordinator(
        hass,
        async_get_clientsession(hass),
        entry.data,
        entry.options,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(
        entry.add_update_listener(async_update_options)
    )

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload AEMET Alertas."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )