/**
 * StepCard.jsx — Renders a single build step with all its sections.
 *
 * Each section is color-coded by purpose so a reader can scan quickly:
 *   Blue   — What is this?  (plain-English explanation)
 *   Amber  — Why it matters (the attacker's-eye justification)
 *   Red    — Day-one look-fors (what a SOC engineer checks first)
 *   Green  — Recommended stack (the "deploy" section)
 *   Gray   — Alternatives & trade-offs
 *   Teal   — Licensing & care-and-feeding notes
 *   Purple — Implementation steps (the hands-on part)
 */

export default function StepCard({ step }) {
  return (
    <div className="step-card">

      {/* ── Header ── */}
      <div className="step-card__header">
        <span className="step-card__num">Step {step.order} of 10</span>
        <h2 className="step-card__title">{step.title}</h2>
      </div>

      {/* ── What is this? ── */}
      <Section modifier="what" icon="●" title="What Is This?">
        <p className="section__text">{step.what}</p>
      </Section>

      {/* ── Why it matters ── */}
      <Section modifier="why" icon="◆" title="Why It Matters">
        <p className="section__text">{step.why}</p>
      </Section>

      {/* ── Day-one look-fors ── */}
      <Section modifier="dayone" icon="⌖" title="What To Look For On Day One">
        <ul className="dayone-list">
          {step.day_one.map((item, i) => (
            <li key={i} className="dayone-item">
              <span className="dayone-item__text">{item}</span>
            </li>
          ))}
        </ul>
      </Section>

      {/* ── Recommended stack ── */}
      <Section modifier="products" icon="✓" title="Recommended for Your Stack">
        <div className="product-list">
          {step.products.map((product, i) => (
            <ProductCard key={i} product={product} />
          ))}
        </div>
      </Section>

      {/* ── Alternatives ── */}
      <Section modifier="alts" icon="⇄" title="Alternatives & Trade-offs">
        {step.alternatives.length > 0 ? (
          <div className="alt-list">
            {step.alternatives.map((alt, i) => (
              <div key={i} className="alt-item">
                <div className="alt-item__name">{alt.name}</div>
                <div className="alt-item__comparison">{alt.comparison}</div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-alts">
            No direct alternatives — the recommended tooling is the standard approach for this path.
          </p>
        )}
      </Section>

      {/* ── Licensing / operations notes ── */}
      <Section modifier="ops" icon="⚙" title="Licensing & Care-and-Feeding Notes">
        <p className="section__text">{step.ops_notes}</p>
      </Section>

      {/* ── Implementation steps ── */}
      <Section modifier="config" icon="#" title="Implementation Steps">
        <ol className="config-steps">
          {step.config_steps.map((s, i) => (
            <li key={i} className="config-step">
              <span className="config-step__text">{s}</span>
            </li>
          ))}
        </ol>
      </Section>

    </div>
  );
}

// ── Section wrapper subcomponent ─────────────────────────────────

function Section({ modifier, icon, title, children }) {
  return (
    <div className={`section section--${modifier}`}>
      <div className="section__header">
        <div className="section__icon">{icon}</div>
        <div className="section__title">{title}</div>
      </div>
      <div className="section__body">
        {children}
      </div>
    </div>
  );
}

// ── ProductCard subcomponent ─────────────────────────────────────

function ProductCard({ product }) {
  return (
    <div className="product-card">
      <div className="product-card__role">{product.role}</div>
      <div className="product-card__top">
        <div className="product-card__name">{product.name}</div>
        <div className="product-card__price">{product.price}</div>
      </div>
      {product.note && (
        <div className="product-card__note">{product.note}</div>
      )}
    </div>
  );
}
