<div align="center">
![AEMET Alertas](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/custom_components/aemet_alertas/brand/icon.png)

  # AEMET Alertas

  **Avisos meteorológicos de AEMET, directamente en Home Assistant.**

  Integración personalizada para consultar avisos meteorológicos oficiales de AEMET,
  configurarlos desde la interfaz de Home Assistant y utilizarlos en sensores, dashboards y automatizaciones.

  <br>

  [![Validate with HACS](https://github.com/jacumal/aemet-alertas/actions/workflows/hacs.yaml/badge.svg)](https://github.com/jacumal/aemet-alertas/actions/workflows/hacs.yaml)
  [![Validate with hassfest](https://github.com/jacumal/aemet-alertas/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/jacumal/aemet-alertas/actions/workflows/hassfest.yaml)
  [![Latest release](https://img.shields.io/github/v/release/jacumal/aemet-alertas?style=flat-square&label=release)](https://github.com/jacumal/aemet-alertas/releases)
  [![License](https://img.shields.io/github/license/jacumal/aemet-alertas?style=flat-square)](LICENSE)
  [![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?style=flat-square&logo=home-assistant&logoColor=white)](https://www.home-assistant.io/)

</div>

---

## ✨ ¿Qué es AEMET Alertas?

**AEMET Alertas** lleva los avisos meteorológicos publicados por la **Agencia Estatal de Meteorología (AEMET)** directamente a Home Assistant utilizando sus canales oficiales de datos.

La integración descubre las provincias y zonas oficiales disponibles, permite seleccionar qué niveles y fenómenos monitorizar y expone la información mediante dispositivos, sensores, sensores binarios y una entidad `Event` preparada para automatizaciones.

> **Importante:** AEMET Alertas es un proyecto independiente y **no está afiliado, patrocinado, respaldado ni mantenido por AEMET**.

## ☕️ ¿Te resulta útil AEMET Alertas?

Si el proyecto te ayuda a estar al día de los avisos meteorológicos en Home Assistant, puedes **apoyar su desarrollo** con un café. Es totalmente opcional y ayuda a mantener el proyecto, preparar nuevas funciones y mejorar la documentación.

  <a href="https://www.buymeacoffee.com/jacumal">
    <img src="https://img.shields.io/badge/☕️%20Buy%20Me%20a%20Coffee-Apoyar%20el%20proyecto-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=000000" alt="Buy Me a Coffee">
  </a>

## 🚀 Características principales

| | Funcionalidad |
|---|---|
| 🌦️ | Datos de avisos directamente desde AEMET |
| 🗺️ | Provincias y zonas oficiales obtenidas dinámicamente de AEMET |
| ⚙️ | Configuración completa mediante Config Flow |
| 🎚️ | Filtros por nivel: verde, amarillo, naranja y rojo |
| 🌧️ | Filtros por fenómeno meteorológico |
| 📊 | Contadores de avisos activos por nivel |
| 🔔 | Sensores binarios para cada nivel de alerta |
| ☁️ | Fenómenos activos agrupados por nivel |
| ⚡ | Entidad `Event` para avisos nuevos, actualizados y finalizados |
| 🏠 | Dispositivo y entidades integrados con Home Assistant |
| 🎨 | Identidad visual propia e independiente de AEMET |
| 🌦️ | Tarjeta Lovelace incluida para visualizar los avisos |

### Niveles soportados

- 🟢 **Verde**
- 🟡 **Amarillo**
- 🟠 **Naranja**
- 🔴 **Rojo**

### Eventos soportados

La entidad de eventos puede generar:

- `new_alert` — nuevo aviso detectado
- `updated_alert` — aviso existente actualizado
- `ended_alert` — aviso finalizado

---

## 🖼️ Así se ve en Home Assistant

La integración utiliza los mecanismos nativos de Home Assistant, incluyendo **Config Flow**, **Device Registry**, **Entity Registry** y una entidad de eventos.

![AEMET Alertas en Home Assistant](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/01-integracion.png)


*Integración instalada y disponible desde Dispositivos y servicios.*

### Dispositivo y entidades

![Dispositivo AEMET Alertas y sus entidades](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/05-dispositivo.png)


*Cada zona configurada se representa como un dispositivo de Home Assistant.*

---

## 🌦️ Tarjeta Lovelace incluida

Desde **AEMET Alertas 1.0.3**, la tarjeta Lovelace está integrada directamente en la propia integración. Ya no es necesario instalar un repositorio separado para la tarjeta ni añadir manualmente un recurso JavaScript desde **Ajustes → Paneles de control → Recursos**.

La tarjeta utiliza los datos de las entidades creadas por AEMET Alertas y se registra automáticamente al instalar la integración.

### 📸 Vista previa

Ejemplos reales de la tarjeta mostrando diferentes niveles y tipos de avisos meteorológicos:

![AEMET Alertas Card - Aviso naranja en Tenerife](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/Ejemplo_alerta_naranja.png)

*🟠 Aviso naranja · Área metropolitana de Tenerife*

![AEMET Alertas Card - Aviso amarillo en Ampurdán](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/Ejemplo_alerta_amarilla.png)

*🟡 Aviso amarillo · Costa - Ampurdán*

> **Importante:** este proyecto es independiente y **no está afiliado, patrocinado, respaldado ni mantenido por AEMET**.

### 🎨 Características de la tarjeta

- 🟡🟠🔴 **Colores dinámicos** según el nivel del aviso.
- 📋 **Modo compacto** para el dashboard principal.
- 🔎 **Modo detallado** con toda la información relevante del aviso.
- 🔄 **Modo automático**: detallado cuando existen avisos y compacto cuando no los hay.
- 🌧️ Soporte para **múltiples avisos activos**.
- 📱 **Responsive por ancho real de tarjeta**, no por tamaño de pantalla.
- 🖥️ Aprovecha mejor el espacio en tablets, escritorio y dashboards panorámicos.
- 🧱 Compatible con el sistema moderno `getGridOptions()` de Home Assistant Sections.
- ↔️ El usuario puede **redimensionar la tarjeta** desde el editor de Home Assistant.
- 🧩 **Editor visual nativo** para seleccionar entidad y configurar las opciones principales sin crear una tarjeta manual.
- 🌙 Compatible con los temas claro y oscuro de Home Assistant.
- 🧩 Sin dependencias externas ni Browser Mod.
- 🧭 Enlace directo al aviso publicado por AEMET cuando está disponible.
- 🧱 Selector de tarjeta de Home Assistant mediante `window.customCards`.

### 🧩 Requisitos

Necesitas:

- Home Assistant.
- HACS para instalar la integración.
- AEMET Alertas instalada y configurada.

La tarjeta **no consulta AEMET directamente**: utiliza los atributos de la entidad proporcionada por la integración.

### ⚙️ Configuración mediante el editor visual

La tarjeta incluye un **editor visual nativo de Home Assistant**. Al añadir una tarjeta de tipo AEMET Alertas puedes configurar desde la interfaz:

- 📍 **Entidad** AEMET.
- 🎛️ **Modo**: Automático, Compacto o Detallado.
- 👁️ **Mostrar cuando no hay avisos**.
- 🔢 **Número máximo de avisos**.

No es necesario crear manualmente un recurso JavaScript.

### 📋 Modo compacto

Ideal para la pantalla principal del dashboard:

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: compact
```

Muestra el nivel, la zona, el número de avisos y un resumen de los fenómenos activos.

### 🔎 Modo detallado

Para una vista meteorológica específica:

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
```

Incluye, cuando están disponibles:

- Fenómeno.
- Zona.
- Parámetro.
- Probabilidad.
- Severidad.
- Urgencia.
- Certeza.
- Inicio y finalización.
- Descripción.
- Recomendaciones.
- Enlace al aviso de AEMET.

### 🔄 Modo automático

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: auto
```

Con `auto`, la tarjeta utiliza el modo detallado cuando existen avisos activos y muestra un estado limpio cuando no hay avisos.

### 👁️ Ocultar la tarjeta cuando no hay avisos

Por defecto, la tarjeta se muestra aunque no existan avisos. Puedes ocultarla completamente con:

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: compact
show_when_clear: false
```

### 🔢 Limitar el número de avisos

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
max_alerts: 3
```

El valor predeterminado es `5`.

---

## 📐 Ancho y layout responsive

La tarjeta utiliza el **ancho real que Home Assistant asigna a la tarjeta**. Esto evita un problema habitual en dashboards: una pantalla de escritorio puede ser enorme, pero una tarjeta concreta puede ocupar solo media sección.

El diseño cambia automáticamente según el ancho de la propia tarjeta:

| Ancho aproximado de la tarjeta | Layout |
|---|---|
| `< 560 px` | 📱 Vertical, optimizado para móvil |
| `560–759 px` | 📲 Horizontal compacto, pensado para tablet |
| `760–1099 px` | 🖥️ Horizontal amplio, con métricas en 3 columnas |
| `1100–1399 px` | 🖥️✨ Escritorio ancho |
| `≥ 1400 px` | 🖥️✨ Pantallas grandes / wall dashboards |

Esto significa que **no importa si el dispositivo es un móvil, iPad, portátil o PC**: la tarjeta responde al espacio que realmente tiene.

### 🧱 Home Assistant Sections y `grid_options`

En los dashboards modernos de tipo **Sections**, Home Assistant utiliza una cuadrícula de 12 columnas. La tarjeta declara un tamaño inicial de ancho completo y permite reducirla hasta 6 columnas.

Puedes modificar el ancho desde el editor visual de Home Assistant o mediante `grid_options`:

```yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
grid_options:
  columns: 12
  rows: 8
```

Para una tarjeta a media anchura:

```yaml
grid_options:
  columns: 6
  rows: 8
```

> 💡 **Recomendación:** en escritorio y wall dashboards, utiliza una tarjeta de `9` o `12` columnas para aprovechar el layout horizontal. En móvil normalmente Home Assistant la mostrará a ancho completo automáticamente.

### 🟢🟡🟠🔴 Niveles de aviso

La tarjeta interpreta los niveles proporcionados por AEMET Alertas:

| Nivel | Presentación |
|---|---|
| 🟢 Verde | Sin riesgo meteorológico relevante |
| 🟡 Amarillo | Aviso amarillo |
| 🟠 Naranja | Aviso naranja |
| 🔴 Rojo | Aviso rojo |

> **Nota:** los colores y la información mostrada dependen de los avisos y atributos proporcionados por la integración.

---

## ⚙️ Configuración paso a paso

### 1. Selección de provincia

![Selección de provincia en AEMET Alertas](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/02-provincia.png)

La provincia se selecciona desde el asistente de configuración. Las zonas disponibles se obtienen directamente de AEMET.

### 2. Selección de zona oficial

![Selección de zona oficial de AEMET](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/03-zona.png)

La integración utiliza las **zonas oficiales de avisos de AEMET**, evitando depender de nombres o divisiones geográficas mantenidas manualmente.

### 3. Dispositivo y asignación a un área

![Asignación del dispositivo AEMET Alertas a un área](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/04-asignacion.png)

Cada zona configurada se representa como un dispositivo y puede asignarse a un área de la vivienda, igual que cualquier otra integración de Home Assistant.

---

## 📊 Entidades disponibles

Por cada zona configurada, AEMET Alertas crea un dispositivo con sus entidades asociadas.

### Sensores

- **Total avisos activos**
- **Nº alertas verdes**
- **Nº alertas amarillas**
- **Nº alertas naranjas**
- **Nº alertas rojas**
- **Fenómenos verdes**
- **Fenómenos amarillos**
- **Fenómenos naranjas**
- **Fenómenos rojos**

### Sensores binarios

Un sensor por nivel:

- **Alerta verde**
- **Alerta amarilla**
- **Alerta naranja**
- **Alerta roja**

Esto permite crear automatizaciones sencillas, por ejemplo reaccionar inmediatamente cuando aparece una alerta roja.

### Eventos

![Entidades y eventos de AEMET Alertas](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/06-entidades.png)

La entidad **Eventos de alertas** permite reaccionar a cambios en los avisos sin tener que consultar continuamente los sensores.

---

## 📦 Instalación

### HACS / Marketplace

AEMET Alertas está preparado para su distribución mediante HACS/Marketplace. Mientras no forme parte del catálogo predeterminado, puede instalarse como repositorio personalizado.

1. Abre **HACS / Marketplace → Integraciones**.
2. Añade `https://github.com/jacumal/aemet-alertas` como repositorio personalizado.
3. Selecciona **Integration**.
4. Instala **AEMET Alertas**.
5. Reinicia Home Assistant.

> 💡 **Consejo:** después de instalar o actualizar una integración personalizada, reinicia Home Assistant para cargar la nueva versión.

> 🌦️ **Tarjeta Lovelace:** no necesitas instalar ningún repositorio adicional. La tarjeta está incluida en AEMET Alertas y se registra automáticamente.

### Instalación manual

Copia el directorio:

```text
custom_components/aemet_alertas
```

en:

```text
/config/custom_components/aemet_alertas
```

Después reinicia Home Assistant.

---

## 🧭 Configuración

Después de reiniciar Home Assistant:

**Configuración → Dispositivos y servicios → Añadir integración → AEMET Alertas**

El asistente guía el proceso:

```text
Provincia
   ↓
Zona oficial de AEMET
   ↓
Niveles a monitorizar
   ↓
Fenómenos a monitorizar
```

La configuración puede modificarse posteriormente desde las opciones de la integración.

---

## 🤖 Automatizaciones

AEMET Alertas está pensado para integrarse directamente con las automatizaciones de Home Assistant.

### 🔴 Avisar al móvil cuando aparece una alerta roja

```yaml
alias: AEMET - Aviso de alerta roja
description: Envía una notificación cuando se activa una alerta roja.
triggers:
  - trigger: state
    entity_id: binary_sensor.aemet_alertas_litoral_norte_de_valencia_alerta_roja
    to: "on"
actions:
  - action: notify.mobile_app_iphone
    data:
      title: "🚨 Alerta roja AEMET"
      message: "Se ha activado una alerta roja en la zona configurada."
mode: single
```

### 🟠 Encender una luz cuando aparece una alerta naranja

```yaml
alias: AEMET - Alerta naranja
description: Enciende una luz cuando existe una alerta naranja.
triggers:
  - trigger: state
    entity_id: binary_sensor.aemet_alertas_litoral_norte_de_valencia_alerta_naranja
    to: "on"
actions:
  - action: light.turn_on
    target:
      entity_id: light.luz_entrada
mode: single
```

> Los nombres exactos de las entidades dependen de la zona configurada en Home Assistant.

---

## ⚡ Eventos para automatizaciones avanzadas

La entidad `Event` permite reaccionar cuando AEMET detecta cambios en los avisos.

```text
new_alert
updated_alert
ended_alert
```

Esto permite construir notificaciones inteligentes, registrar el histórico de avisos o activar escenas dependiendo del tipo de cambio detectado.

---

## 🛰️ Fuente de datos

Los datos se obtienen directamente de los canales oficiales de AEMET para las zonas de aviso y de los mensajes **CAP 1.2** publicados por AEMET.

La integración procesa, entre otros elementos:

- Catálogo oficial de zonas.
- Fichero de estado de avisos.
- Mensajes CAP 1.2.
- Nivel oficial `AEMET-Meteoalerta nivel`.
- Información oficial del fenómeno y parámetros CAP.

La integración **no depende de MeteoAlarm ni de Feedreader**.

Para las condiciones de reutilización de los datos, consulta el [aviso legal de AEMET](https://www.aemet.es/es/nota_legal).

---

## ☕️ Apoya el proyecto

Si **AEMET Alertas** te resulta útil y quieres apoyar su mantenimiento y desarrollo, puedes invitarme a un café a través de **Buy Me a Coffee**:

  <a href="https://www.buymeacoffee.com/jacumal">
    <img src="https://img.shields.io/badge/☕️%20Buy%20Me%20a%20Coffee-Apoyar%20el%20proyecto-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=000000" alt="Buy Me a Coffee">
  </a>

El apoyo es totalmente opcional y ayuda a dedicar tiempo a nuevas funciones, mantenimiento, documentación y soporte de la integración.

---

## 🛠️ Desarrollo y calidad

El repositorio incorpora validación automática mediante **HACS** y **Home Assistant Hassfest** en cada cambio.

Ambas validaciones están pasando actualmente en el commit principal. Antes de publicar una versión se comprueba que la integración mantiene una estructura compatible con los validadores de Home Assistant y HACS.

---

## 📌 Estado del proyecto

**Versión actual: 1.0.3**

La versión 1.0.3 incluye la tarjeta Lovelace integrada en la propia integración, además de las correcciones necesarias para el manejo de eventos y el procesamiento de datos fuera del event loop.

El proyecto está en evolución y se aceptan sugerencias, mejoras y reportes de errores mediante GitHub Issues.

---

## ⚖️ Aviso legal y marca

AEMET Alertas utiliza información meteorológica publicada por la **Agencia Estatal de Meteorología (AEMET)**.

**Este proyecto no es oficial de AEMET y no está afiliado, patrocinado, respaldado ni mantenido por AEMET.**

El nombre AEMET se utiliza únicamente para identificar la fuente de los datos meteorológicos utilizados por esta integración. La identidad visual del proyecto es independiente y no pretende reproducir la imagen corporativa oficial de AEMET.

Consulta las condiciones de reutilización de AEMET antes de redistribuir o utilizar los datos obtenidos mediante esta integración:

https://www.aemet.es/es/nota_legal

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia **MIT**. Consulta [`LICENSE`](LICENSE) para más información.

## 👨‍💻 Créditos

Desarrollado por **Javi / [@jacumal](https://github.com/jacumal)** para la comunidad de Home Assistant.

AEMET y sus contenidos meteorológicos son propiedad de la **Agencia Estatal de Meteorología**. Este proyecto utiliza dichos datos como fuente y no reclama ninguna titularidad sobre ellos.

---

<div align="center">

**AEMET Alertas · Home Assistant · Avisos meteorológicos**

</div>
