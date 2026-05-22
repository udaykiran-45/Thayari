import { useState } from "react";
import ProfileForm from "./pages/ProfileForm";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [studentId, setStudentId] = useState(null);

  return (
    <>
      <nav className="global-nav">
        <span className="logo">Thaiyari</span>
        <span style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
          — placement engine
        </span>
      </nav>

      {!studentId ? (
        <ProfileForm onSuccess={(id) => setStudentId(id)} />
      ) : (
        <Dashboard
          studentId={studentId}
          onBack={() => setStudentId(null)}
        />
      )}
    </>
  );
}