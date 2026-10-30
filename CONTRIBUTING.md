# Contributing to AEMET Alertas

¡Gracias por tu interés en mejorar AEMET Alertas! 💙

Este proyecto es una integración personalizada de Home Assistant y las contribuciones, ideas y reportes de errores son bienvenidos.

## 🐛 Reportar un error

Antes de abrir un issue:

1. Comprueba que estás utilizando la versión más reciente.
2. Revisa los issues existentes para evitar duplicados.
3. Incluye la versión de Home Assistant y la versión de AEMET Alertas.
4. Describe los pasos necesarios para reproducir el problema.
5. Si es posible, incluye los registros relevantes de Home Assistant.

No incluyas tokens, credenciales, información personal ni datos sensibles.

## 💡 Proponer una mejora

Las nuevas funcionalidades pueden proponerse mediante GitHub Issues. Explica:

- qué problema resuelve;
- cuál sería el comportamiento esperado;
- por qué sería útil para otros usuarios de Home Assistant;
- y, si es posible, una propuesta de implementación.

## 🔧 Desarrollo

La integración se encuentra en:

```text
custom_components/aemet_alertas/
```

Los cambios deben mantener la compatibilidad con las convenciones de Home Assistant y evitar dependencias innecesarias.

## ✅ Validaciones

El repositorio utiliza automáticamente:

- **HACS validation**
- **Home Assistant Hassfest**

Los cambios deberían dejar ambas validaciones en estado correcto.

## 🔀 Pull requests

Para una pull request:

1. Describe claramente el cambio.
2. Explica cómo lo has probado.
3. Mantén el alcance de la PR lo más acotado posible.
4. Actualiza la documentación cuando el comportamiento visible de la integración cambie.
5. No incluyas cambios de formato o refactorizaciones no relacionados salvo que sean necesarios.

## 📸 Cambios de interfaz

Si una modificación afecta al flujo de configuración, entidades o interfaz de Home Assistant, añade capturas actualizadas cuando ayuden a documentar el cambio.

## ⚖️ AEMET y fuentes de datos

AEMET Alertas es un proyecto independiente y no está afiliado, patrocinado, respaldado ni mantenido por AEMET. Las contribuciones deben respetar las condiciones de reutilización aplicables a los datos de AEMET.

---

Gracias por contribuir a hacer más útiles los avisos meteorológicos en Home Assistant. 🌦️
