# 🧠 Express & MongoDB Exam Workflow: The CRUD Mental Model

In an Express.js exam question, you'll generally use **Express** as the server, **Mongoose** to interact with MongoDB, and **EJS** for server-side templating.

Follow this strict, linear workflow.

---

## 🚦 Phase 1: Setup & Configuration (5 mins)
*Goal: Initialize the app, middleware, and database connection.*

1. **Imports and Initialization:**
   ```javascript
   const express = require('express');
   const mongoose = require('mongoose');
   const app = express();
   ```

2. **Middleware & EJS:**
   ```javascript
   // Parse form data
   app.use(express.urlencoded({ extended: true }));
   
   // Set EJS as templating engine
   app.set('view engine', 'ejs');
   ```

3. **Database Connection:**
   ```javascript
   mongoose.connect('mongodb://localhost:27017/examDB', {
       useNewUrlParser: true,
       useUnifiedTopology: true
   }).then(() => console.log("MongoDB Connected"))
     .catch(err => console.log(err));
   ```

---

## 💾 Phase 2: Mongoose Models (5 mins)
*Goal: Define the MongoDB Schema.*

```javascript
const itemSchema = new mongoose.Schema({
    name: { type: String, required: true },
    price: { type: Number, required: true },
    createdAt: { type: Date, default: Date.now }
});

const Item = mongoose.model('Item', itemSchema);
```

---

## 🌐 Phase 3: Routes & Controllers (CRUD) (15 mins)
*Goal: Use `async/await` to handle database operations inside routes.*

**1. READ (List All):**
```javascript
app.get('/', async (req, res) => {
    try {
        const items = await Item.find({});
        res.render('index', { items: items }); // Renders views/index.ejs
    } catch (err) {
        res.status(500).send("Error reading DB");
    }
});
```

**2. CREATE:**
```javascript
// Show form
app.get('/add', (req, res) => {
    res.render('add');
});

// Handle form submission
app.post('/add', async (req, res) => {
    try {
        const newItem = new Item({
            name: req.body.name,
            price: req.body.price
        });
        await newItem.save();
        res.redirect('/');
    } catch (err) {
        res.status(500).send("Error saving item");
    }
});
```

**3. UPDATE:**
```javascript
// Show edit form
app.get('/edit/:id', async (req, res) => {
    const item = await Item.findById(req.params.id);
    res.render('edit', { item: item });
});

// Handle update submission
app.post('/edit/:id', async (req, res) => {
    try {
        await Item.findByIdAndUpdate(req.params.id, {
            name: req.body.name,
            price: req.body.price
        });
        res.redirect('/');
    } catch (err) {
        res.status(500).send("Error updating item");
    }
});
```

**4. DELETE:**
```javascript
app.post('/delete/:id', async (req, res) => {
    try {
        await Item.findByIdAndDelete(req.params.id);
        res.redirect('/');
    } catch (err) {
        res.status(500).send("Error deleting item");
    }
});
```

---

## 🎨 Phase 4: Views (EJS) (10 mins)
*Goal: Create HTML files inside the `views/` folder with `.ejs` extensions.*

**1. `views/index.ejs`**
```html
<a href="/add">Add New Item</a>
<ul>
    <% items.forEach(function(item) { %>
        <li>
            <%= item.name %> - $<%= item.price %>
            <a href="/edit/<%= item._id %>">Edit</a>
            
            <form action="/delete/<%= item._id %>" method="POST" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
    <% }) %>
</ul>
```

**2. `views/add.ejs` & `views/edit.ejs`**
*(Make sure the `name` attributes match `req.body.xyz`)*
```html
<form method="POST">
    <!-- In edit.ejs, use value="<%= item.name %>" -->
    <label>Name</label>
    <input type="text" name="name" required>
    
    <label>Price</label>
    <input type="number" step="0.01" name="price" required>
    
    <button type="submit">Save</button>
</form>
```

---

## 🏃 Phase 5: Start the Server
```javascript
app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
```

## 💡 Top 3 Express Traps to Avoid
1. **Forgetting `express.urlencoded`:** If your `req.body` is `undefined` when submitting a form, you forgot `app.use(express.urlencoded({ extended: true }))`.
2. **Missing `views` folder:** EJS looks for templates specifically inside a folder named `views`.
3. **Sync vs Async:** Database calls (`Item.find()`, `item.save()`) take time. Always mark your route callbacks as `async` and use `await`, or your renders will trigger before the data is ready!
