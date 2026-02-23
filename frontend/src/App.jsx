import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8001/api";

function App() {
  const [entries, setEntries] = useState([]);

  async function loadEntries() {
    const res = await fetch(`${API}/entries`);
    const data = await res.json();
    setEntries(data);
  }

  useEffect(() => {
    loadEntries();
  }, []);

  return (
    <div className="container">
      <h1>Personal Dashboard</h1>

      <button onClick={loadEntries}>Reload</button>

      <h2>Entries</h2>

      {entries.map(entry => (
        <div key={entry.id} className="card">
          <p><b>Date:</b> {entry.date}</p>
          <p><b>Sleep:</b> {entry.sleep_hours}</p>
          <p><b>Mood:</b> {entry.mood}</p>
          <p><b>Energy:</b> {entry.energy}</p>
        </div>
      ))}
    </div>
  );
}

export default App;