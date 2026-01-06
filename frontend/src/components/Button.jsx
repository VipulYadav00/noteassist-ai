export default function Button({
  children,
  onClick,
  variant = "primary",
  disabled = false,
  className = "",
}) {
  const base =
    "px-4 py-2 rounded-lg font-medium transition-all duration-200 focus:outline-none";

  const variants = {
    primary:
      "bg-blue-600 text-white hover:bg-blue-700 hover:scale-105 active:scale-95",
    secondary:
      "bg-gray-100 text-gray-700 hover:bg-gray-200 hover:scale-105 active:scale-95",
    danger:
      "bg-red-500 text-white hover:bg-red-600 hover:scale-105 active:scale-95",
    text:
      "bg-transparent text-blue-600 hover:underline",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      } ${className}`}
    >
      {children}
    </button>
  );
}
