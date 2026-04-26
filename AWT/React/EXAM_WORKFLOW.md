# 🧠 React Exam Workflow: In-Memory CRUD Mental Model

In a React exam question, if an external API or database is NOT provided, you'll be asked to build a Single Page Application (SPA) using **in-memory state**. This means all data is stored inside a `useState` array, and will reset if the page is refreshed.

Follow this workflow to rapidly build a frontend CRUD application using just React State.

---

## 🚦 Phase 1: Setup & Main State (5 mins)
*Goal: Initialize the project and set up the global state in `App.jsx`.*

1. **Create the App:**
   *(Assuming Vite or Create React App is already set up)*
   
2. **Setup `App.jsx` State:**
   Keep the main state at the very top level so it can be passed down to all components.
   ```jsx
   import { useState } from 'react';
   import ItemList from './ItemList';
   import ItemForm from './ItemForm';

   function App() {
     // Main In-Memory State
     const [items, setItems] = useState([
       { id: 1, name: 'Sample Item', price: 10 } // Initial dummy data
     ]);
     
     // State to track if we are currently editing an item
     const [editingItem, setEditingItem] = useState(null);

     // CRUD operations will go here...

     return (
       <div>
         <h1>React CRUD App</h1>
         {/* Components will go here */}
       </div>
     );
   }
   export default App;
   ```

---

## 💾 Phase 2: Implement CRUD Logic in App (10 mins)
*Goal: Write the functions to Create, Update, and Delete items.*

Inside `App.jsx` (above the `return`):

```jsx
  // CREATE
  const addItem = (newItem) => {
    // Generate a random ID (e.g., using Date.now())
    const itemWithId = { ...newItem, id: Date.now() };
    setItems([...items, itemWithId]);
  };

  // UPDATE
  const updateItem = (updatedItem) => {
    setItems(items.map(item => (item.id === updatedItem.id ? updatedItem : item)));
    setEditingItem(null); // Clear editing state after update
  };

  // DELETE
  const deleteItem = (id) => {
    if (window.confirm("Are you sure?")) {
      setItems(items.filter(item => item.id !== id));
    }
  };
```

Pass these functions down to your child components in the `return` statement:
```jsx
  return (
    <div>
      <h1>React CRUD App</h1>
      
      <ItemForm 
        addItem={addItem} 
        updateItem={updateItem} 
        editingItem={editingItem} 
        setEditingItem={setEditingItem} 
      />
      
      <ItemList 
        items={items} 
        deleteItem={deleteItem} 
        setEditingItem={setEditingItem} 
      />
    </div>
  );
```

---

## 🌐 Phase 3: READ & DELETE (List Component) (10 mins)
*Goal: Display the items and trigger delete/edit actions.*

**`ItemList.jsx`**
```jsx
function ItemList({ items, deleteItem, setEditingItem }) {
  return (
    <div>
      <h2>Items List</h2>
      {items.length === 0 ? <p>No items found.</p> : null}
      
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - ${item.price}
            
            <button onClick={() => setEditingItem(item)}>Edit</button>
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default ItemList;
```

---

## 📝 Phase 4: CREATE & UPDATE (Form Component) (15 mins)
*Goal: Use one form component for both Adding and Editing by watching `editingItem`.*

**`ItemForm.jsx`**
```jsx
import { useState, useEffect } from 'react';

function ItemForm({ addItem, updateItem, editingItem, setEditingItem }) {
  const [formData, setFormData] = useState({ name: '', price: '' });

  // Watch for 'editingItem' changes to pre-fill the form
  useEffect(() => {
    if (editingItem) {
      setFormData(editingItem); // Pre-fill with existing data
    } else {
      setFormData({ name: '', price: '' }); // Clear form for adding
    }
  }, [editingItem]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      updateItem(formData);
    } else {
      addItem(formData);
    }
    
    // Clear form after submit
    setFormData({ name: '', price: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{editingItem ? 'Edit Item' : 'Add New Item'}</h2>
      
      <input 
        name="name" 
        value={formData.name} 
        onChange={handleChange} 
        placeholder="Item Name" 
        required 
      />
      
      <input 
        name="price" 
        type="number" 
        value={formData.price} 
        onChange={handleChange} 
        placeholder="Price" 
        required 
      />
      
      <button type="submit">{editingItem ? 'Update' : 'Add'}</button>
      
      {/* Show Cancel button only when editing */}
      {editingItem && (
        <button type="button" onClick={() => setEditingItem(null)}>
          Cancel
        </button>
      )}
    </form>
  );
}
export default ItemForm;
```

---

## 💡 Top 3 React In-Memory Traps to Avoid
1. **Mutating State Directly:** NEVER do `items.push(newItem)`. Always use the spread operator: `setItems([...items, newItem])`. React won't re-render if you mutate directly!
2. **Missing `key` in maps:** When doing `{items.map(item => <li key={item.id}>)}`, forgetting the `key` prop will cause React rendering issues when items are added or deleted.
3. **Forgetting `e.preventDefault()`:** If your app flashes and reloads the page (losing all your in-memory data!) when you submit a form, you forgot `e.preventDefault()` in your `handleSubmit` function. React forms must override the default browser submit behavior!
