import { useRef, useState } from "react";
import { sendLiveAudio, exportPDF } from "../services/api";

export default function Live() {
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);

    recorder.ondataavailable = (e) => chunksRef.current.push(e.data);

    recorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      chunksRef.current = [];
      setLoading(true);

      try {
        const data = await sendLiveAudio(blob);
        setResult(data);
      } catch {
        alert("Live processing failed");
      } finally {
        setLoading(false);
      }
    };

    mediaRecorderRef.current = recorder;
    recorder.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  const handleExport = async () => {
    const url = await exportPDF({
      title: "Live Result",
      filename: "live_output.pdf",
      corrected_text: result.corrected_text,
      summary: result.summary,
    });

    const a = document.createElement("a");
    a.href = url;
    a.download = "live_output.pdf";
    a.click();
  };

  return (
    <div className="text-center animate-fade-in">
      <h2 className="text-3xl font-bold mb-6">Live Speech</h2>

      {!recording ? (
        <button
          onClick={startRecording}
          className="px-6 py-2 bg-green-600 text-white rounded"
        >
          Start Recording
        </button>
      ) : (
        <button
          onClick={stopRecording}
          className="px-6 py-2 bg-red-600 text-white rounded"
        >
          Stop Recording
        </button>
      )}

      {loading && <p className="mt-4 animate-pulse">Processing…</p>}

      {result && (
        <div className="mt-6 text-left space-y-4">
          <div>
            <h3 className="font-semibold">Transcription</h3>
            <p>{result.original_text}</p>
          </div>

          <div>
            <h3 className="font-semibold">Corrected</h3>
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
