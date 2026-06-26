/**
 * ProgressBar.jsx — Step progress indicator for the walkthrough.
 *
 * Shows a thin filled bar and a "Step X of Y" label.
 * The fill animates via CSS transition on width change.
 */

export default function ProgressBar({ current, total }) {
  const percent = Math.round(((current + 1) / total) * 100);

  return (
    <div className="progress-bar">
      <div className="progress-bar__track">
        <div
          className="progress-bar__fill"
          style={{ width: `${percent}%` }}
        />
      </div>
      <span className="progress-bar__label">
        {current + 1} / {total}
      </span>
    </div>
  );
}
