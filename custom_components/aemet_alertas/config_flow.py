"""Config flow for AEMET Alertas."""
from __future__ import annotations

import logging
from html.parser import HTMLParser
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import aiohttp
import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_AREA,
    CONF_AREA_NAME,
    CONF_EVENTS,
    CONF_PROVINCE,
    CONF_SEVERITIES,
    DOMAIN,
    EVENT_NAMES,
)

_LOGGER = logging.getLogger(__name__)

AEMET_ROOT = "https://www.aemet.es"

COMMUNITIES = {
    "Andalucía": "and",
    "Aragón": "arn",
    "Asturias": "ast",
    "Illes Balears": "bal",
    "Canarias": "coo",
    "Cantabria": "cant",
    "Castilla-La Mancha": "clm",
    "Castilla y León": "cle",
    "Cataluña": "cat",
    "Ceuta": "ceu",
    "Comunitat Valenciana": "val",
    "Extremadura": "ext",
    "Galicia": "gal",
    "La Rioja": "rio",
    "Comunidad de Madrid": "mad",
    "Navarra": "nav",
    "País Vasco": "pva",
    "Región de Murcia": "mur",
    "Melilla": "mel",
}

PROVINCE_TO_COMMUNITY = {
    "Almería": "Andalucía",
    "Cádiz": "Andalucía",
    "Córdoba": "Andalucía",
    "Granada": "Andalucía",
    "Huelva": "Andalucía",
    "Jaén": "Andalucía",
    "Málaga": "Andalucía",
    "Sevilla": "Andalucía",
    "Huesca": "Aragón",
    "Teruel": "Aragón",
    "Zaragoza": "Aragón",
    "Asturias": "Asturias",
    "Illes Balears": "Illes Balears",
    "Las Palmas": "Canarias",
    "Santa Cruz de Tenerife": "Canarias",
    "Cantabria": "Cantabria",
    "Albacete": "Castilla-La Mancha",
    "Ciudad Real": "Castilla-La Mancha",
    "Cuenca": "Castilla-La Mancha",
    "Guadalajara": "Castilla-La Mancha",
    "Toledo": "Castilla-La Mancha",
    "Ávila": "Castilla y León",
    "Burgos": "Castilla y León",
    "León": "Castilla y León",
    "Palencia": "Castilla y León",
    "Salamanca": "Castilla y León",
    "Segovia": "Castilla y León",
    "Soria": "Castilla y León",
    "Valladolid": "Castilla y León",
    "Zamora": "Castilla y León",
    "Barcelona": "Cataluña",
    "Girona": "Cataluña",
    "Lleida": "Cataluña",
    "Tarragona": "Cataluña",
    "Ceuta": "Ceuta",
    "Melilla": "Melilla",
    "Alicante": "Comunitat Valenciana",
    "Castellón": "Comunitat Valenciana",
    "Valencia": "Comunitat Valenciana",
    "Badajoz": "Extremadura",
    "Cáceres": "Extremadura",
    "A Coruña": "Galicia",
    "Lugo": "Galicia",
    "Ourense": "Galicia",
    "Pontevedra": "Galicia",
    "La Rioja": "La Rioja",
    "Madrid": "Comunidad de Madrid",
    "Navarra": "Navarra",
    "Álava": "País Vasco",
    "Bizkaia": "País Vasco",
    "Gipuzkoa": "País Vasco",
    "Murcia": "Región de Murcia",
}

# AEMET's Canary Islands catalogue is organised by island/zone links,
# without the 4-digit province link used by the mainland provinces.
CANARY_PROVINCE_PREFIXES = {
    "Las Palmas": ("6590", "6591", "6592"),
    "Santa Cruz de Tenerife": ("6593", "6594", "6595", "6596"),
}

PROVINCES = sorted(PROVINCE_TO_COMMUNITY)


def _normalize_name(value: str) -> str:
    value = value.casefold().strip()
    value = value.replace("valència", "valencia")
    replacements = str.maketrans(
        {
            "à": "a",
            "á": "a",
            "è": "e",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ï": "i",
            "ñ": "n",
        }
    )
    return value.translate(replacements)


def _same_name(left: str, right: str) -> bool:
    """Compare AEMET names, including bilingual names such as València/Valencia."""
    left_normalized = _normalize_name(left)
    right_normalized = _normalize_name(right)

    if left_normalized == right_normalized:
        return True

    for part in left_normalized.split("/"):
        if part.strip() == right_normalized:
            return True

    return False


