/**
 * Summary.jsx — The final summary screen.
 *
 * Shows:
 *   1. Path card — chosen path, tagline, Year 1 and recurring costs
 *   2. Network diagram — the topology for this path
 *   3. Full stack table — every component, its product, and approx. price
 *   4. Pricing disclaimer
 *   5. Sources — vendor links so the user can verify current pricing
 *   6. Actions — start over or go back to a specific step
 */

import NetworkDiagram from "./NetworkDiagram.jsx";

export default function Summary({ recommendation, onReset, onReviewStep }) {
  const { path, path_info, steps, sources } = recommendation;

  return (
    <div className="summary">

      {/* ── 1. Path overview ── */}
      <div className="summary__path-card">
        <div className="summary__path-badge">Your selected build path</div>
        <h1 className="summary__path-name">{path_info.name}</h1>
        <p className="summary__path-tagline">{path_info.tagline}</p>

        <div className="summary__costs">
          <div className="cost-card">
            <div className="cost-card__label">Year 1 Total</div>
            <div className="cost-card__value">{path_info.year1_cost}</div>
          </div>
          <div className="cost-card">
            <div className="cost-card__label">Year 2+ (Recurring)</div>
            <div className="cost-card__value">{path_info.recurring_cost}</div>
          </div>
          <div className="cost-card">
            <div className="cost-card__label">Team Size</div>
            <div className="cost-card__value" style={{ fontSize: "14px", color: "var(--text)" }}>
              {path_info.audience}
            </div>
          </div>
        </div>

        <p className="summary__path-desc">{path_info.description}</p>
      </div>

      {/* ── 2. Network diagram ── */}
      <NetworkDiagram pathId={path} />

      {/* ── 3. Full stack table ── */}
      <div>
        <h2 className="summary__section-title">Full Component Stack</h2>
        <table className="stack-table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Component</th>
              <th>Recommended Product</th>
              <th>Approx. Price</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((step) =>
              step.products.map((product, pIdx) => (
                <tr
                  key={`${step.id}-${pIdx}`}
                  style={{ cursor: "pointer" }}
                  onClick={() => onReviewStep(step.order - 1)}
                  title={`Click to review Step ${step.order}: ${step.title}`}
                >
                  {/* Only show step label on the first product row */}
                  {pIdx === 0 ? (
                    <td
                      className="stack-table__step"
                      rowSpan={step.products.length}
                    >
                      {step.order}. {step.title}
                    </td>
                  ) : null}
                  <td className="stack-table__component">
                    <span style={{ fontSize: "11px", color: "var(--text-dim)", display: "block" }}>
                      {product.role}
                    </span>
                  </td>
                  <td className="stack-table__product">{product.name}</td>
                  <td className="stack-table__price">{product.price}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>

        {/* Hint to click rows */}
        <p style={{ fontSize: "12px", color: "var(--text-dim)", marginTop: "var(--space-3)", fontFamily: "var(--mono)" }}>
          ↑ Click any row to review that step's full details
        </p>
      </div>

      {/* ── 4. Pricing disclaimer ── */}
      <div className="pricing-note">
        <span className="pricing-note__icon">⚠</span>
        <span>
          All pricing is approximate as of 2026. Hardware and licensing costs change frequently —
          always verify current pricing directly with vendors before purchasing.
          Links to all vendor sites are in the Sources section below.
        </span>
      </div>

      {/* ── 5. Sources ── */}
      <div>
        <h2 className="summary__section-title">Sources & Vendor Links</h2>
        <div className="sources-grid">
          {sources.map((source) => (
            <a
              key={source.vendor}
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="source-card"
            >
              <div className="source-card__vendor">{source.vendor}</div>
              <div className="source-card__url">{source.url}</div>
              <div className="source-card__note">{source.note}</div>
            </a>
          ))}
        </div>
      </div>

      {/* ── 6. Actions ── */}
      <div className="summary__actions">
        <button className="btn btn--ghost" onClick={() => onReviewStep(0)}>
          ← Review Build Steps
        </button>
        <button className="btn btn--secondary" onClick={onReset}>
          Start Over
        </button>
      </div>

    </div>
  );
}
