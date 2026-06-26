/**
 * Questionnaire.jsx — The four input questions.
 *
 * Renders a hero intro followed by four question blocks:
 *   1. Business type   (currently only Startup/Small Business is active)
 *   2. Team size       (1–10, 11–50, 51+)
 *   3. Budget          (Budget-Conscious vs. Enterprise)
 *   4. Management style (DIY vs. Fully Outsourced)
 *
 * A security posture info banner explains that all builds include
 * best-practice security — budget only changes the tooling, not
 * whether controls exist. This is an intentional design choice.
 *
 * To add a new business type: add an entry to BUSINESS_TYPES below,
 * remove the `disabled` flag, and ensure data.py includes it.
 */

import { useState } from "react";

// ── Option data ───────────────────────────────────────────────────

const BUSINESS_TYPES = [
  {
    id: "startup",
    label: "Startup / Small Business",
    desc: "Growing team, tight budget, building from scratch",
    disabled: false,
  },
  {
    id: "enterprise",
    label: "Enterprise",
    desc: "Multi-site, compliance-driven, large IT team",
    disabled: true,
    soon: true,
  },
  {
    id: "nonprofit",
    label: "Non-Profit / Education",
    desc: "Grant-funded, vendor discount programs",
    disabled: true,
    soon: true,
  },
];

const SIZES = [
  { id: "1-10",  label: "1–10 people",  desc: "Seed / early-stage" },
  { id: "11-50", label: "11–50 people", desc: "Series A / growth" },
  { id: "51+",   label: "51+ people",   desc: "Scaling up" },
];

const BUDGETS = [
  {
    id: "budget_conscious",
    label: "Budget-Conscious",
    desc: "Maximize value; lean on open-source and no-license gear where possible",
  },
  {
    id: "enterprise",
    label: "Enterprise-Grade",
    desc: "Redundancy, full observability, room to scale — willing to invest",
  },
];

const MANAGEMENT_STYLES = [
  {
    id: "diy",
    label: "DIY — I'll manage it",
    desc: "I want to learn, own the config, and run it myself (or with a small IT team)",
  },
  {
    id: "outsourced",
    label: "Fully Outsourced",
    desc: "I want a managed service provider to deploy, monitor, and maintain everything",
  },
];

// ── Component ─────────────────────────────────────────────────────

export default function Questionnaire({ onSubmit, error }) {
  const [formData, setFormData] = useState({
    businessType: "startup",
    size: "1-10",
    budget: "budget_conscious",
    managementStyle: "diy",
  });

  function select(field, value) {
    setFormData((prev) => ({ ...prev, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    // Map camelCase form state to snake_case API fields
    onSubmit({
      business_type:    formData.businessType,
      size:             formData.size,
      budget:           formData.budget,
      management_style: formData.managementStyle,
    });
  }

  return (
    <div className="questionnaire">
      {/* ── Hero ── */}
      <div className="questionnaire__hero">
        <div className="questionnaire__eyebrow">SOHO Network Builder</div>
        <h1 className="questionnaire__title">Your First Network</h1>
        <p className="questionnaire__subtitle">
          Answer four questions. Get a step-by-step guide to building a
          real business network from scratch — including the gear, the config,
          and the plain-English explanation of why it all matters.
        </p>
      </div>

      {/* ── Error ── */}
      {error && (
        <div className="error-card" style={{ marginBottom: "var(--space-8)" }}>
          <div className="error-card__icon">⚠</div>
          <div className="error-card__title">Something went wrong</div>
          <div className="error-card__message">
            {error}
            <br /><br />
            Make sure the Flask backend is running on port 5000:<br />
            <code style={{ fontFamily: "var(--mono)", fontSize: "12px" }}>
              cd backend && python app.py
            </code>
          </div>
        </div>
      )}

      <form className="questionnaire__form" onSubmit={handleSubmit}>

        {/* ── Q1: Business Type ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">1</span>
            Business Type
          </div>
          <div className="question-block__title">What kind of business is this for?</div>
          <div className="option-grid">
            {BUSINESS_TYPES.map((bt) => (
              <OptionCard
                key={bt.id}
                label={bt.label}
                desc={bt.desc}
                selected={formData.businessType === bt.id}
                disabled={bt.disabled}
                soon={bt.soon}
                onClick={() => !bt.disabled && select("businessType", bt.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Q2: Size ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">2</span>
            Team Size
          </div>
          <div className="question-block__title">How many people will use this network?</div>
          <div className="option-grid">
            {SIZES.map((s) => (
              <OptionCard
                key={s.id}
                label={s.label}
                desc={s.desc}
                selected={formData.size === s.id}
                onClick={() => select("size", s.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Q3: Budget ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">3</span>
            Budget
          </div>
          <div className="question-block__title">What's the budget posture?</div>
          <div className="option-grid option-grid--2col">
            {BUDGETS.map((b) => (
              <OptionCard
                key={b.id}
                label={b.label}
                desc={b.desc}
                selected={formData.budget === b.id}
                onClick={() => select("budget", b.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Q4: Security posture banner + Management style ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">4</span>
            Management Style
          </div>
          <div className="question-block__title">How do you want to run it?</div>

          {/* Security posture note — this is not a question, it's a statement */}
          <div className="security-banner">
            <div className="security-banner__icon">🔒</div>
            <div>
              <div className="security-banner__title">Security posture: always enterprise-grade</div>
              <div className="security-banner__body">
                Every build in this tool includes network segmentation (VLANs), encrypted wireless (WPA3),
                firewall with IPS, and monitoring. There is no "low security" option. Budget only
                determines <em>which tools</em> are used — not whether controls exist.
              </div>
            </div>
          </div>

          <div className="option-grid option-grid--2col">
            {MANAGEMENT_STYLES.map((m) => (
              <OptionCard
                key={m.id}
                label={m.label}
                desc={m.desc}
                selected={formData.managementStyle === m.id}
                onClick={() => select("managementStyle", m.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Submit ── */}
        <div className="questionnaire__submit">
          <button type="submit" className="btn btn--primary btn--lg btn--full">
            Build My Network →
          </button>
        </div>

      </form>
    </div>
  );
}

// ── OptionCard subcomponent ───────────────────────────────────────

function OptionCard({ label, desc, selected, disabled, soon, onClick }) {
  const classes = [
    "option-card",
    selected  ? "option-card--selected"  : "",
    disabled  ? "option-card--disabled"  : "",
  ].filter(Boolean).join(" ");

  return (
    <div className={classes} onClick={onClick} role="button" tabIndex={disabled ? -1 : 0}
      onKeyDown={(e) => e.key === "Enter" && !disabled && onClick()}>
      {soon && <span className="option-card__soon">Soon</span>}
      {selected && !disabled && <span className="option-card__check" />}
      <div className="option-card__title">{label}</div>
      <div className="option-card__desc">{desc}</div>
    </div>
  );
}
