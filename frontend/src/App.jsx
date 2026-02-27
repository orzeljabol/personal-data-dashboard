import { useEffect, useState } from "react";
import "./App.css";



const API = "http://127.0.0.1:8001/api";

function App() {
  const [entries, setEntries] = useState([]);
  const [form, setForm] = useState({
    date: new Date().toISOString().slice(0, 10),
    sleep_hours: "",
    mood: "",
    energy: "",
    deep_work_minutes: "",
    exercise_minutes: "",
    stimulation_minutes: "",
    litres_water: "",
    notes: "",
    no_porn: false,
    no_smoking: false,
    no_alcohol: false,
  });
  const [showForm, setShowForm] = useState(false);
  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }
  async function loadEntries() {
    const res = await fetch(`${API}/entries`);
    const data = await res.json();
    setEntries(data);
  }
  async function createEntry() {
    const res = await fetch(`${API}/entries/`, {
      method: "POST",
      headers: {"Content-Type": "application/json",
      },
      body: JSON.stringify({
        date: form.date,
        sleep_hours: Number(form.sleep_hours),
        mood: Number(form.mood),
        energy: Number(form.energy),
        deep_work_minutes: Number(form.deep_work_minutes),
        exercise_minutes: Number(form.exercise_minutes),
        stimulation_minutes: Number(form.stimulation_minutes),
        litres_water: Number(form.litres_water),
        notes: form.notes,
        no_porn: form.no_porn,
        no_smoking: form.no_smoking,
        no_alcohol: form.no_alcohol,
      })
    });
    
    if (!res.ok) {
      const text = await res.text();
      alert(`Error: ${res.status}: ${text}`);
      return;
    }
    setForm({
      date: new Date().toISOString().slice(0, 10),
      sleep_hours: "",
      mood: "",
      energy: "",
      deep_work_minutes: "",
      exercise_minutes: "",
      stimulation_minutes: "",
      litres_water: "",
      notes: "",
      no_porn: false,
      no_smoking: false,
      no_alcohol: false,
    });
    loadEntries();
  }

  return (
    <div className="container">
      <h1>Personal Dashboard</h1>

      <button onClick={() => setShowForm(prev => !prev)}>{showForm ? "Close":"New"}</button>
      <button onClick={function(){}}>Edit</button>
      <button onClick={function(){}}>Delete</button>
      <button onClick={function(){}}>Statsistics</button>
      <button onClick={loadEntries}>History</button>
      <button onClick={function(){}}>Log out</button>
      {showForm && (<div className="entry-form">
      <h2>New Entry</h2>
      <div className="row">
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
        />
        <input
          type="number"
          name="sleep_hours"
          min="0"
          max="24"
          step="0.5"
          placeholder="Sleep hours"
          value={form.sleep_hours}
          onChange={handleChange}
        />
        <input
          type="number"
          name="mood"
          placeholder="Mood (1-10)"
          min="1"
          max="10"
          value={form.mood}
          onChange={handleChange}
        />
        <input
          type="number"
          name="energy"
          placeholder="Energy (1-10)"
          min="1"
          max="10"
          value={form.energy}
          onChange={handleChange}
        />
        </div>
        <div className="row">
        <input
          type="number"
          name="deep_work_minutes"
          placeholder="Deep work minutes"
          value={form.deep_work_minutes}
          onChange={handleChange}
        />
        <input
          type="number"
          name="exercise_minutes"
          placeholder="Exercise minutes"
          value={form.exercise_minutes}
          onChange={handleChange}
        />
        <input
          type="number"
          name="stimulation_minutes"
          placeholder="Stimulation minutes"
          value={form.stimulation_minutes}
          onChange={handleChange}
        />
        <input
          type="number"
          name="litres_water"
          placeholder="Litres of water"
          value={form.litres_water}
          onChange={handleChange}
        />
        </div>

        <textarea
          name="notes"
          placeholder="Notes"
          value={form.notes}
          onChange={handleChange}
        />
        <div className="row_checkbox">
        <label>
          <input
            type="checkbox"
            name="no_porn"
            checked={form.no_porn}
            onChange={(e) => setForm({...form, no_porn: e.target.checked})}
          />
          No porn
        </label>
        <label>
          <input
            type="checkbox"
            name="no_smoking"
            checked={form.no_smoking}
            onChange={(e) => setForm({...form, no_smoking: e.target.checked})}
          />
          No smoking
        </label>
        <label>
          <input
            type="checkbox"
            name="no_alcohol"
            checked={form.no_alcohol}
            onChange={(e) => setForm({...form, no_alcohol: e.target.checked})}
          />
          No alcohol
        </label>
        </div>
        <button onClick={createEntry}>Save</button>
      </div>
      )}
      

      {entries.map(entry => (
        <div key={entry.id} className="card">
          <p><b>Date:</b> {entry.date}</p>
          <p><b>Sleep:</b> {entry.sleep_hours}</p>
          <p><b>Mood:</b> {entry.mood}</p>
          <p><b>Energy:</b> {entry.energy}</p>
          <p><b>Deep Work:</b> {entry.deep_work_minutes} minutes</p>
          <p><b>Exercise:</b> {entry.exercise_minutes} minutes</p>
          <p><b>Stimulation:</b> {entry.stimulation_minutes} minutes</p>
          <p><b>Water:</b> {entry.litres_water} litres</p>
          <p><b>Notes:</b> {entry.notes}</p>
          <p><b>No Porn:</b> {entry.no_porn ? "Yes" : "No"}</p>
          <p><b>No Smoking:</b> {entry.no_smoking ? "Yes" : "No"}</p>
          <p><b>No Alcohol:</b> {entry.no_alcohol ? "Yes" : "No"}</p>
        </div>
      ))}
    </div>
  );
}

export default App;