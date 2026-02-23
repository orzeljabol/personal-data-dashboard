const API = "http://127.0.0.1:8001/api";

const out = document.getElementById("out");
document.getElementById("reload").addEventListener("click", loadEntries);

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
