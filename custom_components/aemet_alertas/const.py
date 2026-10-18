"""Constants for AEMET Alertas."""
from __future__ import annotations

DOMAIN = "aemet_alertas"
NAME = "AEMET Alertas"
DEFAULT_SCAN_INTERVAL = 300
CONF_PROVINCE = "province"
CONF_AREA = "area"
CONF_AREA_NAME = "area_name"
CONF_SEVERITIES = "severities"
CONF_EVENTS = "events"

SEVERITY_GREEN = "green"
SEVERITY_YELLOW = "yellow"
SEVERITY_ORANGE = "orange"
SEVERITY_RED = "red"
SEVERITIES = (
    SEVERITY_GREEN,
    SEVERITY_YELLOW,
    SEVERITY_ORANGE,
    SEVERITY_RED,
)
ALL_EVENTS = "all"

# AEMET Meteoalerta CAP eventCode identifiers.
EVENT_CODES = {
    "PR": "Lluvias",
    "NE": "Nevadas",
    "VI": "Vientos",
    "TO": "Tormentas",
    "AT": "Temperaturas máximas",
    "BT": "Temperaturas mínimas",
    "CO": "Costeros",
    "VS": "Polvo en suspensión",
    "AL": "Aludes",
    "GA": "Galernas",
    "RI": "Rissagues",
    "NI": "Nieblas",
    "DH": "Deshielos",
}
EVENT_NAMES = ("all", *EVENT_CODES.values())

SEVERITY_TO_CAP = {
    "yellow": "Moderate",
    "orange": "Severe",
    "red": "Extreme",
}
CAP_TO_SEVERITY = {v.casefold(): k for k, v in SEVERITY_TO_CAP.items()}