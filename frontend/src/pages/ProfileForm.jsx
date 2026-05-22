import { useState } from "react";

const API = "http://localhost:8000";

const SKILL_SUGGESTIONS = [
  "python", "javascript", "react", "nodejs", "sql", "java",
  "c++", "machine learning", "docker", "mongodb", "rest api",
  "html", "css", "numpy", "pandas", "data structures", "algorithms",
];

export default function ProfileForm({ onSuccess }) {
  const [form, setForm] = useState({
    name: "", college: "", branch: "", cgpa: "", graduation_year: "", about_me: "",
  });
  const [skills, setSkills] = useState([]);
  const [skillInput, setSkillInput] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState("");

  const addSkill = (skill) => {
    const s = skill.trim().toLowerCase();
    if (s && !skills.includes(s)) setSkills((prev) => [...prev, s]);
    setSkillInput("");
  };

  const removeSkill = (s) => setSkills((prev) => prev.filter((x) => x !== s));

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = "Name is required";
    if (!form.college.trim()) e.college = "College is required";
    if (!form.branch.trim()) e.branch = "Branch is required";
    const cgpa = parseFloat(form.cgpa);
    if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) e.cgpa = "CGPA must be between 0 and 10";
    const yr = parseInt(form.graduation_year);
    if (isNaN(yr) || yr < 2000 || yr > 2035) e.graduation_year = "Enter a valid year";
    if (skills.length === 0) e.skills = "Add at least one skill";
    return e;
  };

  const handleSubmit = async () => {
    const e = validate();
    setErrors(e);
    if (Object.keys(e).length > 0) return;

    setLoading(true);
    setServerError("");
    try {
      const res = await fetch(`${API}/api/students`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, cgpa: parseFloat(form.cgpa), graduation_year: parseInt(form.graduation_year), skills }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");
      onSuccess(data.id);
    } catch (err) {
      setServerError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-card">
      <h1>Build Your Profile</h1>
      <p className="subtitle">Let's find the best jobs for you.</p>

      {serverError && <div className="alert alert-error">{serverError}</div>}

      {[
        { key: "name", label: "Full Name", type: "text", placeholder: "Ananya Sharma" },
        { key: "college", label: "College", type: "text", placeholder: "IIT Bombay" },
        { key: "branch", label: "Branch", type: "text", placeholder: "Computer Science" },
        { key: "cgpa", label: "CGPA (0–10)", type: "number", placeholder: "8.5" },
        { key: "graduation_year", label: "Graduation Year", type: "number", placeholder: "2025" },
      ].map(({ key, label, type, placeholder }) => (
        <div className="field" key={key}>
          <label>{label}</label>
          <input
            type={type}
            placeholder={placeholder}
            value={form[key]}
            onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
          />
          {errors[key] && <div className="error-msg">{errors[key]}</div>}
        </div>
      ))}

      <div className="field">
        <label>Skills — press Enter or comma to add</label>
        <div className="skills-input-wrap" onClick={() => document.getElementById("skill-input").focus()}>
          {skills.map((s) => (
            <span className="skill-tag" key={s}>
              {s}
              <button onClick={() => removeSkill(s)}>×</button>
            </span>
          ))}
          <input
            id="skill-input"
            value={skillInput}
            placeholder={skills.length === 0 ? "e.g. python, react..." : ""}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === ",") { e.preventDefault(); addSkill(skillInput); }
              if (e.key === "Backspace" && !skillInput) setSkills((p) => p.slice(0, -1));
            }}
          />
        </div>
        <div style={{ marginTop: "0.5rem", display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
          {SKILL_SUGGESTIONS.filter((s) => !skills.includes(s)).slice(0, 8).map((s) => (
            <span key={s} onClick={() => addSkill(s)}
              style={{ fontSize: "0.75rem", color: "var(--muted)", cursor: "pointer", padding: "0.15rem 0.5rem", border: "1px solid var(--border)", borderRadius: "6px" }}>
              + {s}
            </span>
          ))}
        </div>
        {errors.skills && <div className="error-msg">{errors.skills}</div>}
      </div>

      <div className="field">
        <label>About Me (optional)</label>
        <textarea rows={3} placeholder="A passionate developer who loves building things..." value={form.about_me}
          onChange={(e) => setForm((f) => ({ ...f, about_me: e.target.value }))} />
      </div>

      <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
        {loading ? "Saving..." : "Find My Matches →"}
      </button>
    </div>
  );
}