import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function App() {
  const [incidents, setIncidents] = useState([]);
  const [selected, setSelected] = useState(null);
  const [signals, setSignals] = useState([]);
  const [rca, setRca] = useState({
    root_cause: "",
    fix_applied: "",
    prevention: ""
  });

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    const res = await axios.get(`${API}/api/incidents`);
    setIncidents(res.data);
  };

  const openIncident = async (incident) => {
    setSelected(incident);
    const res = await axios.get(`${API}/api/incidents/${incident.id}/signals`);
    setSignals(res.data);
  };

  const updateStatus = async (status) => {
    if (!selected) return;

    try {
      const res = await axios.patch(
        `${API}/api/incidents/${selected.id}/status`,
        { status }
      );

      alert(res.data.message);

      const updatedIncident = { ...selected, status };
      setSelected(updatedIncident);

      fetchIncidents();
    } catch (err) {
      alert(err.response?.data?.detail || "Error updating status");
    }
  };

  const submitRca = async () => {
    if (!selected) return;

    if (!rca.root_cause || !rca.fix_applied || !rca.prevention) {
      alert("Please fill all RCA fields");
      return;
    }

    try {
      const res = await axios.post(
        `${API}/api/incidents/${selected.id}/rca`,
        rca
      );

      alert(`RCA submitted. MTTR: ${Math.round(res.data.mttr_seconds)} seconds`);

      setRca({
        root_cause: "",
        fix_applied: "",
        prevention: ""
      });

      fetchIncidents();
    } catch (err) {
      alert(err.response?.data?.detail || "Error submitting RCA");
    }
  };

  const severityStyle = (severity) => {
    if (severity === "P0") return { background: "#dc2626", color: "white" };
    if (severity === "P1") return { background: "#f97316", color: "white" };
    if (severity === "P2") return { background: "#eab308", color: "black" };
    return { background: "#64748b", color: "white" };
  };

  const statusStyle = (status) => {
    if (status === "OPEN") return { background: "#dc2626", color: "white" };
    if (status === "INVESTIGATING") return { background: "#2563eb", color: "white" };
    if (status === "RESOLVED") return { background: "#16a34a", color: "white" };
    if (status === "CLOSED") return { background: "#475569", color: "white" };
    return { background: "#64748b", color: "white" };
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "#e5e7eb",
        padding: "30px",
        fontFamily: "Arial"
      }}
    >
      <h1 style={{ textAlign: "center", fontSize: "42px" }}>
        🚨 Incident Dashboard
      </h1>

      <div
        style={{
          marginTop: "25px",
          background: "#111827",
          padding: "20px",
          borderRadius: "12px",
          border: "1px solid #334155"
        }}
      >
        <table
          cellPadding="12"
          style={{
            width: "100%",
            borderCollapse: "collapse"
          }}
        >
          <thead>
            <tr style={{ background: "#1e293b" }}>
              <th>ID</th>
              <th>Component</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Title</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {incidents.map((inc) => (
              <tr
                key={inc.id}
                style={{
                  borderBottom: "1px solid #334155",
                  textAlign: "center"
                }}
              >
                <td>{inc.id}</td>
                <td>{inc.component_id}</td>
                <td>{inc.component_type}</td>

                <td>
                  <span style={{ padding: "6px 12px", borderRadius: "20px", ...severityStyle(inc.severity) }}>
                    {inc.severity}
                  </span>
                </td>

                <td>
                  <span style={{ padding: "6px 12px", borderRadius: "20px", ...statusStyle(inc.status) }}>
                    {inc.status}
                  </span>
                </td>

                <td>{inc.title}</td>

                <td>
                  <button onClick={() => openIncident(inc)} style={viewButtonStyle}>
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <div
          style={{
            marginTop: "30px",
            background: "#111827",
            border: "1px solid #334155",
            borderRadius: "12px",
            padding: "24px"
          }}
        >
          <h2>Incident Details</h2>

          <p><b>ID:</b> {selected.id}</p>
          <p><b>Component:</b> {selected.component_id}</p>
          <p><b>Severity:</b> {selected.severity}</p>
          <p>
            <b>Status:</b>{" "}
            <span style={{ padding: "6px 12px", borderRadius: "20px", ...statusStyle(selected.status) }}>
              {selected.status}
            </span>
          </p>
          <p><b>Title:</b> {selected.title}</p>

          <h3>Status Actions</h3>

          <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
            {selected.status === "OPEN" && (
              <button
                onClick={() => updateStatus("INVESTIGATING")}
                style={{ ...actionButtonStyle, background: "#2563eb" }}
              >
                Start Investigation
              </button>
            )}

            {selected.status === "INVESTIGATING" && (
              <button
                onClick={() => updateStatus("RESOLVED")}
                style={{ ...actionButtonStyle, background: "#16a34a" }}
              >
                Mark Resolved
              </button>
            )}

            {selected.status === "RESOLVED" && (
              <button
                onClick={() => updateStatus("CLOSED")}
                style={{ ...actionButtonStyle, background: "#dc2626" }}
              >
                Close Incident
              </button>
            )}

            <button
              onClick={() => {
                setSelected(null);
                setSignals([]);
              }}
              style={{ ...actionButtonStyle, background: "#64748b" }}
            >
              Close Detail Panel
            </button>
          </div>

          <h3>Raw Signals</h3>

          {signals.length === 0 ? (
            <p>No signals found.</p>
          ) : (
            <pre
              style={{
                background: "#020617",
                color: "#22c55e",
                padding: "16px",
                borderRadius: "10px",
                overflowX: "auto"
              }}
            >
              {JSON.stringify(signals, null, 2)}
            </pre>
          )}

          {selected.status !== "CLOSED" && (
            <>
              <h3>Submit RCA</h3>

              <input
                placeholder="Root Cause"
                value={rca.root_cause}
                onChange={(e) => setRca({ ...rca, root_cause: e.target.value })}
                style={inputStyle}
              />

              <textarea
                placeholder="Fix Applied"
                value={rca.fix_applied}
                onChange={(e) => setRca({ ...rca, fix_applied: e.target.value })}
                style={inputStyle}
              />

              <textarea
                placeholder="Prevention Steps"
                value={rca.prevention}
                onChange={(e) => setRca({ ...rca, prevention: e.target.value })}
                style={inputStyle}
              />

              <button
                onClick={submitRca}
                style={{
                  padding: "10px 18px",
                  borderRadius: "8px",
                  border: "none",
                  cursor: "pointer",
                  background: "#22c55e",
                  color: "white",
                  fontWeight: "bold"
                }}
              >
                Submit RCA
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  marginBottom: "12px",
  padding: "10px",
  borderRadius: "8px",
  border: "1px solid #475569",
  background: "#020617",
  color: "#e5e7eb"
};

const viewButtonStyle = {
  padding: "8px 14px",
  borderRadius: "8px",
  border: "none",
  cursor: "pointer",
  background: "#38bdf8",
  color: "#0f172a",
  fontWeight: "bold"
};

const actionButtonStyle = {
  padding: "10px 16px",
  borderRadius: "8px",
  border: "none",
  cursor: "pointer",
  color: "white",
  fontWeight: "bold"
};

export default App;