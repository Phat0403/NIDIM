import { useState } from "react";
import type { FormEvent } from "react";

interface Props {
  addTodo: (text: string) => void;
}

export default function TodoInput({ addTodo }: Props) {
  const [value, setValue] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!value.trim()) return;
    addTodo(value.trim());
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex mb-4">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="flex-1 px-3 py-2 border rounded-l-lg focus:outline-none"
        placeholder="Enter a task..."
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
      >
        Add
      </button>
    </form>
  );
}
