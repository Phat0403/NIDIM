import TodoItem from "./TodoItem";
import type { Todo } from "../interface/type";

interface Props {
  todos: Todo[];
  toggleTodo: (id: number) => void;
  editTodo: (id: number, newText: string) => void;
  deleteTodo: (id: number) => void;
}

export default function TodoList({ todos, toggleTodo, editTodo, deleteTodo }: Props) {
  return (
    <ul className="space-y-2">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          toggleTodo={toggleTodo}
          editTodo={editTodo}
          deleteTodo={deleteTodo}
        />
      ))}
    </ul>
  );
}
