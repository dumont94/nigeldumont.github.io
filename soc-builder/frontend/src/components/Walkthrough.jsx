/**
 * Walkthrough.jsx — Orchestrates the step-by-step build sequence.
 *
 * Layout:
 *   Left sidebar — scrollable step list showing completion state
 *   Right column — StepCard for the current step + prev/next navigation
 *
 * The user can also click any item in the step list to jump directly
 * to that step, which is useful for reviewing a specific section.
 *
 * On the final step, "Next" becomes "Finish — View Summary" which
 * triggers the onComplete callback to transition to the Summary screen.
 */

import StepCard from "./StepCard.jsx";
import ProgressBar from "./ProgressBar.jsx";

export default function Walkthrough({
  recommendation,
  currentStep,
  onStepChange,
  onComplete,
}) {
  const { steps, path_info } = recommendation;
  const step = steps[currentStep];
  const isFirst = currentStep === 0;
  const isLast = currentStep === steps.length - 1;

  function goNext() {
    if (isLast) {
      onComplete();
    } else {
      onStepChange(currentStep + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function goPrev() {
    if (!isFirst) {
      onStepChange(currentStep - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  return (
    <div>
      {/* Progress bar spans full width above the two-column layout */}
      <ProgressBar current={currentStep} total={steps.length} />

      <div className="walkthrough">
        {/* ── Left: step list sidebar ── */}
        <aside className="step-list">
          <div className="step-list__path">{path_info.name}</div>
          {steps.map((s, i) => {
            const isDone   = i < currentStep;
            const isActive = i === currentStep;
            return (
              <div
                key={s.id}
                className={[
                  "step-list__item",
                  isActive ? "step-list__item--active"    : "",
                  isDone   ? "step-list__item--completed" : "",
                ].filter(Boolean).join(" ")}
                onClick={() => {
                  onStepChange(i);
                  window.scrollTo({ top: 0, behavior: "smooth" });
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && onStepChange(i)}
              >
                <span className="step-list__num">
                  {isDone ? "✓" : s.order}
                </span>
                <span className="step-list__name">{s.title}</span>
              </div>
            );
          })}
        </aside>

        {/* ── Right: current step content ── */}
        <div>
          <StepCard step={step} />

          {/* Navigation */}
          <div className="step-nav">
            <button
              className="btn btn--ghost"
              onClick={goPrev}
              disabled={isFirst}
            >
              ← Previous
            </button>

            <span className="step-nav__center">
              {step.title}
            </span>

            <button
              className="btn btn--primary"
              onClick={goNext}
            >
              {isLast ? "View Summary →" : "Next →"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
