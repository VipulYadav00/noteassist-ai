import { useState } from "react";
import { analyzeText, exportPDF } from "../services/api";

export default function Paste() {
  const [text, setText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const data = await analyzeText(text);
      setCorrectedText(data.corrected_text);
      setSummary(data.summary);
    } catch (err) {
      alert("Error analyzing text");
    } finally {
      setLoading(false);
    }
  }

  async function handleDownloadPDF() {
    try {
      const blob = await exportPDF({
        title: "NoteAssist – AI Notes",
        filename: "noteassist_notes",
        corrected_text: correctedText,
        summary: summary,
      });

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "noteassist_notes.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error downloading PDF");
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-semibold">Paste Text</h2>

      <textarea
        className="w-full h-40 p-3 border rounded"
        placeholder="Paste your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {correctedText && (
        <>
          <div className="mt-4">
            <h3 className="font-semibold">Corrected Text</h3>
            <p className="p-2 border rounded">{correctedText}</p>
          </div>

          <div className="mt-4">
            <h3 className="font-semibold">Summary</h3>
            <p className="p-2 border rounded">{summary}</p>
          </div>

          <button
            onClick={handleDownloadPDF}
            className="mt-4 px-4 py-2 bg-green-600 text-white rounded"
          >
            Download PDF
          </button>
        </>
      )}
    </div>
  );
}
