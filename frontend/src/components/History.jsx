import { useEffect, useState } from "react";
import {
  fetchHistory,
  deleteHistoryOne,
  deleteHistoryMany,
  deleteHistoryAll,
} from "../services/api";

export default function History() {
  const [items, setItems] = useState([]);
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    const data = await fetchHistory();

    const mapped = data.map((note) => ({
      id: note.id,
      type: note.input_type,
      text: note.original_text,
      summary: note.summary,
      time: new Date(note.created_at).toLocaleString(),
    }));

    setItems(mapped);
  }

  const toggleSelect = (id) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="w-full px-4 py-2 mb-2 rounded bg-gray-700 text-white"
      >
        History
      </button>

      {open && (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {items.length === 0 && (
            <p className="text-sm text-gray-400">No history yet</p>
          )}

          {items.map((item) => (
            <div
              key={item.id}
              onDoubleClick={() => toggleSelect(item.id)}
              className="p-3 border rounded hover:bg-gray-700 cursor-pointer"
            >
              <p className="text-xs text-blue-400 uppercase">{item.type}</p>
              <p className="text-sm text-white truncate">{item.text}</p>
              <p className="text-xs text-gray-400">{item.time}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
