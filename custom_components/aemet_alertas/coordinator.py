"""AEMET CAP/Atom client and parser."""
from __future__ import annotations

import io
import logging
import tarfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urljoin

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CAP_TO_SEVERITY,
    CONF_AREA,
    CONF_AREA_NAME,
    CONF_EVENTS,
    CONF_SEVERITIES,
    DOMAIN,
    EVENT_CODES,
)

_LOGGER = logging.getLogger(__name__)

ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
}

CAP = "{urn:oasis:names:tc:emergency:cap:1.2}"


@dataclass(frozen=True, slots=True)
class Alert:
    """Represent one AEMET CAP alert."""

    identifier: str
    references: str
    status: str
    msg_type: str
    sent: str
    effective: str
    onset: str
    expires: str
    severity: str
    level: str
    event: str
    event_code: str
    headline: str
    description: str
    instruction: str
    certainty: str
    urgency: str
    area_desc: str
    area_code: str
    parameter: str
    probability: str
    source_url: str

    @property
    def key(self) -> str:
        """Return a stable key for this alert."""
        return (
            f"{self.identifier}|"
            f"{self.area_code}|"
            f"{self.event_code}|"
            f"{self.onset}|"
            f"{self.expires}"
        )

    def as_dict(self) -> dict[str, Any]:
        """Return the alert as a dictionary."""
        return asdict(self)


def _text(
    parent: ET.Element,
    name: str,
    default: str = "",
) -> str:
    """Read a CAP child element as text."""
    node = parent.find(f"{CAP}{name}")

    if node is None or node.text is None:
        return default

    return node.text.strip()


def _parameters(info: ET.Element) -> dict[str, str]:
    """Read CAP parameter elements."""
    result: dict[str, str] = {}

    for parameter in info.findall(f"{CAP}parameter"):
        name = _text(parameter, "valueName")
        value = _text(parameter, "value")

        if name:
            result[name] = value

    return result


def _event_code(info: ET.Element) -> str:
    """Read the official AEMET phenomenon eventCode."""
    for code in info.findall(f"{CAP}eventCode"):
        value_name = _text(code, "valueName")

        if value_name == "AEMET-Meteoalerta fenómeno":
            value = _text(code, "value")

            if value:
                return value.split(";", 1)[0].strip().upper()

    return ""


def _area_code(area: ET.Element) -> str:
    """Read the official AEMET warning-area code."""
    for code in area.findall(f"{CAP}geocode"):
        value_name = _text(code, "valueName")

        if value_name == "AEMET-Meteoalerta zona":
            return _text(code, "value")

    return ""


def _normalize_level(value: str) -> str:
    """Normalize AEMET warning levels."""
    value = value.strip().casefold()

    return {
        "verde": "green",
        "amarillo": "yellow",
        "naranja": "orange",
        "rojo": "red",
    }.get(value, value)


def parse_cap(
    xml_bytes: bytes,
    source_url: str = "",
) -> list[Alert]:
    """Parse an AEMET CAP XML document."""
    root = ET.fromstring(xml_bytes)

    identifier = _text(root, "identifier")
    status = _text(root, "status")
    msg_type = _text(root, "msgType")
    references = _text(root, "references")
    sent = _text(root, "sent")

    alerts: list[Alert] = []

    for info in root.findall(f"{CAP}info"):
        language = _text(info, "language")

        # AEMET publishes the Spanish information as es-ES.
        if language and language.lower() not in {"es-es", "es"}:
            continue

        severity = _text(info, "severity")

        # CAP severity is a useful fallback:
        #
        # Moderate -> yellow
        # Severe   -> orange
        # Extreme  -> red
        level = CAP_TO_SEVERITY.get(
            severity.casefold(),
            "",
        )

        params = _parameters(info)

        # IMPORTANT:
        # AEMET explicitly publishes the official Meteoalerta
        # colour in this parameter. It is more reliable for our
        # purposes than translating the generic CAP severity.
        aemet_level = params.get(
            "AEMET-Meteoalerta nivel",
            "",
        )

        if aemet_level:
            level = _normalize_level(aemet_level)

        event_code = _event_code(info)

        event = EVENT_CODES.get(
            event_code,
            _text(info, "event"),
        )

        for area in info.findall(f"{CAP}area"):
            area_desc = _text(area, "areaDesc")

            alerts.append(
                Alert(
                    identifier=identifier,
                    references=references,
                    status=status,
                    msg_type=msg_type,
                    sent=sent,
                    effective=_text(info, "effective"),
                    onset=_text(info, "onset"),
                    expires=_text(info, "expires"),
                    severity=severity,
                    level=level,
                    event=event,
                    event_code=event_code,
                    headline=_text(info, "headline"),
                    description=_text(info, "description"),
                    instruction=_text(info, "instruction"),
                    certainty=_text(info, "certainty"),
                    urgency=_text(info, "urgency"),
                    area_desc=area_desc,
                    area_code=_area_code(area),
                    parameter=params.get(
                        "AEMET-Meteoalerta parametro",
                        "",
                    ),
                    probability=params.get(
                        "AEMET-Meteoalerta probabilidad",
                        "",
                    ),
                    source_url=source_url,
                )
            )

    return alerts


