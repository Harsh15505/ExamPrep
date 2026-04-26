# React To-Do List Application: Detailed Guide (Component-Based)

This guide breaks down the React application line-by-line. We have refactored the app into a modern, **Component-Based Architecture**. The main `App` component holds the state, and passes data and functions down to child components (`TaskForm`, `TaskList`, `TaskItem`) using **Props**.

---

## 📁 Folder Structure
```text
src/
├── App.jsx            (Main State & Layout)
├── App.css            (Styling)
└── components/
    ├── TaskForm.jsx   (Form to add tasks)
    ├── TaskList.jsx   (Wrapper for rendering multiple tasks)
    └── TaskItem.jsx   (Individual task row)
```

---

## 📄 1. `src/App.jsx` (The Parent Component)

```jsx
import React, { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
// Imports our custom child components so we can use them like HTML tags below.
import './App.css';

function App() {
  // ==========================================
  // 1. MAIN STATE (The "Source of Truth")
  // ==========================================
  const [tasks, setTasks] = useState([]);
  // Initializes a state variable called 'tasks' as an empty array [].
  // All task data lives HERE in the parent component.

  // ==========================================
  // 2. USEEFFECT HOOKS (LocalStorage)
  // ==========================================
  useEffect(() => {
    const savedTasks = JSON.parse(localStorage.getItem('todo-tasks'));
    if (savedTasks) setTasks(savedTasks);
  }, []);
  // Runs ONLY ONCE on mount. Fetches saved tasks from browser storage and updates state.

  useEffect(() => {
    localStorage.setItem('todo-tasks', JSON.stringify(tasks));
  }, [tasks]);
  // Runs EVERY TIME 'tasks' array changes. Saves the new array to browser storage.

  // ==========================================
  // 3. HANDLER FUNCTIONS
  // ==========================================
  const handleAddTask = (text, category) => {
  // This function takes text and category as arguments (which will be provided by the TaskForm child).
    const newTask = {
      id: Date.now(),
      text: text,
      category: category,
      completed: false
    };
    setTasks([...tasks, newTask]);
    // Updates state by creating a new array with all existing tasks plus the new one.
  };

  const handleToggleComplete = (id) => {
  // Finds the task by ID and flips its 'completed' boolean.
    const updatedTasks = tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    );
    setTasks(updatedTasks);
  };

  const handleDeleteTask = (id) => {
  // Filters out the task matching the ID, effectively deleting it.
    const remainingTasks = tasks.filter(task => task.id !== id);
    setTasks(remainingTasks);
  };

  // ==========================================
  // 4. RENDERING (Passing Props)
  // ==========================================
  return (
    <div className="app-container">
      <h1>My To-Do List</h1>
      
      <TaskForm onAddTask={handleAddTask} />
      {/* We render the TaskForm component. */}
      {/* Prop Passing: We pass the 'handleAddTask' function down to the child under the prop name 'onAddTask'. */}

      <TaskList 
        tasks={tasks} 
        onToggleComplete={handleToggleComplete} 
        onDelete={handleDeleteTask} 
      />
      {/* We pass the 'tasks' array AND the handler functions down to the TaskList so it can render and modify data. */}
    </div>
  );
}

export default App;
```

---

## 📄 2. `src/components/TaskForm.jsx` (Child)

```jsx
import React, { useState } from 'react';

function TaskForm({ onAddTask }) {
// Destructures the 'onAddTask' prop passed from App.jsx.

  const [inputTask, setInputTask] = useState('');
  const [category, setCategory] = useState('Personal');
  // Local state. We only need to track what the user is typing here in the form, 
  // we don't need the whole app to know about every keystroke until they hit submit.

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page reload
    
    if (inputTask.trim() === '') {
      alert("Task cannot be empty!");
      return;
    }

    onAddTask(inputTask, category);
    // Calls the parent function (handleAddTask in App.jsx), passing the local input data up to the parent!
    
    setInputTask('');
    // Clears the input field after successful submission.
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input 
        type="text" 
        placeholder="What needs to be done?" 
        value={inputTask} 
        onChange={(e) => setInputTask(e.target.value)} 
        // Two-way binding updates local state on every keystroke.
      />
      
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="Personal">Personal work</option>
        <option value="Office">Office</option>
        <option value="Home">Home</option>
      </select>
      
      <button type="submit" className="add-btn">Add Task</button>
    </form>
  );
}

export default TaskForm;
```

---

## 📄 3. `src/components/TaskList.jsx` (Child)

```jsx
import React from 'react';
import TaskItem from './TaskItem';
// Imports the individual TaskItem component.

function TaskList({ tasks, onToggleComplete, onDelete }) {
// Destructures the array and handler functions passed from App.jsx.

  if (tasks.length === 0) {
    return <p className="empty-message">No tasks yet. Add one above!</p>;
    // Early return: If the array is empty, just render this paragraph and stop.
  }

  return (
    <div className="task-list">
      {tasks.map(task => (
      // Loops over every task object in the array...

        <TaskItem 
          key={task.id} 
          // 'key' is mandatory in React when using .map(). It helps React optimize re-renders.
          task={task} 
          // Passes the individual task object down to the TaskItem.
          onToggleComplete={onToggleComplete} 
          onDelete={onDelete} 
          // Passes the handler functions down yet another level!
        />

      ))}
    </div>
  );
}

export default TaskList;
```

---

## 📄 4. `src/components/TaskItem.jsx` (Grandchild)

```jsx
import React from 'react';

function TaskItem({ task, onToggleComplete, onDelete }) {
// Destructures the specific 'task' object and handler functions passed from TaskList.jsx.

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
    {/* Template Literals dynamically apply the 'completed' CSS class if task.completed is true. */}
      
      <div className="task-content">
        <span className="task-category badge">{task.category}</span>
        
        <span className={`task-text ${task.completed ? 'strikethrough' : ''}`}>
        {/* REQUIREMENT: Strikethrough effect based on completion status. */}
          {task.text}
        </span>
      </div>

      <div className="task-actions">
        <button 
          onClick={() => onToggleComplete(task.id)} 
          // When clicked, calls the parent function, passing THIS task's ID all the way back up to App.jsx!
          className={`complete-btn ${task.completed ? 'undo' : ''}`}
        >
          {task.completed ? 'Undo' : 'Complete'}
          {/* Conditional text rendering based on state. */}
        </button>
        
        <button 
          onClick={() => onDelete(task.id)} 
          className="delete-btn"
        >
          Delete
        </button>
      </div>

    </div>
  );
}

export default TaskItem;
```
