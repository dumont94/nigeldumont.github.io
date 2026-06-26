/**
 * StepCard.jsx — Renders a single build step with all its sections.
 *
 * Each section is color-coded by purpose so a reader can scan quickly:
 *   Blue   — What is this?  (plain-English explanation)
 *   Amber  — Why you need it (business justification)
 *   Green  — Recommended products (the "buy" section)
 *   Gray   — Alternatives & trade-offs
 *   Red    — Patching / licensing notes (the "don't forget" section)
 *   Purple — Configuration steps (the hands-on part)
 *
 * Sections with no content (e.g. empty alternatives list) render a
 * tasteful "no alternatives listed" note rather than an empty card.
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

      {/* ── Why you need it ── */}
      <Section modifier="why" icon="◆" title="Why You Need It">
        <p className="section__text">{step.why}</p>
      </Section>

      {/* ── Recommended products ── */}
      <Section modifier="products" icon="✓" title="Recommended for Your Build">
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
            No direct alternatives — the recommended product is the standard approach for this path.
          </p>
        )}
      </Section>

      {/* ── Patching / licensing notes ── */}
      <Section modifier="patch" icon="⚠" title="Patching, Licensing & Renewal Notes">
        <p className="section__text">{step.patching_notes}</p>
      </Section>

      {/* ── Configuration steps ── */}
      <Section modifier="config" icon="#" title="Configuration Steps">
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
