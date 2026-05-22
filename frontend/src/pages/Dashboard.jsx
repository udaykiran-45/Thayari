import { useEffect, useState } from "react";
import ProfileSummary from "../components/SkillTagInput";
import JobCard from "../components/JobCard";

const API = "http://localhost:8000";

export default function Dashboard({ studentId, onBack }) {
  const [student, setStudent] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [sRes, mRes] = await Promise.all([
          fetch(`${API}/api/students/${studentId}`),
          fetch(`${API}/api/match/${studentId}`),
        ]);
        if (!sRes.ok) throw new Error("Failed to load profile");
        if (!mRes.ok) throw new Error("Failed to load matches");
        setStudent(await sRes.json());
        setMatches(await mRes.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [studentId]);

  if (loading) return (
    <div className="dashboard" style={{ textAlign: "center", paddingTop: "4rem" }}>
      <p style={{ color: "var(--muted)" }}>Loading your matches...</p>
    </div>
  );

  if (error) return (
    <div className="dashboard">
      <div className="alert alert-error">{error}</div>
      <button className="btn btn-primary" style={{ width: "auto" }} onClick={onBack}>← Go Back</button>
    </div>
  );

  return (
    <div className="dashboard">
      <button onClick={onBack}
        style={{ background: "none", border: "1px solid var(--border)", color: "var(--muted)", borderRadius: "8px", padding: "0.4rem 1rem", cursor: "pointer", marginBottom: "1.5rem", fontFamily: "inherit", fontSize: "0.85rem" }}>
        ← New Profile
      </button>

      {student && <ProfileSummary student={student} />}

      <p className="section-title">{matches.length} Job Matches</p>

      {matches.map((m) => <JobCard key={m.job.id} match={m} />)}
    </div>
  );
}