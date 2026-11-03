class AemetAlertasCardEditor extends HTMLElement {
  setConfig(config) {
    this._config = {
      ...config,
      type: config?.type || "custom:aemet-alertas-card",
    };
    this._renderForm();
  }

  set hass(hass) {
    this._hass = hass;
    if (this._form) this._renderForm();
  }

  _getAlertEntities() {
    const states = Object.values(this._hass?.states || {});
    return states
      .filter((state) =>
        state.entity_id.startsWith("binary_sensor.") &&
        typeof state.attributes?.area === "string" &&
        ["green", "yellow", "orange", "red"].includes(state.attributes?.nivel) &&
        Array.isArray(state.attributes?.avisos)
      )
      .map((state) => ({
        entity: state.entity_id,
        area: state.attributes.area,
        level: state.attributes.nivel,
      }));
  }

  _getSelection(entities) {
    const currentEntity = this._config?.entity;
    const current = entities.find((item) => item.entity === currentEntity);
    const area = this._config?.area || current?.area || entities[0]?.area || "";
    const levels = entities.filter((item) => item.area === area);
    const level = this._config?.level || current?.level ||
      (levels.some((item) => item.level === "yellow") ? "yellow" : levels[0]?.level || "yellow");
    const selected = levels.find((item) => item.level === level) || levels[0];
    return { area, level: selected?.level || level, entity: selected?.entity || "" };
  }

  _renderForm() {
    if (!this._hass || !customElements.get("ha-form")) {
      setTimeout(() => this._renderForm(), 50);
      return;
    }

    const entities = this._getAlertEntities();
    const selection = this._getSelection(entities);
    const areas = [...new Set(entities.map((item) => item.area))].sort((a, b) => a.localeCompare(b, "es"));
    const areaOptions = areas.map((area) => ({ value: area, label: area }));
    const levelLabels = {
      green: "Verde",
      yellow: "Amarilla",
      orange: "Naranja",
      red: "Roja",
    };
    // Always offer all four official levels, even when no alert is active.
    // Each location has one binary sensor per level; an empty avisos array
    // is a valid state and the card renders its "Sin avisos" presentation.
    const levelOptions = ["green", "yellow", "orange", "red"]
      .map((level) => ({ value: level, label: levelLabels[level] }));

    if (!this._form) {
      this._form = document.createElement("ha-form");
      this._form.addEventListener("value-changed", (event) => {
        const values = event.detail.value || {};
        const available = this._getAlertEntities();
        const nextArea = values.area || this._config.area;
        const nextLevel = values.level || this._config.level || "yellow";
        const match = available.find((item) => item.area === nextArea && item.level === nextLevel)
          || available.find((item) => item.area === nextArea);
        this._config = {
          ...this._config,
          ...values,
          area: nextArea,
          level: match?.level || nextLevel,
          entity: match?.entity || this._config.entity,
          type: "custom:aemet-alertas-card",
        };
        this._renderForm();
        this.dispatchEvent(new CustomEvent("config-changed", {
          detail: { config: this._config },
          bubbles: true,
          composed: true,
        }));
      });
      this.appendChild(this._form);
    }

    this._form.hass = this._hass;
    this._form.data = {
      area: selection.area,
      level: selection.level,
      mode: this._config?.mode || "auto",
      show_when_clear: this._config?.show_when_clear !== false,
      max_alerts: Number(this._config?.max_alerts) || 5,
    };
    this._form.schema = [
      {
        name: "area",
        label: "Localización",
        required: true,
        selector: {
          select: {
            options: areaOptions,
            mode: "dropdown",
          },
        },
      },
      {
        name: "level",
        label: "Nivel de aviso",
        required: true,
        selector: {
          select: {
            options: levelOptions,
            mode: "dropdown",
          },
        },
      },
      {
        name: "mode",
        label: "Modo de visualización",
        selector: {
          select: {
            options: [
              { value: "auto", label: "Automático" },
              { value: "compact", label: "Compacto" },
              { value: "detailed", label: "Detallado" },
            ],
            mode: "dropdown",
          },
        },
      },
      {
        name: "show_when_clear",
        label: "Mostrar tarjeta cuando no haya avisos",
        selector: { boolean: {} },
      },
      {
        name: "max_alerts",
        label: "Número máximo de avisos",
        selector: {
          number: { min: 1, max: 20, step: 1, mode: "box" },
        },
      },
    ];
  }
}

if (!customElements.get("aemet-alertas-card-editor")) {
  customElements.define("aemet-alertas-card-editor", AemetAlertasCardEditor);
}

customElements.whenDefined("aemet-alertas-card").then(() => {
  const Card = customElements.get("aemet-alertas-card");
  if (!Card.getConfigElement) {
    Card.getConfigElement = () => document.createElement("aemet-alertas-card-editor");
  }
});
