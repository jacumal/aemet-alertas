<div align="center">
<img src="https://raw.githubusercontent.com/jacumal/aemet-alertas/main/custom_components/aemet_alertas/brand/icon.png" alt="AEMET Alertas" width="180">

# AEMET Alertas

**Avisos meteorológicos oficiales de AEMET, directamente en Home Assistant.**

Una única instalación para consultar, gestionar y visualizar avisos meteorológicos en tus dashboards y automatizaciones.

[![Validate with HACS](https://github.com/jacumal/aemet-alertas/actions/workflows/hacs.yaml/badge.svg)](https://github.com/jacumal/aemet-alertas/actions/workflows/hacs.yaml)
[![Validate with hassfest](https://github.com/jacumal/aemet-alertas/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/jacumal/aemet-alertas/actions/workflows/hassfest.yaml)
[![Latest release](https://img.shields.io/github/v/release/jacumal/aemet-alertas?style=flat-square&label=release)](https://github.com/jacumal/aemet-alertas/releases)
[![License](https://img.shields.io/github/license/jacumal/aemet-alertas?style=flat-square)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?style=flat-square&logo=home-assistant&logoColor=white)](https://www.home-assistant.io/)
</div>

---

## 🚀 Una instalación. Dos componentes. Una experiencia completa.

**AEMET Alertas incluye todo lo necesario para consultar, gestionar y visualizar los avisos meteorológicos oficiales de AEMET en Home Assistant.**

Al instalar AEMET Alertas obtienes automáticamente:

| Componente | ¿Qué incluye? |
|---|---|
| 🌦️ **Integración AEMET Alertas** | Consulta de avisos oficiales, configuración de provincias y zonas, sensores, sensores binarios y eventos para automatizaciones. |
| 🎨 **Tarjeta Lovelace AEMET Alertas** | Tarjeta visual para tus dashboards, con editor gráfico, distintos modos de visualización y diseño responsive. |

**No necesitas instalar dos repositorios. No necesitas descargar otra tarjeta desde HACS. No necesitas añadir manualmente un recurso JavaScript en la configuración estándar de Lovelace.**

Los dos componentes forman parte del mismo proyecto y se distribuyen conjuntamente.

> 💡 **Importante:** si has instalado AEMET Alertas, también tienes la tarjeta. Una vez cargado el recurso, podrás encontrarla en el selector de tarjetas de Home Assistant como **AEMET Alertas**.

## ✨ ¿Qué es AEMET Alertas?

AEMET Alertas es una integración personalizada para Home Assistant que obtiene los avisos meteorológicos publicados por la **Agencia Estatal de Meteorología (AEMET)** utilizando sus canales oficiales de datos.

Permite seleccionar las provincias, zonas, niveles y fenómenos que quieres monitorizar. La información se incorpora a Home Assistant mediante dispositivos, sensores, sensores binarios y una entidad Event, para utilizarla tanto en dashboards como en automatizaciones.

Además, incluye una tarjeta Lovelace propia para consultar los avisos de forma visual, sin dependencias externas.

> **Aviso:** AEMET Alertas es un proyecto independiente y no está afiliado, patrocinado, respaldado ni mantenido por AEMET.

## 🌟 Características principales

| | Funcionalidad |
|---|---|
| 🌦️ | Datos de avisos directamente desde los canales oficiales de AEMET |
| 🗺️ | Provincias y zonas oficiales obtenidas dinámicamente |
| ⚙️ | Configuración mediante el asistente gráfico de Home Assistant |
| 🎚️ | Selección de niveles: verde, amarillo, naranja y rojo |
| 🌧️ | Filtros por fenómenos meteorológicos |
| 📊 | Contadores de avisos activos por nivel |
| 🔔 | Sensores binarios para cada nivel de alerta |
| ☁️ | Fenómenos activos agrupados por nivel |
| ⚡ | Entidad Event para avisos nuevos, actualizados y finalizados |
| 🏠 | Dispositivos y entidades nativos de Home Assistant |
| 🎨 | Tarjeta Lovelace incluida y registrada automáticamente |
| 📱 | Tarjeta responsive para móvil, tablet y escritorio |
| 🧩 | Editor visual para configurar la tarjeta sin escribir YAML |

### Niveles soportados

- 🟢 Verde
- 🟡 Amarillo
- 🟠 Naranja
- 🔴 Rojo

### Eventos soportados

La entidad de eventos puede generar:

- new_alert — nuevo aviso detectado.
- updated_alert — aviso existente actualizado.
- ended_alert — aviso finalizado.

---

## 📦 Instalación

AEMET Alertas está disponible en **Home Assistant Marketplace** y también puede instalarse mediante **HACS** o manualmente.

### ⭐ Opción 1. Home Assistant Marketplace (recomendada)

1. Abre **Ajustes → Marketplace**.
2. Busca **AEMET Alertas**.
3. Selecciona la integración e inicia la instalación.
4. Home Assistant abrirá el asistente de configuración.
5. Selecciona la provincia, la zona oficial y los niveles y fenómenos que quieras monitorizar.
6. Finaliza la configuración.

**¡Y listo!** La integración y la tarjeta Lovelace quedan instaladas conjuntamente.

En una primera instalación desde Marketplace, si Home Assistant puede cargar la integración directamente, no es necesario reiniciar: se abrirá el asistente de configuración.

> 🔄 **Actualizaciones:** cuando Marketplace instale una nueva versión de AEMET Alertas, puede ser necesario reiniciar Home Assistant para cargar el nuevo código de la integración. Marketplace te avisará cuando sea necesario.

### Opción 2. HACS

1. Abre **HACS → Integraciones**.
2. Añade https://github.com/jacumal/aemet-alertas como repositorio personalizado si todavía no aparece en tu catálogo.
3. Selecciona la categoría **Integration**.
4. Busca e instala **AEMET Alertas**.
5. Reinicia Home Assistant para cargar la integración.
6. Accede a **Ajustes → Dispositivos y servicios → Añadir integración**.
7. Busca **AEMET Alertas** e inicia el asistente.

> 🎨 **La tarjeta Lovelace ya está incluida.** No tienes que instalar un segundo repositorio ni descargar una tarjeta independiente.

### Opción 3. Instalación manual

1. Descarga el repositorio.
2. Copia el directorio:

~~~text
custom_components/aemet_alertas
~~~

3. En tu instalación de Home Assistant, colócalo en:

~~~text
/config/custom_components/aemet_alertas
~~~

4. Reinicia Home Assistant.
5. Accede a **Ajustes → Dispositivos y servicios → Añadir integración**.
6. Busca **AEMET Alertas** y completa la configuración.

La tarjeta Lovelace también está incluida dentro de ese mismo directorio.

---

## 🎨 La tarjeta Lovelace está incluida

Desde AEMET Alertas 1.0.3, la tarjeta Lovelace forma parte de la propia integración. Ya no se distribuye como una instalación independiente.

La integración registra el recurso JavaScript de la tarjeta en Home Assistant y lo pone a disposición del selector de tarjetas.

**No tienes que añadir recursos manualmente en una instalación estándar de Lovelace.**

### ¿Dónde encuentro la tarjeta?

Una vez instalada y cargada la integración:

1. Abre tu dashboard.
2. Entra en el modo de edición.
3. Selecciona **Añadir tarjeta**.
4. Busca **AEMET Alertas**.
5. Selecciona la tarjeta y configura sus opciones desde el editor visual.

Si acabas de instalarla y todavía no aparece en el selector, recarga el navegador o la aplicación de Home Assistant para actualizar los recursos del frontend.

### 📸 Vista previa

Ejemplos de la tarjeta mostrando diferentes niveles y tipos de avisos meteorológicos:

![AEMET Alertas Card - Aviso naranja en Tenerife](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/Ejemplo_alerta_naranja.png)

*🟠 Aviso naranja · Área metropolitana de Tenerife*

![AEMET Alertas Card - Aviso amarillo en Ampurdán](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/Ejemplo_alerta_amarilla.png)

*🟡 Aviso amarillo · Costa - Ampurdán*

### Características de la tarjeta

- 🟡🟠🔴 Colores dinámicos según el nivel del aviso.
- 📋 Modo compacto para dashboards principales.
- 🔎 Modo detallado con toda la información disponible.
- 🔄 Modo automático: detallado cuando existen avisos y compacto cuando no los hay.
- 🌧️ Soporte para múltiples avisos activos.
- 📱 Diseño responsive basado en el ancho real de la tarjeta.
- 🖥️ Adaptación a tablets, escritorio y dashboards panorámicos.
- 🧱 Compatibilidad con getGridOptions() de Home Assistant Sections.
- ↔️ Redimensionamiento desde el editor de Home Assistant.
- 🧩 Editor visual nativo para configurar las opciones principales.
- 🌙 Compatibilidad con temas claro y oscuro.
- 🧩 Sin dependencias externas ni Browser Mod.
- 🧭 Enlace directo al aviso publicado por AEMET cuando está disponible.
- 🧱 Integración con el selector de tarjetas de Home Assistant.

### Requisitos de la tarjeta

- Home Assistant.
- AEMET Alertas instalada y cargada.

La tarjeta no consulta AEMET directamente: utiliza los datos y atributos de las entidades creadas por la integración.

### Configuración mediante el editor visual

Al añadir una tarjeta AEMET Alertas podrás configurar desde la interfaz:

- 📍 Localización y entidad de AEMET.
- 🎛️ Nivel de aviso.
- 🖥️ Modo de visualización: Automático, Compacto o Detallado.
- 👁️ Mostrar u ocultar la tarjeta cuando no haya avisos.
- 🔢 Número máximo de avisos.

No es necesario escribir YAML para utilizar las opciones principales.

### 📋 Modo compacto

Ideal para la pantalla principal del dashboard:

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: compact
~~~

Muestra el nivel, la zona, el número de avisos y un resumen de los fenómenos activos.

### 🔎 Modo detallado

Para una vista meteorológica específica:

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
~~~

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

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: auto
~~~

Con el modo automático, la tarjeta utiliza el modo detallado cuando existen avisos activos y muestra un estado limpio cuando no hay avisos.

### 👁️ Ocultar la tarjeta cuando no hay avisos

Por defecto, la tarjeta se muestra aunque no existan avisos. Puedes ocultarla completamente con:

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: compact
show_when_clear: false
~~~

### 🔢 Limitar el número de avisos

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
max_alerts: 3
~~~

El valor predeterminado es 5.

### 🟢🟡🟠🔴 Cómo funcionan los niveles

El nivel seleccionado en la tarjeta es un **filtro específico**, no acumulativo.

Por ejemplo, una tarjeta configurada para el nivel amarillo muestra los avisos amarillos, no los amarillos, naranjas y rojos conjuntamente.

Si quieres visualizar los cuatro niveles en tu dashboard, puedes crear una tarjeta para cada nivel y utilizar las condiciones de visibilidad de Home Assistant para mostrar cada una únicamente cuando el nivel correspondiente esté activo.

---

## 📐 Diseño responsive y layout

La tarjeta utiliza el ancho real que Home Assistant le asigna. Esto evita que el diseño dependa del tamaño de la pantalla cuando la tarjeta solo ocupa una parte del dashboard.

El diseño cambia automáticamente según el espacio disponible:

| Ancho aproximado de la tarjeta | Layout |
|---|---|
| Menos de 560 px | 📱 Vertical, optimizado para móvil |
| 560–759 px | 📲 Horizontal compacto, pensado para tablet |
| 760–1099 px | 🖥️ Horizontal amplio, con métricas en 3 columnas |
| 1100–1399 px | 🖥️ Escritorio ancho |
| 1400 px o más | 🖥️ Pantallas grandes y wall dashboards |

No importa si utilizas un móvil, iPad, portátil o PC: la tarjeta responde al espacio que realmente tiene.

### 🧱 Home Assistant Sections y grid_options

En los dashboards modernos de tipo **Sections**, Home Assistant utiliza una cuadrícula de 12 columnas.

Puedes modificar el ancho desde el editor visual o mediante grid_options:

~~~yaml
type: custom:aemet-alertas-card
entity: sensor.alertas_amarillas_litoral_norte_de_valencia
mode: detailed
grid_options:
  columns: 12
  rows: 8
~~~

Para una tarjeta a media anchura:

~~~yaml
grid_options:
  columns: 6
  rows: 8
~~~

> 💡 **Recomendación:** en escritorio y wall dashboards, utiliza una tarjeta de 9 o 12 columnas para aprovechar el layout horizontal. En móvil, Home Assistant normalmente la mostrará a ancho completo.

---

## ⚙️ Configuración de la integración

El asistente de configuración permite seleccionar:

1. Provincia.
2. Zona oficial de AEMET.
3. Niveles a monitorizar.
4. Fenómenos a monitorizar.

Las provincias y zonas disponibles se obtienen dinámicamente de AEMET, evitando depender de listados geográficos mantenidos manualmente.

### 1. Selección de provincia

![Selección de provincia en AEMET Alertas](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/02-provincia.png)

La provincia se selecciona desde el asistente de configuración.

### 2. Selección de zona oficial

![Selección de zona oficial de AEMET](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/03-zona.png)

La integración utiliza las zonas oficiales de avisos de AEMET.

### 3. Dispositivo y asignación a un área

![Asignación del dispositivo AEMET Alertas a un área](https://raw.githubusercontent.com/jacumal/aemet-alertas/main/assets/screenshots/04-asignacion.png)

Cada zona configurada se representa como un dispositivo y puede asignarse a un área de la vivienda, igual que cualquier otra integración de Home Assistant.

La configuración puede modificarse posteriormente desde las opciones de la integración.

---

## 📊 Entidades disponibles

Por cada zona configurada, AEMET Alertas crea un dispositivo con sus entidades asociadas.

### Sensores

- **Total avisos activos**
- **N.º alertas verdes**
- **N.º alertas amarillas**
- **N.º alertas naranjas**
- **N.º alertas rojas**
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

## 🤖 Automatizaciones

AEMET Alertas está pensado para integrarse directamente con las automatizaciones de Home Assistant.

### 🔴 Avisar al móvil cuando aparece una alerta roja

~~~yaml
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
~~~

### 🟠 Encender una luz cuando aparece una alerta naranja

~~~yaml
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
~~~

> Los nombres exactos de las entidades dependen de la zona configurada en Home Assistant.

---

## ⚡ Eventos para automatizaciones avanzadas

La entidad Event permite reaccionar cuando AEMET detecta cambios en los avisos:

~~~text
new_alert
updated_alert
ended_alert
~~~

Esto permite construir notificaciones inteligentes, registrar el histórico de avisos o activar escenas dependiendo del tipo de cambio detectado.

---

## 🛰️ Fuente de datos

Los datos se obtienen directamente de los canales oficiales de AEMET para las zonas de aviso y de los mensajes **CAP 1.2** publicados por AEMET.

La integración procesa, entre otros elementos:

- Catálogo oficial de zonas.
- Fichero de estado de avisos.
- Mensajes CAP 1.2.
- Nivel oficial AEMET-Meteoalerta.
- Información oficial del fenómeno y parámetros CAP.

La integración **no depende de MeteoAlarm ni de Feedreader**.

Para las condiciones de reutilización de los datos, consulta el [aviso legal de AEMET](https://www.aemet.es/es/nota_legal).

---

## ❓ Preguntas frecuentes

### ¿Tengo que instalar AEMET Alertas Card por separado?

**No.** La tarjeta Lovelace está incluida en la integración AEMET Alertas. Ambos componentes se instalan conjuntamente.

### He instalado AEMET Alertas, pero no encuentro la tarjeta. ¿Qué hago?

Comprueba que la integración se ha cargado correctamente. Después, recarga el navegador o la aplicación de Home Assistant para actualizar los recursos del frontend.

### ¿Tengo que añadir un recurso JavaScript manualmente?

En la configuración estándar de Lovelace, **no**. La integración registra automáticamente el recurso de la tarjeta.

Si utilizas resource_mode: yaml, Home Assistant no permite que la integración gestione automáticamente los recursos Lovelace. En ese caso tendrás que añadir manualmente el recurso:

~~~yaml
url: /aemet_alertas/aemet-alertas-card-responsive.js?v=1.0.6
type: module
~~~

Añádelo a la configuración de recursos de tu dashboard YAML, manteniendo la URL correspondiente a la versión instalada.

### ¿Tengo que reiniciar Home Assistant después de instalar?

Depende del método de instalación:

- **Marketplace (primera instalación):** normalmente no. Si la integración puede cargarse en caliente, Home Assistant abre directamente el asistente de configuración.
- **HACS:** reinicia Home Assistant después de instalar para cargar la integración.
- **Instalación manual:** reinicia Home Assistant después de copiar los archivos.
- **Actualización de una versión existente:** puede requerir reinicio para cargar el nuevo código Python. Marketplace te avisará cuando sea necesario.

Si la tarjeta no aparece después de instalarla, prueba primero a recargar el frontend.

### ¿La tarjeta consulta AEMET directamente?

No. La integración obtiene y procesa los datos oficiales. La tarjeta utiliza las entidades y atributos que genera AEMET Alertas.

### ¿El nivel de la tarjeta es acumulativo?

No. Cada tarjeta filtra un nivel concreto. Para mostrar varios niveles, crea una tarjeta para cada uno y utiliza condiciones de visibilidad para mostrarla cuando corresponda.

### ¿Necesito MeteoAlarm o Feedreader?

No. AEMET Alertas obtiene la información directamente de los canales oficiales de AEMET.

### ¿Puedo monitorizar varias zonas?

Sí. Puedes configurar las zonas que necesites mediante la integración y utilizar sus entidades en dashboards y automatizaciones.

---

## ☕️ Apoya el proyecto

Si **AEMET Alertas** te resulta útil y quieres apoyar su mantenimiento y desarrollo, puedes invitarme a un café a través de **Buy Me a Coffee**:

<div align="center">
<a href="https://www.buymeacoffee.com/jacumal">
<img src="https://img.shields.io/badge/☕️%20Buy%20Me%20a%20Coffee-Apoyar%20el%20proyecto-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=000000" alt="Buy Me a Coffee">
</a>
</div>

El apoyo es totalmente opcional y ayuda a dedicar tiempo a nuevas funciones, mantenimiento, documentación y soporte de la integración.

---

## 🛠️ Desarrollo y calidad

El repositorio incorpora validación automática mediante **HACS** y **Home Assistant Hassfest** en cada cambio.

Antes de publicar una versión se comprueba que la integración mantiene una estructura compatible con los validadores de Home Assistant y HACS.

Las sugerencias, mejoras y reportes de errores son bienvenidos a través de [GitHub Issues](https://github.com/jacumal/aemet-alertas/issues).

---

## 📌 Estado del proyecto

**Versión actual: 1.0.6**

La versión 1.0.6 corrige el registro del editor visual de la tarjeta Lovelace mediante getConfigElement() estático y fuerza la recarga de los módulos JavaScript con una URL versionada para evitar que el navegador reutilice código antiguo en caché.

El editor permite seleccionar la localización y el nivel de aviso, resolviendo internamente la entidad binaria correspondiente.

La tarjeta continúa integrada en la propia integración, sin necesidad de instalarla por separado.

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

Este proyecto se distribuye bajo licencia **MIT**. Consulta el archivo LICENSE para más información.

## 👨‍💻 Créditos

Desarrollado por **Javi / [@jacumal](https://github.com/jacumal)** para la comunidad de Home Assistant.

AEMET y sus contenidos meteorológicos son propiedad de la **Agencia Estatal de Meteorología**. Este proyecto utiliza dichos datos como fuente y no reclama ninguna titularidad sobre ellos.

---

<div align="center">

**AEMET Alertas · Home Assistant · Avisos meteorológicos**

</div>