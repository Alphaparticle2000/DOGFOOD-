import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export default function Input({
  label,
  error,
  className = "",
  ...props
}: InputProps) {
  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-sm text-gray-300">
          {label}
        </label>
      )}

      <input
        {...props}
        className={`w-full rounded-lg border border-white/10 bg-[#080B14] px-4 py-3 text-white outline-none transition placeholder:text-gray-600 focus:border-blue-500 ${className}`}
      />

      {error && (
        <p className="text-sm text-red-400">{error}</p>
      )}
    </div>
  );
}