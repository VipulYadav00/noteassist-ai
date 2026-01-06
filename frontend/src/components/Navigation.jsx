export default function Navigation({
  activeTab,
  setActiveTab,
  darkMode,
  setDarkMode,
}) {
  const tabs = ["paste", "upload", "live"];

  return (
    <div className="flex items-center justify-between mb-6">
      {/* Tabs */}
      <div className="flex gap-3">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition
              ${
                activeTab === tab
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600"
              }
            `}
          >
            {tab.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Dark Mode Toggle */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="px-3 py-2 text-sm rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
      >
        {darkMode ? "🌙 Dark" : "☀️ Light"}
      </button>
    </div>
  );
}
