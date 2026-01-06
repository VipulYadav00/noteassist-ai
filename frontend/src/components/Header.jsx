import React from 'react';

export default function LivePanel({ isListening, startLive, stopLive, liveText, setLiveText, analyzePreview, summarizeText, setResult, loadHistory, setLoading }) {
  return (
    <div>
      <h3 className="font-semibold text-lg">Live Transcription</h3>
      <p className="text-sm text-gray-600 mb-2">Use your microphone to transcribe speech in real time.</p>
      <div className="flex items-center gap-3 mb-2">
        <button onClick={startLive} disabled={isListening} className="py-2 px-3 rounded bg-yellow-500 text-white">Start Live</button>
        <button onClick={stopLive} disabled={!isListening} className="py-2 px-3 rounded bg-gray-200">Stop Live</button>

        <button onClick={async () => { if (!liveText.trim()) return alert('No live text to preview'); try { setLoading(true); const preview = await analyzePreview(liveText, 'live'); setResult(preview); } catch (err) { console.error(err); alert('Preview failed'); } finally { setLoading(false); } }} className="py-2 px-3 rounded border bg-white">Preview</button>

        <button onClick={async () => { if (!liveText.trim()) return alert('No live text to save'); try { setLoading(true); const data = await summarizeText(liveText, 'live'); setResult(data); loadHistory(); } catch (err) { console.error(err); alert('Failed to save live transcript'); } finally { setLoading(false); } }} className="py-2 px-3 rounded bg-indigo-600 text-white">Analyze Live</button>

        <button onClick={() => { setLiveText(''); }} className="py-2 px-3 rounded bg-gray-200">Clear</button>
      </div>

      <textarea value={liveText} onChange={(e) => setLiveText(e.target.value)} rows={6} placeholder="Live transcript will appear here... (you can edit before saving)" className="w-full p-3 border rounded resize-none text-sm bg-white" />
    </div>
  );
}
