const SKILL_RESOURCES = {
  python: "https://docs.python.org/3/tutorial/",
  react: "https://react.dev/learn",
  sql: "https://www.w3schools.com/sql/",
  javascript: "https://javascript.info/",
  docker: "https://docs.docker.com/get-started/",
  "machine learning": "https://www.coursera.org/learn/machine-learning",
  "data structures": "https://www.geeksforgeeks.org/data-structures/",
  algorithms: "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
  nodejs: "https://nodejs.org/en/learn",
  mongodb: "https://learn.mongodb.com/",
  numpy: "https://numpy.org/learn/",
  pandas: "https://pandas.pydata.org/docs/getting_started/",
  statistics: "https://www.khanacademy.org/math/statistics-probability",
};

export default function JobCard({ match }) {
  const { job, score, matched_skills, missing_skills, why } = match;
  const pct = Math.round(score);

  const scoreColor =
    pct >= 75 ? "var(--green)" : pct >= 50 ? "var(--accent)" : "var(--accent2)";

  return (
    <div className="job-card">
      <div className="job-header">
        <div>
          <div className="job-title">{job.title}</div>
          <div className="job-company">{job.company}</div>
        </div>
        <div className="score-ring">
          <span className="score-val" style={{ color: scoreColor }}>{pct}</span>
          <span className="score-lbl">score</span>
        </div>
      </div>

      <div className="why-box">{why}</div>

      <div className="meta-chips">
        {matched_skills.map((s) => (
          <span className="chip chip-green" key={s}>✓ {s}</span>
        ))}
        {missing_skills.map((s) => (
          <span className="chip chip-red" key={s}>✗ {s}</span>
        ))}
      </div>

      {missing_skills.length > 0 && (
        <div className="skill-gap">
          <h4>What to learn next</h4>
          <div className="meta-chips">
            {missing_skills.map((s) => (
              SKILL_RESOURCES[s] ? (
                <a className="learn-link" href={SKILL_RESOURCES[s]} target="_blank" rel="noreferrer" key={s}>
                  📚 {s}
                </a>
              ) : (
                <span className="chip chip-red" key={s}>{s}</span>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
}