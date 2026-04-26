import React from 'react';

function TaskItem({ task, onToggleComplete, onDelete }) {
  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      
      <div className="task-content">
        <span className="task-category badge">{task.category}</span>
        
        {/* Apply strikethrough class if task.completed is true */}
        <span className={`task-text ${task.completed ? 'strikethrough' : ''}`}>
          {task.text}
        </span>
      </div>

      <div className="task-actions">
        <button 
          onClick={() => onToggleComplete(task.id)} 
          className={`complete-btn ${task.completed ? 'undo' : ''}`}
        >
          {task.completed ? 'Undo' : 'Complete'}
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
