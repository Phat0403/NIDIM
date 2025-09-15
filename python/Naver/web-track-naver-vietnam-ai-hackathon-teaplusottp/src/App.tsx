import { useEffect, useState } from "react";
import axios from "axios";
import TodoInput from "./components/TodoInput";
import TodoList from "./components/TodoList";
import type { Todo } from "./interface/type";

const API = "http://localhost:8000/todos";

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([]);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    const res = await axios.get<Todo[]>(API);
    setTodos(res.data);
  };

  const addTodo = async (text: string) => {
    const res = await axios.post<Todo>(API, { text });
    setTodos([...todos, res.data]);
  };

  const toggleTodo = async (id: number) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;
    const res = await axios.put<Todo>(`${API}/${id}`, {
      text: todo.text,
      completed: !todo.completed,
    });
    setTodos(todos.map((t) => (t.id === id ? res.data : t)));
  };

  const editTodo = async (id: number, newText: string) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;
    const res = await axios.put<Todo>(`${API}/${id}`, {
      text: newText,
      completed: todo.completed,
    });
    setTodos(todos.map((t) => (t.id === id ? res.data : t)));
  };

  const deleteTodo = async (id: number) => {
    await axios.delete(`${API}/${id}`);
    setTodos(todos.filter((t) => t.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">📝 To-Do App</h1>
        <TodoInput addTodo={addTodo} />
        <TodoList
          todos={todos}
          toggleTodo={toggleTodo}
          editTodo={editTodo}
          deleteTodo={deleteTodo}
        />
      </div>
    </div>
  );
}