def _parse_datetime(value: str) -> datetime | None:
    """Parse an ISO-8601 CAP datetime."""
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _is_current_alert(alert: Alert) -> bool:
    """Return whether an alert is currently active."""
    # The AEMET tar.gz is already a snapshot of the current state,
    # but we still apply these checks to avoid exposing obsolete
    # or cancelled CAP messages.
    if alert.status.casefold() != "actual":
        return False

    if alert.msg_type.casefold() == "cancel":
        return False

    expires = _parse_datetime(alert.expires)

    if expires is None:
        # If AEMET does not provide a valid expiry date,
        # keep the alert rather than silently discarding it.
        return True

    now = datetime.now(expires.tzinfo)

    return expires > now


class AemetAlertasCoordinator(
    DataUpdateCoordinator[list[Alert]]
):
    """Keep the selected AEMET area synchronized."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        data: dict[str, Any],
        options: dict[str, Any],
    ) -> None:
        """Initialize the coordinator."""
        self.session = session

        self.area_url = data[CONF_AREA]
        self.area_name = data[CONF_AREA_NAME]

        self.severities = options.get(
            CONF_SEVERITIES,
            [
                "green",
                "yellow",
                "orange",
                "red",
            ],
        )

        self.events = options.get(
            CONF_EVENTS,
            ["all"],
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=300
            ),
        )

    async def _get(
        self,
        url: str,
    ) -> bytes:
        """Download data from AEMET."""
        async with self.session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            response.raise_for_status()
            return await response.read()

    async def _read_archive(
        self,
        archive_url: str,
    ) -> list[Alert]:
        """Read all CAP XML files from an AEMET tar.gz snapshot."""
        payload = await self._get(archive_url)

        alerts: list[Alert] = []

        with tarfile.open(
            fileobj=io.BytesIO(payload),
            mode="r:gz",
        ) as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue

                if not member.name.lower().endswith(".xml"):
                    continue

                extracted = archive.extractfile(member)

                if extracted is None:
                    continue

                try:
                    alerts.extend(
                        parse_cap(
                            extracted.read(),
                            archive_url,
                        )
                    )
                except ET.ParseError:
                    _LOGGER.warning(
                        "AEMET Alertas: invalid CAP XML "
                        "inside archive: %s",
                        member.name,
                    )

        return alerts

    async def _read_atom(
        self,
        atom: bytes,
    ) -> list[Alert]:
        """Read CAP information from the AEMET Atom feed."""
        root = ET.fromstring(atom)

        entries = root.findall(
            "atom:entry",
            ATOM_NS,
        )

        urls: list[str] = []

        for entry in entries:
            for link in entry.findall(
                "atom:link",
                ATOM_NS,
            ):
                href = link.attrib.get("href")

                if href:
                    urls.append(
                        urljoin(
                            self.area_url,
                            href,
                        )
                    )

        # AEMET publishes a complete active-state tar.gz.
        archive_url = next(
            (
                url
                for url in urls
                if url.lower().endswith(".tar.gz")
            ),
            None,
        )

        if archive_url:
            _LOGGER.debug(
                "AEMET Alertas: reading active-state archive %s",
                archive_url,
            )

            return await self._read_archive(
                archive_url
            )

        # Fallback for feeds that expose individual CAP XML files.
        alerts: list[Alert] = []

        for url in urls:
            if not url.lower().endswith(".xml"):
                continue

            try:
                alerts.extend(
                    parse_cap(
                        await self._get(url),
                        url,
                    )
                )
            except (
                aiohttp.ClientError,
                ET.ParseError,
            ):
                _LOGGER.debug(
                    "AEMET Alertas: could not read CAP %s",
                    url,
                    exc_info=True,
                )

        return alerts

    def _filter_alerts(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        """Filter, deduplicate and sort active alerts."""
        # First discard expired/cancelled messages.
        current = [
            alert
            for alert in alerts
            if _is_current_alert(alert)
        ]

        # Deduplicate by CAP identity.
        unique = {
            alert.key: alert
            for alert in current
        }

        filtered = list(unique.values())

        # Severity filter.
        allowed_levels = {
            str(level).casefold()
            for level in self.severities
        }

        if allowed_levels:
            filtered = [
                alert
                for alert in filtered
                if alert.level.casefold()
                in allowed_levels
            ]

        # Event filter.
        if "all" not in {
            str(event).casefold()
            for event in self.events
        }:
            wanted_events = {
                str(event).casefold()
                for event in self.events
            }

            filtered = [
                alert
                for alert in filtered
                if alert.event.casefold()
                in wanted_events
            ]

        return sorted(
            filtered,
            key=lambda alert: (
                alert.onset,
                alert.expires,
                alert.event,
                alert.area_desc,
            ),
        )

    async def _async_update_data(
        self,
    ) -> list[Alert]:
        """Fetch and process current AEMET alerts."""
        try:
            atom = await self._get(
                self.area_url
            )

            alerts = await self._read_atom(
                atom
            )

            filtered = self._filter_alerts(
                alerts
            )

            _LOGGER.debug(
                "AEMET Alertas: area=%s total=%s active=%s",
                self.area_name,
                len(alerts),
                len(filtered),
            )

            return filtered

        except (
            aiohttp.ClientError,
            ET.ParseError,
            tarfile.TarError,
            OSError,
        ) as err:
            raise UpdateFailed(
                "No se pudieron consultar "
                f"los avisos de AEMET: {err}"
            ) from err