import { useState, useEffect } from "react";
import Questionnaire from "./components/Questionnaire.jsx";
import Walkthrough from "./components/Walkthrough.jsx";
import Summary from "./components/Summary.jsx";
import { buildRecommendation } from "./recommendations.js";

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
  // SOC apps default to dark — analysts live in dark dashboards
  const [theme, setTheme] = useState(
    () => localStorage.getItem("soc-theme") || "dark"
  );

  useEffect(() => {
    document.body.classList.toggle("light", theme === "light");
    localStorage.setItem("soc-theme", theme);
  }, [theme]);

  function toggleTheme() {
    setTheme((t) => (t === "dark" ? "light" : "dark"));
  }

  function handleSubmit(formData) {
    setScreen(SCREENS.LOADING);
    setError(null);
    try {
      const data = buildRecommendation(formData);
      setRecommendation(data);
      setCurrentStep(0);
      setScreen(SCREENS.WALKTHROUGH);
    } catch (err) {
      setError(err.message);
      setScreen(SCREENS.QUESTIONNAIRE);
    }
  }

  function handleWalkthroughComplete() {
    setScreen(SCREENS.SUMMARY);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function handleReset() {
    setRecommendation(null);
    setCurrentStep(0);
    setError(null);
    setScreen(SCREENS.QUESTIONNAIRE);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const pathLabel = recommendation ? recommendation.path_info.name : null;

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header__logo">
          <div className="app-header__dot" />
          <div>
            <div className="app-header__title">SOC Foundations Builder</div>
            <div className="app-header__sub">by Nigel Dumont</div>
          </div>
        </div>
        <div className="app-header__right">
          {pathLabel && <div className="app-header__badge">{pathLabel}</div>}
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === "dark" ? "☀ light" : "☾ dark"}
          </button>
          <a
            className="app-header__back"
            href="https://dumont94.github.io/nigeldumont.github.io/"
          >
            ← portfolio
          </a>
        </div>
      </header>

      <main className="main">
        {screen === SCREENS.QUESTIONNAIRE && (
          <Questionnaire onSubmit={handleSubmit} error={error} />
        )}

        {screen === SCREENS.LOADING && (
          <div className="loading">
            <div className="loading__spinner" />
            <div className="loading__text">Building your 90-day security plan…</div>
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
