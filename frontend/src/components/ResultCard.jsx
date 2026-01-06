export default function ResultCard({ title, content }) {
  return (
    <div className="animate-fade-in border border-gray-200 rounded-xl p-6 mt-6 bg-gray-50">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-700 whitespace-pre-line">
        {content}
      </p>
    </div>
  );
}
