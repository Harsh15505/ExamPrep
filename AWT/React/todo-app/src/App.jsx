import React, { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import './App.css';

function App() {
  // 1. MAIN STATE
  const [tasks, setTasks] = useState([]);

  // 2. USEEFFECT HOOKS (LocalStorage)
  useEffect(() => {
    const savedTasks = JSON.parse(localStorage.getItem('todo-tasks'));
    if (savedTasks) setTasks(savedTasks);
  }, []);

  useEffect(() => {
    localStorage.setItem('todo-tasks', JSON.stringify(tasks));
  }, [tasks]);

  // 3. HANDLER FUNCTIONS (Passed down as Props)
  const handleAddTask = (text, category) => {
    const newTask = {
      id: Date.now(),
      text: text,
      category: category,
      completed: false
    };
    setTasks([...tasks, newTask]);
  };

  const handleToggleComplete = (id) => {
    const updatedTasks = tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    );
    setTasks(updatedTasks);
  };

  const handleDeleteTask = (id) => {
    const remainingTasks = tasks.filter(task => task.id !== id);
    setTasks(remainingTasks);
  };

  // 4. RENDERING COMPONENTS
  return (
    <div className="app-container">
      <h1>My To-Do List</h1>
      
      {/* Passing handleAddTask down to TaskForm via props */}
      <TaskForm onAddTask={handleAddTask} />

      {/* Passing tasks data and handlers down to TaskList via props */}
      <TaskList 
        tasks={tasks} 
        onToggleComplete={handleToggleComplete} 
        onDelete={handleDeleteTask} 
      />
    </div>
  );
}

export default App;
