import { useState } from "react";
import { uploadFile, exportPDF } from "../services/api";

export default function Upload() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    try {
      const data = await uploadFile(file);
      setResult(data);
    } catch {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    const url = await exportPDF({
      title: "Upload Result",
      filename: "upload_output.pdf",
      corrected_text: result.corrected_text,
      summary: result.summary,
    });

    const a = document.createElement("a");
    a.href = url;
    a.download = "upload_output.pdf";
    a.click();
  };

  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold mb-6">Upload File</h2>

      <input type="file" onChange={handleUpload} />

      {loading && <p className="mt-4">Processing…</p>}

      {result && (
        <div className="mt-6 text-left space-y-4">
          <div>
            <h3 className="font-semibold">Corrected Text</h3>
            <p>{result.corrected_text}</p>
          </div>

          <div>
            <h3 className="font-semibold">Summary</h3>
            <p>{result.summary}</p>
          </div>

          <button
            onClick={handleExport}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
          >
            Export PDF
          </button>
        </div>
      )}
    </div>
  );
}
