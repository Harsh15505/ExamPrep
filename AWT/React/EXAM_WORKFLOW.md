# 🧠 React Exam Workflow: The CRUD Mental Model

In a React exam question, you're building a Single Page Application (SPA). Unlike backend frameworks, React doesn't connect directly to a database; it manages state and communicates with an API.

Follow this workflow to rapidly build a frontend CRUD application.

---

## 🚦 Phase 1: Setup & Routing (5 mins)
*Goal: Initialize the project and set up React Router.*

1. **Install Router & Axios:**
   ```bash
   npm install react-router-dom axios
   ```

2. **Setup App.js Routing:**
   ```jsx
   import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
   import ItemList from './ItemList';
   import ItemForm from './ItemForm';

   function App() {
     return (
       <BrowserRouter>
         <nav>
            <Link to="/">Home</Link> | <Link to="/add">Add Item</Link>
         </nav>
         <Routes>
           <Route path="/" element={<ItemList />} />
           <Route path="/add" element={<ItemForm />} />
           <Route path="/edit/:id" element={<ItemForm />} />
         </Routes>
       </BrowserRouter>
     );
   }
   export default App;
   ```

---

## 🌐 Phase 2: READ (List Component) (10 mins)
*Goal: Fetch data on mount and display it.*

**`ItemList.jsx`**
```jsx
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function ItemList() {
  const [items, setItems] = useState([]);

  // Fetch data when component loads
  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/items');
      setItems(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if(window.confirm("Are you sure?")) {
        await axios.delete(`http://localhost:5000/api/items/${id}`);
        fetchItems(); // Refresh the list
    }
  };

  return (
    <div>
      <h2>Items</h2>
      <ul>
        {items.map(item => (
          <li key={item._id}>
            {item.name} - ${item.price}
            <Link to={`/edit/${item._id}`}>Edit</Link>
            <button onClick={() => handleDelete(item._id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default ItemList;
```

---

## 📝 Phase 3: CREATE & UPDATE (Form Component) (15 mins)
*Goal: Use one component for both Adding and Editing by checking the URL parameters.*

**`ItemForm.jsx`**
```jsx
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

function ItemForm() {
  const [formData, setFormData] = useState({ name: '', price: '' });
  const navigate = useNavigate();
  const { id } = useParams(); // Gets ID from URL (/edit/123)

  // If there's an ID, we are EDITING. Fetch existing data.
  useEffect(() => {
    if (id) {
      axios.get(`http://localhost:5000/api/items/${id}`)
        .then(res => setFormData(res.data))
        .catch(err => console.error(err));
    }
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        // UPDATE
        await axios.put(`http://localhost:5000/api/items/${id}`, formData);
      } else {
        // CREATE
        await axios.post('http://localhost:5000/api/items', formData);
      }
      navigate('/'); // Redirect back to list
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{id ? 'Edit Item' : 'Add Item'}</h2>
      
      <input 
        name="name" 
        value={formData.name} 
        onChange={handleChange} 
        placeholder="Name" 
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
      
      <button type="submit">Save</button>
    </form>
  );
}
export default ItemForm;
```

---

## 💡 Top 3 React Traps to Avoid
1. **Infinite Loops in `useEffect`:** If you forget the empty dependency array `[]` in your `useEffect` fetch call, React will fetch data, update state, re-render, fetch data again, infinitely crashing your browser.
2. **Missing `key` in maps:** When doing `{items.map(item => <li key={item.id}>)}`, forgetting the `key` prop will cause React rendering issues.
3. **Forgetting `e.preventDefault()`:** If your app flashes and reloads the page when you submit a form, you forgot `e.preventDefault()` in your `handleSubmit` function. React forms must override the default browser submit behavior!
