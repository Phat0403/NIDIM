import { useState } from "react";
import type { Todo } from "../interface/type";

interface Props {
  todo: Todo;
  toggleTodo: (id: number) => void;
  editTodo: (id: number, newText: string) => void;
  deleteTodo: (id: number) => void;
}

export default function TodoItem({ todo, toggleTodo, editTodo, deleteTodo }: Props) {
  const [isEditing, setIsEditing] = useState(false);
  const [value, setValue] = useState(todo.text);

  const handleSave = () => {
    if (value.trim()) {
      editTodo(todo.id, value);
      setIsEditing(false);
    }
  };

  return (
    <li className="flex items-center justify-between bg-gray-50 p-2 rounded-lg shadow">
      {isEditing ? (
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="flex-1 px-2 py-1 border rounded"
        />
      ) : (
        <span
          onClick={() => toggleTodo(todo.id)}
          className={`flex-1 cursor-pointer ${
            todo.completed ? "line-through text-gray-400" : ""
          }`}
        >
          {todo.text}
        </span>
      )}

      <div className="flex gap-2 ml-2">
        {isEditing ? (
          <button
            onClick={handleSave}
            className="text-green-500 hover:text-green-700"
          >
            Save
          </button>
        ) : (
          <button
            onClick={() => setIsEditing(true)}
            className="text-blue-500 hover:text-blue-700"
          >
            Edit
          </button>
        )}
        <button
          onClick={() => deleteTodo(todo.id)}
          className="text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      </div>
    </li>
  );
}
