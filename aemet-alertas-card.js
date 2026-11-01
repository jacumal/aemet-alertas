/*
 * AEMET Alertas Card
 * Lovelace dashboard card for the AEMET Alertas integration.
 *
 * This card is intentionally dependency-free and uses Home Assistant's
 * existing frontend components and theme variables.
 */

class AemetAlertCard extends HTMLElement {
  static getStubConfig() {
    return {
      entity: "sensor.alertas_amarillas_litoral_norte_de_valencia",
      mode: "compact",
    };
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("AEMET Alertas Card: 'entity' is required");
    }

    this.config = {
      mode: "compact",
      show_when_clear: true,
      max_alerts: 5,
      ...config,
    };

    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return this.config?.mode === "detailed" ? 7 : 2;
  }

  _getState() {
    return this._hass?.states?.[this.config?.entity];
  }

  _getAlerts(state) {
    if (!state) return [];

    const alerts = state.attributes?.avisos;
    if (Array.isArray(alerts)) return alerts.slice(0, this.config.max_alerts);

    return [];
  }

  _getLevel(state, alerts) {
    const value = state?.attributes?.nivel || alerts?.[0]?.level;
    return ["green", "yellow", "orange", "red"].includes(value)
      ? value
      : "green";
  }

  _getLevelLabel(level) {
    return {
      green: "Sin aviso",
      yellow: "Aviso amarillo",
      orange: "Aviso naranja",
      red: "Aviso rojo",
    }[level];
  }

  _getLevelColor(level) {
    return {
      green: "#43a047",
      yellow: "#f9a825",
      orange: "#ef6c00",
      red: "#d32f2f",
    }[level];
  }

  _getLevelIcon(level) {
    return {
      green: "mdi:weather-sunny",
      yellow: "mdi:weather-rainy",
      orange: "mdi:weather-lightning-rainy",
      red: "mdi:alert-octagon",
    }[level];
  }

  _getAlertIcon(alert) {
    const text = `${alert?.event || ""} ${alert?.description || ""}`.toLowerCase();

    if (text.includes("torment")) return "mdi:weather-lightning-rainy";
    if (text.includes("lluv") || text.includes("precipit")) return "mdi:weather-rainy";
    if (text.includes("viento")) return "mdi:weather-windy";
    if (text.includes("nieve")) return "mdi:weather-snowy";
    if (text.includes("temperatura") || text.includes("calor")) return "mdi:thermometer-alert";
    if (text.includes("oleaje") || text.includes("costa")) return "mdi:waves";
    return "mdi:alert-outline";
  }

  _formatDate(value) {
    if (!value) return "—";

    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;

    return new Intl.DateTimeFormat("es-ES", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  }

  _escape(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  _icon(name, className = "") {
    return `<ha-icon icon="${this._escape(name)}" class="${className}"></ha-icon>`;
  }

  _render() {
    if (!this.config || !this._hass) return;

    const state = this._getState();
    if (!state) {
      this.innerHTML = this._styles() + this._empty("Entidad no disponible");
      return;
    }

    const alerts = this._getAlerts(state);
    const level = this._getLevel(state, alerts);
    const hasAlerts = alerts.length > 0 || Number(state.state) > 0;

    if (!hasAlerts && this.config.show_when_clear === false) {
      this.innerHTML = "";
      return;
    }

    this.innerHTML = this._styles();

    if (this.config.mode === "detailed") {
      this.innerHTML += this._detailed(state, alerts, level);
    } else {
      this.innerHTML += this._compact(state, alerts, level);
    }
  }

  _compact(state, alerts, level) {
    const color = this._getLevelColor(level);
    const first = alerts[0];
    const area = first?.area_desc || state.attributes?.area || "Zona configurada";
    const event = first?.event || "No hay avisos activos";
    const count = Number(state.attributes?.total_avisos ?? alerts.length ?? 0);

    return `
      <ha-card class="compact" style="--aemet-level:${color}">
        <div class="compact-inner">
          <div class="level-icon">${this._icon(this._getLevelIcon(level))}</div>
          <div class="summary">
            <div class="topline">
              <span class="brand">AEMET</span>
              <span class="badge">${this._escape(this._getLevelLabel(level))}</span>
            </div>
            <div class="event">${this._escape(event)}</div>
            <div class="area">${this._escape(area)}</div>
          </div>
          <div class="count">
            <strong>${count}</strong>
            <span>${count === 1 ? "aviso" : "avisos"}</span>
          </div>
        </div>
      </ha-card>
    `;
  }

  _detailed(state, alerts, level) {
    const color = this._getLevelColor(level);
    const area = state.attributes?.area || alerts[0]?.area_desc || "Zona configurada";
    const total = Number(state.attributes?.total_avisos ?? alerts.length ?? 0);

    return `
      <ha-card class="detailed" style="--aemet-level:${color}">
        <div class="header">
          <div class="header-icon">${this._icon(this._getLevelIcon(level))}</div>
          <div class="header-copy">
            <div class="eyebrow">AEMET · AVISOS METEOROLÓGICOS</div>
            <div class="title">${this._escape(this._getLevelLabel(level))}</div>
            <div class="area">${this._escape(area)}</div>
          </div>
          <div class="total"><strong>${total}</strong><span>activos</span></div>
        </div>

        <div class="content">
          ${alerts.length ? alerts.map((alert, index) => this._alert(alert, index)).join("") : this._emptyContent()}
        </div>
      </ha-card>
    `;
  }

  _alert(alert, index) {
    const level = alert.level || "yellow";
    const color = this._getLevelColor(level);
    const title = alert.event || alert.headline || "Aviso meteorológico";
    const parameter = alert.parameter || alert.description || "—";
    const probability = alert.probability || "—";
    const severity = alert.severity || "—";
    const certainty = alert.certainty || "—";
    const urgency = alert.urgency || "—";
    const source = alert.source_url;

    return `
      <section class="alert" style="--alert-level:${color}">
        <div class="alert-title-row">
          <div class="alert-icon">${this._icon(this._getAlertIcon(alert))}</div>
          <div>
            <div class="alert-title">${this._escape(title)}</div>
            <div class="alert-location">${this._escape(alert.area_desc || "Zona de aviso")}</div>
          </div>
          <span class="alert-level">${this._escape(this._getLevelLabel(level))}</span>
        </div>

        <div class="grid">
          ${this._metric("Parámetro", parameter)}
          ${this._metric("Probabilidad", probability)}
          ${this._metric("Severidad", severity)}
          ${this._metric("Certeza", certainty)}
          ${this._metric("Urgencia", urgency)}
          ${this._metric("Inicio", this._formatDate(alert.onset))}
          ${this._metric("Fin", this._formatDate(alert.expires))}
          ${this._metric("Actualizado", this._formatDate(alert.sent))}
        </div>

        ${alert.description ? `<div class="block"><div class="label">Descripción</div><div>${this._escape(alert.description)}</div></div>` : ""}
        ${alert.instruction ? `<div class="instruction"><div class="label">Recomendación</div><div>${this._escape(alert.instruction)}</div></div>` : ""}
        ${source ? `<a class="source" href="${this._escape(source)}" target="_blank" rel="noopener">${this._icon("mdi:open-in-new")} Fuente oficial AEMET</a>` : ""}
      </section>
    `;
  }

  _metric(label, value) {
    return `<div class="metric"><span>${this._escape(label)}</span><strong>${this._escape(value)}</strong></div>`;
  }

  _empty(message = "Sin avisos activos") {
    return `<ha-card class="empty"><div>${this._icon("mdi:weather-sunny")}</div><strong>${this._escape(message)}</strong></ha-card>`;
  }

  _emptyContent() {
    return `
      <div class="clear">
        ${this._icon("mdi:weather-sunny")}
        <strong>No hay avisos meteorológicos activos</strong>
        <span>La zona está actualmente sin alertas.</span>
      </div>
    `;
  }

  _styles() {
    return `
      <style>
        :host {
          display: block;
          --aemet-surface: var(--ha-card-background, var(--card-background-color, #fff));
          --aemet-text: var(--primary-text-color, #1c1c1c);
          --aemet-secondary: var(--secondary-text-color, #6f6f6f);
          --aemet-divider: var(--divider-color, rgba(127,127,127,.18));
        }

        ha-card {
          overflow: hidden;
          color: var(--aemet-text);
          background: var(--aemet-surface);
          border-radius: 20px;
          border: 1px solid var(--aemet-divider);
          box-shadow: none;
        }

        .compact {
          border-left: 5px solid var(--aemet-level);
        }

        .compact-inner {
          min-height: 92px;
          display: grid;
          grid-template-columns: auto 1fr auto;
          gap: 14px;
          align-items: center;
          padding: 14px 18px 14px 14px;
        }

        .level-icon, .header-icon {
          width: 48px;
          height: 48px;
          display: grid;
          place-items: center;
          border-radius: 15px;
          color: var(--aemet-level);
          background: color-mix(in srgb, var(--aemet-level) 13%, transparent);
        }

        .level-icon ha-icon { --mdc-icon-size: 28px; }

        .topline {
          display: flex;
          gap: 8px;
          align-items: center;
          margin-bottom: 3px;
        }

        .brand, .eyebrow {
          font-size: 11px;
          font-weight: 800;
          letter-spacing: .08em;
          opacity: .7;
        }

        .badge, .alert-level {
          padding: 3px 8px;
          border-radius: 999px;
          color: var(--aemet-level);
          background: color-mix(in srgb, var(--aemet-level) 13%, transparent);
          font-size: 11px;
          font-weight: 800;
        }

        .event {
          font-size: 15px;
          line-height: 1.25;
          font-weight: 750;
        }

        .area, .alert-location {
          color: var(--aemet-secondary);
          font-size: 12px;
          margin-top: 3px;
        }

        .count {
          min-width: 44px;
          text-align: center;
          color: var(--aemet-level);
        }

        .count strong, .total strong {
          display: block;
          font-size: 24px;
          line-height: 1;
        }

        .count span, .total span {
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: .05em;
          opacity: .65;
        }

        .header {
          display: grid;
          grid-template-columns: auto 1fr auto;
          gap: 14px;
          align-items: center;
          padding: 18px;
          border-bottom: 1px solid var(--aemet-divider);
          border-top: 5px solid var(--aemet-level);
        }

        .header-icon ha-icon { --mdc-icon-size: 27px; }
        .title { font-size: 20px; font-weight: 850; margin-top: 2px; }
        .total { text-align: center; color: var(--aemet-level); }

        .content { padding: 14px; }

        .alert {
          padding: 15px;
          border: 1px solid var(--aemet-divider);
          border-left: 4px solid var(--alert-level);
          border-radius: 16px;
          margin-bottom: 12px;
        }

        .alert:last-child { margin-bottom: 0; }

        .alert-title-row {
          display: grid;
          grid-template-columns: auto 1fr auto;
          gap: 11px;
          align-items: center;
          margin-bottom: 14px;
        }

        .alert-icon {
          color: var(--alert-level);
          width: 36px;
          height: 36px;
          display: grid;
          place-items: center;
          border-radius: 11px;
          background: color-mix(in srgb, var(--alert-level) 12%, transparent);
        }

        .alert-icon ha-icon { --mdc-icon-size: 21px; }
        .alert-title { font-weight: 800; font-size: 14px; line-height: 1.25; }

        .alert-level {
          color: var(--alert-level);
          background: color-mix(in srgb, var(--alert-level) 12%, transparent);
        }

        .grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 8px;
        }

        .metric {
          padding: 9px 10px;
          border-radius: 11px;
          background: color-mix(in srgb, var(--primary-text-color) 4%, transparent);
        }

        .metric span, .label {
          display: block;
          color: var(--aemet-secondary);
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: .04em;
          margin-bottom: 3px;
        }

        .metric strong { font-size: 12px; line-height: 1.25; }
        .block, .instruction { margin-top: 12px; font-size: 12px; line-height: 1.5; }

        .instruction {
          padding: 12px;
          border-radius: 12px;
          background: color-mix(in srgb, var(--alert-level) 7%, transparent);
        }

        .source {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          margin-top: 13px;
          color: var(--alert-level);
          text-decoration: none;
          font-size: 12px;
          font-weight: 800;
        }

        .source ha-icon { --mdc-icon-size: 15px; }

        .clear, .empty {
          padding: 28px 20px;
          text-align: center;
        }

        .clear ha-icon, .empty ha-icon {
          display: block;
          margin: 0 auto 10px;
          --mdc-icon-size: 34px;
          color: var(--primary-color);
        }

        .clear span { display: block; margin-top: 4px; color: var(--aemet-secondary); font-size: 12px; }

        @media (max-width: 520px) {
          .compact-inner { grid-template-columns: auto 1fr; }
          .count { grid-column: 2; text-align: left; }
          .header { grid-template-columns: auto 1fr; }
          .total { grid-column: 2; text-align: left; }
          .alert-title-row { grid-template-columns: auto 1fr; }
          .alert-level { grid-column: 2; justify-self: start; }
        }
      </style>
    `;
  }
}

customElements.define("aemet-alertas-card", AemetAlertCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "aemet-alertas-card",
  name: "AEMET Alertas Card",
  description: "Tarjeta visual para los avisos meteorológicos de AEMET Alertas.",
  preview: true,
  documentationURL: "https://github.com/jacumal/aemet-alertas",
});
