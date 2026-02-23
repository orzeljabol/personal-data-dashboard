const API = "http://127.0.0.1:8001/api";

const out = document.getElementById("out");
document.getElementById("reload").addEventListener("click", loadEntries);
document.getElementById("history").addEventListener("click",history);
document.getElementById("new_entry").addEventListener("click",newEntry);
document.getElementById("delete_entry").addEventListener("click",deleteEntry);
async function loadEntries() {
    out.textContent = "Loading...";
    try{
        const res = await fetch(`${API}/entries`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        out.textContent = `Error: ` + err.message;
    }

}
async function history() {
    out.textContent = "Loading history...";
    try{
        const res = await fetch(`${API}/entries`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        out.textContent = `Error: ` + err.message;
    }
}
async function newEntry() {
    out.textContent = "Creating new entry...";
    try{
        const res = await fetch(`${API}/entries`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({content: "New entry content"})
        });
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        out.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        out.textContent = `Error: ` + err.message;
    }