class _LinkParser(HTMLParser):
    """Collect links and their visible text."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            text = " ".join(" ".join(self._text).split())
            self.links.append((text, urljoin(AEMET_ROOT, self._href)))
            self._href = None
            self._text = []


def _area_url(code: str) -> str:
    """Build the official AEMET Atom URL for a warning area."""
    return (
        f"{AEMET_ROOT}/documentos_d/eltiempo/prediccion/"
        f"avisos/rss/CAP_AFAZ{code}_ATOM.xml"
    )


async def _get_catalog(hass: Any, province: str) -> dict[str, str]:
    """Get official AEMET warning areas for a province."""
    community = PROVINCE_TO_COMMUNITY[province]
    url = f"{AEMET_ROOT}/es/rss_info/avisos/{COMMUNITIES[community]}"
    session = async_get_clientsession(hass)

    _LOGGER.debug(
        "AEMET Alertas: requesting catalogue for province=%s URL=%s",
        province,
        url,
    )

    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as response:
            status = response.status
            final_url = str(response.url)
            html = await response.text()

            _LOGGER.debug(
                "AEMET Alertas: catalogue response status=%s final_url=%s bytes=%s",
                status,
                final_url,
                len(html),
            )
            response.raise_for_status()

    except (ClientError, TimeoutError) as err:
        _LOGGER.exception(
            "AEMET Alertas: connection error while requesting %s: %s",
            url,
            err,
        )
        raise RuntimeError(f"connection error: {err}") from err

    parser = _LinkParser()
    parser.feed(html)

    # Mainland AEMET pages expose a 4-digit province link (p=XXXX).
    province_code: str | None = None
    for text, href in parser.links:
        query = parse_qs(urlparse(href).query)
        code = (query.get("p") or [""])[0]

        if code.isdigit() and len(code) == 4 and _same_name(text, province):
            province_code = code
            break

    areas: dict[str, str] = {}
    area_details: list[tuple[str, str, str]] = []

    if province_code is not None:
        # Mainland / non-Canary catalogue: warning area codes start with
        # the four-digit province code.
        for text, href in parser.links:
            query = parse_qs(urlparse(href).query)
            code = (query.get("l") or [""])[0]

            if (
                code.isdigit()
                and len(code) == 6
                and code.startswith(province_code)
                and text
            ):
                atom_url = _area_url(code)
                areas[text] = atom_url
                area_details.append((text, code, atom_url))
    elif community == "Canarias":
        # Canarias is different: the RSS page has no province link for
        # Santa Cruz de Tenerife / Las Palmas. It links directly to islands
        # and warning areas, whose first four digits identify the province.
        prefixes = CANARY_PROVINCE_PREFIXES[province]

        for text, href in parser.links:
            query = parse_qs(urlparse(href).query)
            code = (query.get("l") or [""])[0]

            if (
                code.isdigit()
                and len(code) == 6
                and code.startswith(prefixes)
                and text
            ):
                atom_url = _area_url(code)
                areas[text] = atom_url
                area_details.append((text, code, atom_url))

        _LOGGER.debug(
            "AEMET Alertas: Canary catalogue province=%s prefixes=%s areas=%s",
            province,
            prefixes,
            area_details,
        )
    else:
        candidates = []
        for text, href in parser.links:
            query = parse_qs(urlparse(href).query)
            code = (query.get("p") or query.get("l") or [""])[0]
            if code.isdigit() and len(code) == 4:
                candidates.append((text, code, href))

        _LOGGER.error(
            "AEMET Alertas: could not identify province %s. 4-digit links found: %s",
            province,
            candidates,
        )
        raise RuntimeError("province code not found")

    _LOGGER.debug(
        "AEMET Alertas: province=%s code=%s areas_found=%s details=%s",
        province,
        province_code,
        len(areas),
        area_details,
    )

    if not areas:
        raise RuntimeError(
            f"no warning areas found for province {province}"
            + (f" (code {province_code})" if province_code else "")
        )

    return dict(sorted(areas.items()))


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the AEMET Alertas config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._province: str | None = None
        self._areas: dict[str, str] = {}
        self._area_name: str | None = None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow."""
        return OptionsFlowHandler()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Select province."""
        if user_input:
            self._province = user_input[CONF_PROVINCE]

            try:
                self._areas = await _get_catalog(self.hass, self._province)
            except Exception as err:  # noqa: BLE001
                _LOGGER.exception(
                    "AEMET Alertas: unexpected error getting catalogue for province %s: %s",
                    self._province,
                    err,
                )
                return self.async_abort(reason="cannot_connect")

            return await self.async_step_area()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_PROVINCE): vol.In(PROVINCES)}
            ),
        )

    async def async_step_area(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Select warning area."""
        if user_input:
            self._area_name = user_input[CONF_AREA_NAME]
            area_url = self._areas[self._area_name]

            await self.async_set_unique_id(
                f"{self._province}_{self._area_name}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"AEMET Alertas – {self._area_name}",
                data={
                    CONF_PROVINCE: self._province,
                    CONF_AREA: area_url,
                    CONF_AREA_NAME: self._area_name,
                },
                options={
                    CONF_SEVERITIES: [
                        "green",
                        "yellow",
                        "orange",
                        "red",
                    ],
                    CONF_EVENTS: ["all"],
                },
            )

        return self.async_show_form(
            step_id="area",
            data_schema=vol.Schema(
                {vol.Required(CONF_AREA_NAME): vol.In(list(self._areas))}
            ),
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle AEMET Alertas option changes."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Start the options flow."""
        return await self.async_step_options(user_input)

    async def async_step_options(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Configure alert severity and phenomenon filters."""
        current_severities = list(
            self.config_entry.options.get(
                CONF_SEVERITIES,
                ["green", "yellow", "orange", "red"],
            )
        )
        current_events = list(
            self.config_entry.options.get(CONF_EVENTS, ["all"])
        )

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        severity_options = [
            {"value": "green", "label": "Verde"},
            {"value": "yellow", "label": "Amarillo"},
            {"value": "orange", "label": "Naranja"},
            {"value": "red", "label": "Rojo"},
        ]

        event_options = [
            {"value": "all", "label": "Todos"},
            *(
                {"value": event, "label": event}
                for event in EVENT_NAMES
                if event != "all"
            ),
        ]

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SEVERITIES,
                        default=current_severities,
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=severity_options,
                            multiple=True,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Required(
                        CONF_EVENTS,
                        default=current_events,
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=event_options,
                            multiple=True,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
        )
