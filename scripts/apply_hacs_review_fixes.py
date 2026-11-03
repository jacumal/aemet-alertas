from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "aemet_alertas"
CARD_DIR = INTEGRATION / "www"
VERSION = "1.0.3"
CARD_BASE = "https://raw.githubusercontent.com/jacumal/aemet-alertas-card/main"


def write_event() -> None:
    (INTEGRATION / "event.py").write_text(
        '''"""Events for AEMET Alertas."""
from __future__ import annotations

from homeassistant.components.event import EventEntity

from .entity import AemetAlertEntity, area_slug


class AemetAlertEvent(AemetAlertEntity, EventEntity):
    """Event entity for AEMET alert changes."""

    _attr_event_types = ["new_alert", "updated_alert", "ended_alert"]
    _attr_icon = "mdi:bell-alert"

    def __init__(self, coordinator) -> None:
        """Initialize the event entity."""
        super().__init__(coordinator)
        slug = area_slug(coordinator.area_name)
        self._attr_name = "Eventos de alertas"
        self._attr_unique_id = f"aemet_alertas_{slug}_event"
        self._seen: dict[str, object] = {}

    async def async_added_to_hass(self) -> None:
        """Initialize the previous alert state."""
        await super().async_added_to_hass()
        self._seen = {
            alert.key: alert for alert in (self.coordinator.data or [])
        }

    def _handle_coordinator_update(self) -> None:
        """Detect changes in the active alerts."""
        current = {
            alert.key: alert for alert in (self.coordinator.data or [])
        }

        for key, alert in current.items():
            if key not in self._seen:
                self._trigger_event("new_alert", alert.as_dict())
            elif alert.as_dict() != self._seen[key].as_dict():
                self._trigger_event("updated_alert", alert.as_dict())

        for key in self._seen.keys() - current.keys():
            self._trigger_event("ended_alert", self._seen[key].as_dict())

        self._seen = current
        super()._handle_coordinator_update()


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up AEMET Alertas event entity."""
    async_add_entities([AemetAlertEvent(entry.runtime_data)])
''',
        encoding="utf-8",
    )


def patch_coordinator() -> None:
    path = INTEGRATION / "coordinator.py"
    text = path.read_text(encoding="utf-8")

    helper = '''def _read_archive(payload: bytes, archive_url: str) -> list[Alert]:
    """Read all CAP XML files from an AEMET tar.gz snapshot."""
    alerts: list[Alert] = []
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.lower().endswith(".xml"):
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            try:
                alerts.extend(parse_cap(extracted.read(), archive_url))
            except ET.ParseError:
                _LOGGER.warning(
                    "AEMET Alertas: invalid CAP XML inside archive: %s",
                    member.name,
                )
    return alerts


'''
    if "def _read_archive(payload: bytes" not in text:
        text = text.replace("class AemetAlertasCoordinator(\n", helper + "class AemetAlertasCoordinator(\n", 1)

    replacement = '''    async def _read_archive(
        self,
        archive_url: str,
    ) -> list[Alert]:
        """Download and parse an AEMET tar.gz snapshot off the event loop."""
        payload = await self._get(archive_url)
        return await self.hass.async_add_executor_job(
            _read_archive,
            payload,
            archive_url,
        )

    async def _read_atom(
'''
    text, count = re.subn(
        r"    async def _read_archive\(\n.*?\n    async def _read_atom\(",
        replacement,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Could not replace coordinator _read_archive")

    old = '''                alerts.extend(
                    parse_cap(
                        await self._get(url),
                        url,
                    )
                )
'''
    new = '''                payload = await self._get(url)
                alerts.extend(
                    await self.hass.async_add_executor_job(
                        parse_cap,
                        payload,
                        url,
                    )
                )
'''
    if old not in text:
        raise RuntimeError("Could not find fallback parse_cap block")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def write_init() -> None:
    (INTEGRATION / "__init__.py").write_text(
        '''"""AEMET Alertas integration."""
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
CARD_URL = "/aemet_alertas/aemet-alertas-card.js"

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
''',
        encoding="utf-8",
    )


def patch_metadata() -> None:
    path = INTEGRATION / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    dependencies = list(data.get("dependencies", []))
    for dependency in ("frontend", "http"):
        if dependency not in dependencies:
            dependencies.append(dependency)
    data["dependencies"] = dependencies
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    if f"## [{VERSION}]" not in text:
        text = text.replace(
            "## [1.0.0] - 2026-10-30",
            f"""## [{VERSION}] - 2026-11-03

### Fixed

- Fixed `new_alert` for the first alert after a clear state.
- Moved TAR/GZIP decompression and CAP parsing to the executor.
- Bundled the AEMET Alertas Lovelace card with automatic registration.

## [1.0.0] - 2026-10-30""",
            1,
        )
        changelog.write_text(text, encoding="utf-8")


def download_card() -> None:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    for name in (
        "aemet-alertas-card.js",
        "aemet-alertas-card-core.js",
        "aemet-alertas-card-editor.js",
        "aemet-alertas-card-responsive.js",
    ):
        urllib.request.urlretrieve(f"{CARD_BASE}/{name}", CARD_DIR / name)


if __name__ == "__main__":
    write_event()
    patch_coordinator()
    write_init()
    patch_metadata()
    download_card()
