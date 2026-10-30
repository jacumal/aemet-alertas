# Changelog

All notable changes to **AEMET Alertas** are documented here.

The project follows a simple release-oriented changelog. Version numbers refer to the integration version exposed by Home Assistant.

## [1.0.0] - 2026-10-30

### Added

- Direct retrieval of AEMET weather alerts through official public data channels.
- Dynamic discovery of provinces and official alert zones.
- Home Assistant Config Flow for setup and configuration.
- Configurable filters for alert levels and meteorological phenomena.
- Support for green, yellow, orange and red alert levels.
- Sensors with active alert counts by level.
- Binary sensors for each alert level.
- Active phenomena grouped by alert level.
- Event entity supporting `new_alert`, `updated_alert` and `ended_alert`.
- Home Assistant Device Registry and Entity Registry integration.
- HACS validation workflow.
- Home Assistant Hassfest validation workflow.
- Custom project branding and documentation.

### Documentation

- Initial public README.
- Home Assistant screenshots covering installation, configuration and entities.
- Automation examples for red and orange alerts.
- Legal and AEMET data-source information.

[1.0.0]: https://github.com/jacumal/aemet-alertas/releases/tag/v1.0.0
