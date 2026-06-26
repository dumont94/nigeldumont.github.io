/**
 * App.jsx — Root component and application state machine.
 *
 * Screen flow:
 *   questionnaire → (API call) → loading → walkthrough → summary
 *
 * All network data lives in the Flask backend; the frontend is purely
 * presentational. State is kept in this component and passed as props
 * to avoid prop-drilling through a complex tree.
 */

import { useState } from "react";
import Questionnaire from "./components/Questionnaire.jsx";
import Walkthrough from "./components/Walkthrough.jsx";
import Summary from "./components/Summary.jsx";

// Application screens — acts as a lightweight state machine
const SCREENS = {
  QUESTIONNAIRE: "questionnaire",
  LOADING: "loading",
  WALKTHROUGH: "walkthrough",
  SUMMARY: "summary",
};

export default function App() {
  const [screen, setScreen] = useState(SCREENS.QUESTIONNAIRE);
  const [recommendation, setRecommendation] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);

  // Called by Questionnaire when the user submits answers
  async function handleSubmit(formData) {
    setScreen(SCREENS.LOADING);
    setError(null);

    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || `Server error ${res.status}`);
      }

      const data = await res.json();
      setRecommendation(data);
      setCurrentStep(0);
      setScreen(SCREENS.WALKTHROUGH);
    } catch (err) {
      setError(err.message);
      setScreen(SCREENS.QUESTIONNAIRE);
    }
  }

  // Called by Walkthrough when the user reaches the last step and clicks "Finish"
  function handleWalkthroughComplete() {
    setScreen(SCREENS.SUMMARY);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Reset everything — let the user start over
  function handleReset() {
    setRecommendation(null);
    setCurrentStep(0);
    setError(null);
    setScreen(SCREENS.QUESTIONNAIRE);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Derive a short path label for the header badge
  const pathLabel = recommendation
    ? recommendation.path_info.name
    : null;

  return (
    <div className="app">
      {/* ── Fixed header ── */}
      <header className="app-header">
        <div className="app-header__logo">
          <div className="app-header__dot" />
          <div>
            <div className="app-header__title">Your First Network</div>
            <div className="app-header__sub">SOHO Infrastructure Builder</div>
          </div>
        </div>
        {pathLabel && (
          <div className="app-header__badge">{pathLabel}</div>
        )}
      </header>

      {/* ── Main content ── */}
      <main className="main">
        {screen === SCREENS.QUESTIONNAIRE && (
          <Questionnaire onSubmit={handleSubmit} error={error} />
        )}

        {screen === SCREENS.LOADING && (
          <div className="loading">
            <div className="loading__spinner" />
            <div className="loading__text">Building your network plan…</div>
          </div>
        )}

        {screen === SCREENS.WALKTHROUGH && recommendation && (
          <Walkthrough
            recommendation={recommendation}
            currentStep={currentStep}
            onStepChange={setCurrentStep}
            onComplete={handleWalkthroughComplete}
          />
        )}

        {screen === SCREENS.SUMMARY && recommendation && (
          <Summary
            recommendation={recommendation}
            onReset={handleReset}
            onReviewStep={(idx) => {
              setCurrentStep(idx);
              setScreen(SCREENS.WALKTHROUGH);
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
          />
        )}
      </main>
    </div>
  );
}
