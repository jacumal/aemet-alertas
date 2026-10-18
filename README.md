# AEMET Alertas

Integración personalizada para [Home Assistant](https://www.home-assistant.io/) que obtiene los avisos meteorológicos oficiales de AEMET directamente desde sus canales Atom y procesa los mensajes CAP 1.2 publicados para cada zona de aviso.

**AEMET Alertas es un proyecto independiente y no está afiliado, patrocinado, respaldado ni mantenido por AEMET.**

La integración es independiente de MeteoAlarm y Feedreader.

## Características

- Catálogo de provincias y zonas obtenido directamente de AEMET.
- Configuración mediante la interfaz de Home Assistant: **provincia → zona → niveles → fenómenos**.
- Lectura del fichero de estado completo (`tar.gz`) publicado por AEMET.
- Procesado de mensajes CAP 1.2.
- Lectura del nivel oficial desde `AEMET-Meteoalerta nivel`.
- Soporte para los cuatro niveles oficiales:
  - Verde
  - Amarillo
  - Naranja
  - Rojo
- Identificación del fenómeno mediante la información oficial de AEMET y los parámetros CAP.
- Filtros configurables por nivel y fenómeno.
- Sensor de avisos activos con información detallada.
- Sensores para el número de avisos por nivel.
- Sensores de fenómenos activos por nivel.
- Cuatro sensores binarios por zona, uno para cada nivel de alerta.
- Entidad `Event` para detectar:
  - Nuevos avisos
  - Avisos actualizados
  - Avisos finalizados
- Identificación de entidades mediante la zona de AEMET para evitar conflictos cuando se configuran varias zonas.
- Agrupación de las entidades por dispositivo en Home Assistant.
- Branding propio e independiente.

## Instalación mediante HACS

AEMET Alertas puede instalarse como repositorio personalizado de HACS mientras el proyecto no forme parte del catálogo oficial.

1. Abre **HACS → Integraciones**.
2. Abre el menú de tres puntos y selecciona **Repositorios personalizados**.
3. Añade:

   `https://github.com/jacumal/aemet-alertas`

4. Selecciona **Integration** como categoría.
5. Instala **AEMET Alertas**.
6. Reinicia Home Assistant.

## Instalación manual

Copia el directorio `custom_components/aemet_alertas` en:

```text
/config/custom_components/aemet_alertas
```

Después reinicia Home Assistant.

## Configuración

Después del reinicio, ve a:

**Configuración → Dispositivos y servicios → Añadir integración → AEMET Alertas**

Selecciona la provincia y, a continuación, la zona oficial de avisos de AEMET.

La integración permite configurar los niveles y fenómenos que se quieren monitorizar.

## Entidades

Para cada zona configurada se crean entidades para:

- Total de avisos activos.
- Número de alertas rojas, naranjas, amarillas y verdes.
- Fenómenos activos por cada nivel.
- Alerta roja.
- Alerta naranja.
- Alerta amarilla.
- Alerta verde.
- Eventos de alertas.

La entidad de eventos utiliza los tipos:

- `new_alert`
- `updated_alert`
- `ended_alert`

## Fuentes de datos

Los datos proceden directamente de los canales oficiales de AEMET para las zonas de aviso y de los mensajes CAP 1.2 publicados por AEMET.

La reutilización de información de AEMET debe respetar las condiciones establecidas por la propia Agencia. Para más información, consulta el [aviso legal de AEMET](https://www.aemet.es/es/nota_legal).

Cuando corresponda, debe indicarse AEMET como fuente de la información. Este proyecto no debe presentarse como un producto oficial de AEMET ni dar a entender que AEMET lo patrocina, respalda o mantiene.

## Ejemplo de automatización

Ejemplo sencillo para reaccionar ante una alerta roja:

```yaml
alias: Aviso AEMET - Alerta roja
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

El nombre exacto de la entidad dependerá de la zona configurada.

## Estado del proyecto

**Versión 1.0.0**

Primera versión preparada para pruebas y distribución como integración personalizada de Home Assistant.

## Aviso legal y marca

AEMET Alertas utiliza información meteorológica publicada por la Agencia Estatal de Meteorología (AEMET).

**Este proyecto no es oficial de AEMET y no está afiliado, patrocinado, respaldado ni mantenido por AEMET.**

El nombre AEMET se utiliza únicamente para identificar la fuente de los datos meteorológicos utilizados por esta integración. La identidad visual del proyecto es independiente y no pretende reproducir la imagen corporativa oficial de AEMET.

Consulta las condiciones de reutilización de AEMET antes de redistribuir o utilizar los datos obtenidos mediante esta integración:

https://www.aemet.es/es/nota_legal

## Licencia

Este proyecto se distribuye bajo licencia MIT. Consulta el archivo `LICENSE` incluido en el repositorio para más información.

## Créditos

Desarrollado por **Javi / jacumal** para la comunidad de Home Assistant.

AEMET y sus contenidos meteorológicos son propiedad de la **Agencia Estatal de Meteorología**. Este proyecto utiliza dichos datos como fuente y no reclama ninguna titularidad sobre ellos.
