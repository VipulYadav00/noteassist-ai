import { useState } from "react";
import Navigation from "./components/Navigation";
import Paste from "./Sections/Paste";
import Upload from "./Sections/Upload";
import Live from "./Sections/Live";
import History from "./components/History";

import { analyzeText, fetchHistory } from "./services/api";

function App() {
  const [activeTab, setActiveTab] = useState("paste");
  const [darkMode, setDarkMode] = useState(false);

  const [text, setText] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [history, setHistory] = useState([]);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  /* 🌙 Dark mode */
  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
    document.documentElement.classList.toggle("dark");
  };

  /* 🔍 Analyze using BACKEND */
  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setIsAnalyzing(true);
    try {
      const data = await analyzeText(text);
      setAnalysisResult(data);

      // Reload history from backend
      const updatedHistory = await fetchHistory();
      setHistory(updatedHistory);
    } catch (err) {
      alert("Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-2xl shadow-lg p-8 grid grid-cols-4 gap-6">

        {/* History (from BACKEND) */}
        <div className="col-span-1 border-r dark:border-gray-700 pr-4">
          <History items={history} />
        </div>

        {/* Main content */}
        <div className="col-span-3">
          <Navigation
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            darkMode={darkMode}
            setDarkMode={toggleDarkMode}
          />

          {activeTab === "paste" && (
            <Paste
              text={text}
              setText={setText}
              onAnalyze={handleAnalyze}
              isAnalyzing={isAnalyzing}
              analysisResult={analysisResult}
            />
          )}

          {activeTab === "upload" && <Upload />}

          {activeTab === "live" && <Live />}
        </div>
      </div>
    </div>
  );
}

export default App;
