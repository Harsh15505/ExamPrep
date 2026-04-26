import React, { useState } from 'react';

function TaskForm({ onAddTask }) {
  // Local state for the form inputs
  const [inputTask, setInputTask] = useState('');
  const [category, setCategory] = useState('Personal');

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent page reload
    
    // Validation
    if (inputTask.trim() === '') {
      alert("Task cannot be empty!");
      return;
    }

    // Call the parent's function passed via props
    onAddTask(inputTask, category);
    
    // Clear input field
    setInputTask('');
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input 
        type="text" 
        placeholder="What needs to be done?" 
        value={inputTask} 
        onChange={(e) => setInputTask(e.target.value)} 
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
