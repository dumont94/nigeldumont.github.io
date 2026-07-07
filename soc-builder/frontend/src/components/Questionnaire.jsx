/**
 * Questionnaire.jsx — The four input questions.
 *
 * Frames the tool from a SOC engineer's point of view: you just
 * walked into a company as the first (or only) security hire —
 * what's the environment, how big is it, what already exists,
 * and what's the budget? The answers route to one of three
 * build paths (Microsoft-native, open-source/lean, best-of-breed).
 *
 * A visibility banner explains the core philosophy: every path
 * covers all ten monitoring domains — budget changes the tooling,
 * never whether a domain gets covered.
 */

import { useState } from "react";

// ── Option data ───────────────────────────────────────────────────

const ENVIRONMENTS = [
  {
    id: "m365",
    label: "Microsoft 365 / Azure",
    desc: "Exchange Online, Entra ID, Teams — a Microsoft-first shop",
  },
  {
    id: "hybrid",
    label: "Hybrid — Cloud + On-Prem",
    desc: "On-prem AD and servers plus cloud apps; a bit of everything",
  },
  {
    id: "gws",
    label: "Google Workspace / Mixed SaaS",
    desc: "Gmail, assorted SaaS, little to no Microsoft footprint",
  },
];

const SIZES = [
  { id: "1-50",   label: "1–50 people",   desc: "You are probably the whole security team" },
  { id: "51-250", label: "51–250 people", desc: "Small IT team, security is becoming a role" },
  { id: "251+",   label: "251+ people",   desc: "Dedicated security function taking shape" },
];

const MATURITY_LEVELS = [
  {
    id: "greenfield",
    label: "Nothing Formal",
    desc: "No EDR, no central logging, no policies — a true blank slate",
  },
  {
    id: "basics",
    label: "Some Basics",
    desc: "AV installed, MFA partially rolled out, but nothing centralized",
  },
  {
    id: "unwatched",
    label: "Tools, No Eyes",
    desc: "Security products exist but nobody is actually watching them",
  },
];

const BUDGETS = [
  {
    id: "lean",
    label: "Lean",
    desc: "Squeeze existing licensing and open source; every dollar is argued for",
  },
  {
    id: "funded",
    label: "Funded",
    desc: "Leadership has committed real budget — buy best-of-breed where it counts",
  },
];

// ── Component ─────────────────────────────────────────────────────

export default function Questionnaire({ onSubmit, error }) {
  const [formData, setFormData] = useState({
    environment: "m365",
    size: "1-50",
    maturity: "greenfield",
    budget: "lean",
  });

  function select(field, value) {
    setFormData((prev) => ({ ...prev, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(formData);
  }

  return (
    <div className="questionnaire">
      {/* ── Hero ── */}
      <div className="questionnaire__hero">
        <div className="questionnaire__eyebrow">SOC Foundations Builder</div>
        <h1 className="questionnaire__title">Build your own security posture.</h1>
        <p className="questionnaire__subtitle">
          Answer four questions. Get a 10-step plan to monitor and secure
          a company — the checks, the tools, and the costs.
        </p>
        <p className="questionnaire__byline">Built by Nigel Dumont</p>
      </div>

      {/* ── Error ── */}
      {error && (
        <div className="error-card" style={{ marginBottom: "var(--space-8)" }}>
          <div className="error-card__icon">⚠</div>
          <div className="error-card__title">Something went wrong</div>
          <div className="error-card__message">{error}</div>
        </div>
      )}

      <form className="questionnaire__form" onSubmit={handleSubmit}>

        {/* ── Q1: Environment ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">1</span>
            Environment
          </div>
          <div className="question-block__title">What does the company run on?</div>
          <div className="option-grid">
            {ENVIRONMENTS.map((env) => (
              <OptionCard
                key={env.id}
                label={env.label}
                desc={env.desc}
                selected={formData.environment === env.id}
                onClick={() => select("environment", env.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Q2: Size ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">2</span>
            Company Size
          </div>
          <div className="question-block__title">How many people are you defending?</div>
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

        {/* ── Q3: Current state ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">3</span>
            Current State
          </div>
          <div className="question-block__title">What security exists today?</div>
          <div className="option-grid">
            {MATURITY_LEVELS.map((m) => (
              <OptionCard
                key={m.id}
                label={m.label}
                desc={m.desc}
                selected={formData.maturity === m.id}
                onClick={() => select("maturity", m.id)}
              />
            ))}
          </div>
        </div>

        {/* ── Q4: Visibility banner + Budget ── */}
        <div className="question-block">
          <div className="question-block__label">
            <span className="question-block__number">4</span>
            Budget
          </div>
          <div className="question-block__title">What's the budget posture?</div>

          {/* Philosophy note — this is not a question, it's a statement */}
          <div className="security-banner">
            <div className="security-banner__icon">👁</div>
            <div>
              <div className="security-banner__title">Coverage philosophy: visibility before shiny tools</div>
              <div className="security-banner__body">
                Every path in this tool covers the same ten domains — inventory, identity,
                endpoints, logging, email, vulnerabilities, network, detections, and incident
                response. There is no "skip monitoring" option. Budget only determines
                <em> which tools</em> do the work — not whether a domain gets covered.
              </div>
            </div>
          </div>

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

        {/* ── Submit ── */}
        <div className="questionnaire__submit">
          <button type="submit" className="btn btn--primary btn--lg btn--full">
            Build My 90-Day Plan →
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
