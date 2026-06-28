import { useEffect, useState } from "react";
import "./App.css";
import { FaBed, FaBolt, FaSmile, FaDumbbell, FaTint, FaBrain } from "react-icons/fa";
import { IoHourglass } from "react-icons/io5";


const API = "http://127.0.0.1:8001/api";
function toNumberOrNull(value) {
  return value === "" ? null : Number(value);
}
function App() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [editing, setEditing] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const friendly = {
  mood: "Mood must be between 1 and 10",
  energy: "Energy must be between 1 and 10",
  sleep_hours: "Sleep hours must be valid",
  deep_work_minutes: "Deep work minutes must be valid",
  exercise_minutes: "Exercise minutes must be valid",
  stimulation_minutes: "Stimulation minutes must be valid",
  litres_water: "Litres of water must be valid",
};
function formatNumbers(value){
  return value !== null && value !== undefined ? Number(value).toFixed(2) : "-";
}
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

  setError("");
  setFieldErrors((prev) => ({
    ...prev,
    [e.target.name]: undefined
  }));
  }
  async function loadEntries() {
    try {
      setLoading(true);
      setError("");
      const res = await fetch(`${API}/entries`);
      if (!res.ok) {
        throw new Error("Failed to load entries");
      }
      const data = await res.json();
      setEntries(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }
  async function createEntry() {
    if (Number(form.mood) < 1 || Number(form.mood) > 10) {
      setError("Mood must be between 1 and 10");
      return;
    }

    if (Number(form.energy) < 1 || Number(form.energy) > 10) {
      setError("Energy must be between 1 and 10");
      return;
    }
    const res = await fetch(`${API}/entries/`, {
      method: "POST",
      headers: {"Content-Type": "application/json",
      },
      body: JSON.stringify({
      date: form.date,
      sleep_hours: toNumberOrNull(form.sleep_hours),
      mood: toNumberOrNull(form.mood),
      energy: toNumberOrNull(form.energy),
      deep_work_minutes: toNumberOrNull(form.deep_work_minutes),
      exercise_minutes: toNumberOrNull(form.exercise_minutes),
      stimulation_minutes: toNumberOrNull(form.stimulation_minutes),
      litres_water: toNumberOrNull(form.litres_water),
      notes: form.notes || null,
      no_porn: form.no_porn,
      no_smoking: form.no_smoking,
      no_alcohol: form.no_alcohol,
      })

    
    });
    
    if (!res.ok) {
  const data = await res.json().catch(() => null);

  if (data?.detail && Array.isArray(data.detail)) {
    const errors = {};
    const messages = [];

    data.detail.forEach((err) => {
      const field = err.loc?.[1];
      if (field) {
        errors[field] = err.msg;
        messages.push(friendly[field] || err.msg);
      }
    });

    setFieldErrors(errors);
    setError(messages.join(" | "));
  } 
  else {
    let message = "Could not create entry.";

    if (res.status === 422) {
      message = "Some fields contain invalid values.";
    }
    else if (res.status === 400) {
    message = "Entry for this date already exists.";
    }
    else if (res.status === 500) {
    message = "Server error. Please try again later.";
    }

    setError(message);
    setFieldErrors({});
  }

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
    setError("");
    setFieldErrors({});
    setShowForm(false);
    loadEntries();
  }
  function startEdit(entry) {
    setEditing(entry);
    setEditForm({
      sleep_hours: entry.sleep_hours ?? "",
      mood: entry.mood ?? "",
      energy: entry.energy ?? "",
      deep_work_minutes: entry.deep_work_minutes ?? "",
      exercise_minutes: entry.exercise_minutes ?? "",
      stimulation_minutes: entry.stimulation_minutes ?? "",
      litres_water: entry.litres_water ?? "",
      notes: entry.notes ?? "",
      no_porn: !!entry.no_porn,
      no_smoking: !!entry.no_smoking,
      no_alcohol: !!entry.no_alcohol,
    });
  }
  
  async function saveEdit() {
  if (!editing) return;

  const payload = {};
  const numFields = new Set([
    "sleep_hours",
    "mood",
    "energy",
    "deep_work_minutes",
    "exercise_minutes",
    "stimulation_minutes",
    "litres_water",
  ]);

  for (const [k, v] of Object.entries(editForm)) {
    if (v === "") continue;

    let value = v;
    if (numFields.has(k)) {
      value = Number(v);
    }

    const original = editing[k] ?? "";
    if (value !== original) {
      payload[k] = value;
    }
  }

  if (Object.keys(payload).length === 0) {
    setError("No changes to save.");
    return;
  }

  const res = await fetch(`${API}/entries/${editing.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => null);

    if (data?.detail && Array.isArray(data.detail)) {
      const errors = {};
      const messages = [];

      data.detail.forEach((err) => {
        const field = err.loc?.[1];
        if (field) {
          errors[field] = err.msg;
          messages.push(friendly[field] || err.msg);
        }
      });

      setFieldErrors(errors);
      setError(messages.join(" | "));
    } else {
      let message = "Could not update entry.";
      if (res.status === 422) {
        message = "Some fields contain invalid values.";
      } else if (res.status === 400) {
        message = "Entry for this date already exists.";
      } else if (res.status === 500) {
        message = "Server error. Please try again later.";
      }

      setError(message);
      setFieldErrors({});
    }

    return;
  }

  const updated = await res.json();
  setEntries((prev) => prev.map((e) => (e.id === updated.id ? updated : e)));
  setEditing(null);
  setError("");
  setFieldErrors({});
}


async function deleteEntry(entryId) {
  const res = await fetch(`${API}/entries/${entryId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
      let message = "Could not delete entry.";
      if (res.status === 404) {
        message = "Entry not found.";
      }
      else if (res.status === 500) {
        message = "Server error. Please try again later.";
      }
      setError(message);
      setFieldErrors({});
  

      return;
  }
  setEntries((prev) => prev.filter(e => e.id !== entryId));
}
async function showSummary() {
  const res = await fetch(`${API}/entries/summary/7days`);
  const data = await res.json();
  if (!res.ok) {
    let message = "Could not load summary.";
    if (res.status === 404) {
      message = "No entries found for the last 7 days.";
    }
    else if (res.status === 500) {
      message = "Server error. Please try again later.";
    }

    setError(message);
    return;
  }
  setSummary(data ? [data] : []);
}
  useEffect(() => {
    loadEntries();
  }, []);

  return (
    <div className="container">
      <h1>Personal Dashboard</h1>
      <button onClick={() => setShowForm(prev => !prev)}>{showForm ? "Close":"New"}</button>
      <button onClick={showSummary}>Statistics</button>
      <button onClick={loadEntries}>Reload</button>
      {error && <div className="error-box">{error}</div>}
      {loading && <p>Loading entries...</p>}
      {!loading && entries.length === 0 && (
        <p>No entries yet. Create your first daily entry.</p>
      )}
      {summary && (
        summary.map((item,index) => (
          <div key={index} className="summary-card">
            <p><FaSmile /> <b>Avg Mood:</b> {formatNumbers(item.average_mood)}</p>
            <p><FaBolt /> <b>Avg Energy:</b> {formatNumbers(item.average_energy)}</p>
            <p><FaBed /> <b>Avg Sleep [h]:</b> {formatNumbers(item.average_sleep_hours)}</p>
            <p><FaTint /> <b>Avg Water [l]:</b> {formatNumbers(item.average_litres_water)}</p>
            <p><FaBrain /> <b>Total Deep Work [min]:</b> {Math.round(formatNumbers(item.total_deep_work_minutes))}</p>
            <p><FaDumbbell /> <b>Total Exercise [min]:</b> {Math.round(formatNumbers(item.total_exercise_minutes))}</p>
            <p><IoHourglass /><b>Total Stimulation [min]:</b> {Math.round(formatNumbers(item.total_stimulation_minutes))}</p>
          </div>
        ))
      )} 
      {showForm && (<div className="entry-form">
      <h2>New Entry</h2>
      <div className="row">
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
        />
        {fieldErrors.date && <p className="field-error">{fieldErrors.date}</p>}
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
        {fieldErrors.sleep_hours && <p className="field-error">{fieldErrors.sleep_hours}</p>}
        <input
          type="number"
          name="mood"
          placeholder="Mood (1-10)"
          min="1"
          max="10"
          value={form.mood}
          onChange={handleChange}
        />
        {fieldErrors.mood && <p className="field-error">{fieldErrors.mood}</p>}
        <input
          type="number"
          name="energy"
          placeholder="Energy (1-10)"
          min="1"
          max="10"
          value={form.energy}
          onChange={handleChange}
        />
        {fieldErrors.energy && <p className="field-error">{fieldErrors.energy}</p>}
        </div>
        <div className="row">
        <input
          type="number"
          name="deep_work_minutes"
          placeholder="Deep work minutes"
          value={form.deep_work_minutes}
          onChange={handleChange}
        />
        {fieldErrors.deep_work_minutes && <p className="field-error">{fieldErrors.deep_work_minutes}</p>}
        <input
          type="number"
          name="exercise_minutes"
          placeholder="Exercise minutes"
          value={form.exercise_minutes}
          onChange={handleChange}
        />
        {fieldErrors.exercise_minutes && <p className="field-error">{fieldErrors.exercise_minutes}</p>}
        <input
          type="number"
          name="stimulation_minutes"
          placeholder="Stimulation minutes"
          value={form.stimulation_minutes}
          onChange={handleChange}
        />
        {fieldErrors.stimulation_minutes && <p className="field-error">{fieldErrors.stimulation_minutes}</p>}
        <input
          type="number"
          name="litres_water"
          placeholder="Litres of water"
          value={form.litres_water}
          onChange={handleChange}
        />
        {fieldErrors.litres_water && <p className="field-error">{fieldErrors.litres_water}</p>}
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
      {editing && (
  <div className="edit-form">
    <h2>Edit entry: {editing.date}</h2>

    <div className="form-grid">
      <div className="field">
        <label>Sleep [h]</label>
        <input
          type="number"
          value={editForm.sleep_hours}
          onChange={(e) => setEditForm({ ...editForm, sleep_hours: e.target.value })}
          placeholder="Sleep hours"
        />
      </div>

      <div className="field">
        <label>Mood (1-10)</label>
        <input
          type="number"
          value={editForm.mood}
          onChange={(e) => setEditForm({ ...editForm, mood: e.target.value })}
          placeholder="Mood"
        />
      </div>

      <div className="field">
        <label>Energy (1-10)</label>
        <input
          type="number"
          value={editForm.energy}
          onChange={(e) => setEditForm({ ...editForm, energy: e.target.value })}
          placeholder="Energy"
        />
      </div>

      <div className="field">
        <label>Deep work [min]</label>
        <input
          type="number"
          value={editForm.deep_work_minutes}
          onChange={(e) => setEditForm({ ...editForm, deep_work_minutes: e.target.value })}
          placeholder="Deep work minutes"
        />
      </div>

      <div className="field">
        <label>Exercise [min]</label>
        <input
          type="number"
          value={editForm.exercise_minutes}
          onChange={(e) => setEditForm({ ...editForm, exercise_minutes: e.target.value })}
          placeholder="Exercise minutes"
        />
      </div>

      <div className="field">
        <label>Stimulation [min]</label>
        <input
          type="number"
          value={editForm.stimulation_minutes}
          onChange={(e) => setEditForm({ ...editForm, stimulation_minutes: e.target.value })}
          placeholder="Stimulation minutes"
        />
      </div>

      <div className="field">
        <label>Water [l]</label>
        <input
          type="number"
          value={editForm.litres_water}
          onChange={(e) => setEditForm({ ...editForm, litres_water: e.target.value })}
          placeholder="Litres of water"
        />
      </div>

      <div className="field field-full">
        <label>Notes</label>
        <textarea
          value={editForm.notes}
          onChange={(e) => setEditForm({ ...editForm, notes: e.target.value })}
          placeholder="Notes"
        />
      </div>
    </div>

    <div className="checkbox-row">
      <label>
        <input
          type="checkbox"
          checked={editForm.no_porn}
          onChange={(e) => setEditForm({ ...editForm, no_porn: e.target.checked })}
        />
        No porn
      </label>

      <label>
        <input
          type="checkbox"
          checked={editForm.no_smoking}
          onChange={(e) => setEditForm({ ...editForm, no_smoking: e.target.checked })}
        />
        No smoking
      </label>

      <label>
        <input
          type="checkbox"
          checked={editForm.no_alcohol}
          onChange={(e) => setEditForm({ ...editForm, no_alcohol: e.target.checked })}
        />
        No alcohol
      </label>
    </div>

    <div className="action-row">
      <button onClick={saveEdit}>Save</button>
      <button onClick={() => setEditing(null)}>Cancel</button>
    </div>
  </div>
)}

      {!loading && entries.map(entry => (
        <div key={entry.id} className="card">
          <div style={{display: "flex", gap: 8 }}>
            <button onClick={() => startEdit(entry)}>Edit</button>
            <button onClick={() => deleteEntry(entry.id)}>Delete</button>
          </div>
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