const API_BASE = "http://127.0.0.1:8000";

/* =======================
   ANALYZE (PASTE)
======================= */
export async function analyzeText(text) {
  const res = await fetch(`${API_BASE}/analyze/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) throw new Error("Analyze failed");
  return await res.json();
}

/* =======================
   UPLOAD
======================= */
export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/upload/media`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Upload failed");
  return await res.json();
}

/* =======================
   LIVE AUDIO
======================= */
export async function sendLiveAudio(blob) {
  const form = new FormData();
  form.append("file", blob, "live.webm");

  const res = await fetch(`${API_BASE}/live/audio`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Live processing failed");
  return await res.json();
}

/* =======================
   EXPORT PDF
======================= */
export async function exportPDF(payload) {
  const res = await fetch(`${API_BASE}/export/pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("PDF export failed");

  const blob = await res.blob();
  return window.URL.createObjectURL(blob);
}

/* =======================
   HISTORY
======================= */
export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error("History fetch failed");
  return await res.json();
}

export async function deleteHistoryOne(id) {
  await fetch(`${API_BASE}/history/${id}`, { method: "DELETE" });
}

export async function deleteHistoryMany(ids) {
  await fetch(`${API_BASE}/history/bulk`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ids }),
  });
}

export async function deleteHistoryAll() {
  await fetch(`${API_BASE}/history`, { method: "DELETE" });
}
