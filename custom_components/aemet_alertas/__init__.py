"""AEMET Alertas integration."""
from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace import LOVELACE_DATA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .coordinator import AemetAlertasCoordinator

CARD_DIR = Path(__file__).parent / "www"
CARD_URL = "/aemet_alertas/aemet-alertas-card-responsive.js"

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.EVENT]


async def _async_register_card(hass: HomeAssistant) -> None:
    """Serve and register the bundled Lovelace card."""
    card_path = CARD_DIR / "aemet-alertas-card.js"
    if not card_path.is_file():
        return

    try:
        await hass.http.async_register_static_paths(
            [StaticPathConfig("/aemet_alertas", str(CARD_DIR), False)]
        )
    except RuntimeError:
        pass

    lovelace = hass.data.get(LOVELACE_DATA)
    if lovelace is None:
        return
    resources = getattr(lovelace, "resources", None)
    if resources is None or not hasattr(resources, "async_create_item"):
        return

    await resources.async_get_info()
    if any(item.get("url") == CARD_URL for item in resources.async_items()):
        return
    await resources.async_create_item({"res_type": "module", "url": CARD_URL})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up AEMET Alertas."""
    await _async_register_card(hass)
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration after option changes."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AEMET Alertas from a config entry."""
    coordinator = AemetAlertasCoordinator(
        hass,
        async_get_clientsession(hass),
        entry.data,
        entry.options,
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload AEMET Alertas."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
