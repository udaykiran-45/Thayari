export default function ProfileSummary({ student }) {
  return (
    <div className="profile-card">
      <div>
        <h2>{student.name}</h2>
        <div className="college">{student.college} · {student.branch}</div>
        <div className="meta-chips">
          <span className="chip chip-purple">Class of {student.graduation_year}</span>
          {student.skills.map((s) => (
            <span className="chip chip-purple" key={s}>{s}</span>
          ))}
        </div>
        {student.about_me && (
          <p style={{ color: "var(--muted)", fontSize: "0.88rem" }}>{student.about_me}</p>
        )}
      </div>
      <div className="cgpa-badge">
        <span className="val">{student.cgpa}</span>
        <span className="lbl">CGPA</span>
      </div>
    </div>
  );
}