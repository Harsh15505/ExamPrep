# 🚀 Node.js & Express Guide

## 🧠 Section 1 — Node.js & Express Theory

### What is Node.js?
Node.js is an open-source, cross-platform JavaScript runtime environment built on Chrome's V8 engine. It allows developers to run JavaScript on the server side, outside of a web browser.
- **Asynchronous & Event-Driven:** Non-blocking I/O operations make Node.js lightweight and efficient.
- **Single-Threaded:** Uses a single thread with an event loop, making it highly scalable for handling concurrent requests without the overhead of thread context switching.
- **NPM (Node Package Manager):** The largest software registry globally, providing thousands of open-source libraries that can be easily integrated into projects.

### Blocking vs Non-Blocking Operations
- **Blocking (Synchronous):** The execution of additional JavaScript in the Node.js process must wait until an I/O operation (like reading a file or querying a database) completes. It "blocks" the main single thread.
  - *Example:* `fs.readFileSync('file.txt')` — The server literally stops everything else until the file is fully read. No other users can be served during this time.
- **Non-Blocking (Asynchronous):** The Node.js process continues executing other JavaScript code while the heavy I/O operation happens in the background. Once the background task finishes, a callback is triggered to handle the result.
  - *Example:* `fs.readFile('file.txt', callback)` — The server initiates the file read, then immediately moves on to serve other clients while the file is being read in the background.

### The Event Loop
The Event Loop is the secret mechanism that allows Node.js to perform non-blocking I/O operations despite JavaScript being single-threaded.
- When an asynchronous operation is triggered, Node.js offloads the heavy lifting to the system kernel (which is multithreaded) via the `libuv` library.
- The main JavaScript thread continues running other code without pausing.
- Once the kernel finishes the background operation, it puts the associated callback function into a **Task Queue** (or Callback Queue).
- The **Event Loop** is a continuous process that monitors the Call Stack. When the Call Stack is completely empty, the Event Loop grabs the first callback from the Task Queue and pushes it onto the Call Stack to be executed.

### Promises and Async/Await
Historically, asynchronous Node.js code relied heavily on callbacks, which often led to deeply nested, unreadable code known as "Callback Hell" (or the Pyramid of Doom).
- **Promises:** An object representing the eventual completion (or failure) of an asynchronous operation. Instead of passing callbacks, you chain `.then()` for success and `.catch()` for errors.
- **Async/Await:** Syntactic sugar built on top of Promises, introduced in modern JavaScript. It allows you to write asynchronous, non-blocking code that *reads* top-to-bottom like synchronous code.
  - You add the `async` keyword before a function declaration to indicate it will handle asynchronous operations (it automatically returns a Promise).
  - Inside an `async` function, you place the `await` keyword in front of any Promise-returning function (like a database query). This pauses the execution of *that specific function* until the Promise resolves, without blocking the main server thread.

### What is Express.js?
Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications. It acts as a higher-level layer built on top of Node.js to simplify server creation.
- **Routing:** Provides a robust routing mechanism to handle client requests based on HTTP methods (GET, POST, etc.) and URLs.
- **Middleware:** Functions that have access to the request and response objects. They form a pipeline to process requests before they hit the final route handler.
- **Templating:** Easily integrates with template engines like EJS, Pug, or Handlebars to render dynamic HTML pages on the server.

### What is Mongoose?
Mongoose is an Object Data Modeling (ODM) library for MongoDB and Node.js. It manages relationships between data, provides schema validation, and translates between objects in code and the representation of those objects in MongoDB.
- **Schemas:** Defines the structure of the document, data types, default values, and validators.
- **Models:** Compiled from Schemas, Models provide an interface to the database for querying, creating, updating, and deleting records.

---

## 🏗️ Section 2 — Basic Code Structure

This is the absolute minimum code required to spin up an Express server.

```javascript
// 1. Import express module
const express = require('express');

// 2. Initialize the Express application
const app = express();

// 3. Define the port number
const PORT = 3000;

// 4. Create a basic route for GET requests to the root URL '/'
app.get('/', (req, res) => {
    res.send('Hello, World! Welcome to Express.');
});

// 5. Start the server and listen on the specified port
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```

---

## 🔄 Section 3 — Database Connected CRUD Operations (Mongoose & MongoDB)

CRUD (Create, Read, Update, Delete) maps directly to standard HTTP methods: POST, GET, PUT/PATCH, and DELETE. This example uses **Mongoose** to interact with a MongoDB database.

```javascript
const express = require('express');
const mongoose = require('mongoose');
const app = express();

// Middleware to parse incoming JSON payloads
app.use(express.json()); 

// 1. Connect to MongoDB Database
mongoose.connect('mongodb://localhost:27017/express_crud_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log('✅ MongoDB Connected'))
.catch(err => console.error('❌ MongoDB Connection Error:', err));

// 2. Define Mongoose Schema & Model
const userSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    age: { type: Number, default: 18 },
    createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// READ (GET) - Retrieve all users
app.get('/users', async (req, res) => {
    try {
        const users = await User.find(); // Fetches all documents
        res.status(200).json(users);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// READ (GET) - Retrieve a single user by ID
app.get('/users/:id', async (req, res) => {
    try {
        const user = await User.findById(req.params.id);
        if (!user) return res.status(404).json({ message: 'User not found' });
        res.status(200).json(user);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// CREATE (POST) - Add a new user
app.post('/users', async (req, res) => {
    try {
        // Create a new instance and save it to the database
        const newUser = new User(req.body);
        const savedUser = await newUser.save(); 
        res.status(201).json(savedUser); // 201 Created
    } catch (err) {
        res.status(400).json({ error: err.message }); // 400 Bad Request for validation errors
    }
});

// UPDATE (PUT) - Fully update an existing user
app.put('/users/:id', async (req, res) => {
    try {
        // findByIdAndUpdate(id, updateData, options)
        // { new: true } returns the updated document instead of the old one
        const updatedUser = await User.findByIdAndUpdate(req.params.id, req.body, { new: true, runValidators: true });
        
        if (!updatedUser) return res.status(404).json({ message: 'User not found' });
        res.status(200).json(updatedUser);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// DELETE (DELETE) - Remove a user
app.delete('/users/:id', async (req, res) => {
    try {
        const deletedUser = await User.findByIdAndDelete(req.params.id);
        
        if (!deletedUser) return res.status(404).json({ message: 'User not found' });
        res.status(200).json({ message: 'User deleted successfully' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(3000, () => console.log('🚀 Server running on port 3000'));
```

---

## 🛡️ Section 4 — Middlewares

Middleware functions are the backbone of Express. They have access to the request object (`req`), the response object (`res`), and the `next` function. 

They can:
1. Execute any code.
2. Make changes to the request and response objects.
3. End the request-response cycle.
4. Call the next middleware function in the stack using `next()`.

### Example: Logging Middleware (Global)
```javascript
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} request to ${req.url}`);
    
    // IMPORTANT: Pass control to the next middleware or route handler.
    // If you forget this, the request will hang forever!
    next(); 
};

// Apply to ALL routes
app.use(loggerMiddleware); 
```

### Example: Authentication Middleware (Route-specific)
```javascript
const requireAuth = (req, res, next) => {
    const isAuth = true; // Simulated authentication check
    
    if (isAuth) {
        next(); // User is authenticated, proceed to the route
    } else {
        res.status(401).send('Unauthorized Access'); // End the cycle here
    }
};

// Apply ONLY to the /dashboard route
app.get('/dashboard', requireAuth, (req, res) => {
    res.send('Welcome to the secure dashboard!');
});
```

---

## 🏛️ Section 5 — MVC Architecture in Express

MVC (Model-View-Controller) separates an application into logical components, making code maintainable and scalable.

*   **Model:** Handles data logic and database interactions (e.g., MongoDB schemas using Mongoose).
*   **View:** Handles UI/Presentation. In modern API development, this might just be sending JSON, or rendering EJS/Pug templates for server-side rendering.
*   **Controller:** Contains the business logic. It takes user input from the router, interacts with the Model, and dictates what the View should render/return.

### Recommended Directory Structure:
```text
project-root/
│
├── controllers/
│   └── userController.js  # Business logic
├── models/
│   └── userModel.js       # Database schema/logic
├── routes/
│   └── userRoutes.js      # URL routing mapping to controllers
├── views/                 # (Optional) HTML Templates if using EJS/Pug
├── app.js                 # Entry point / Server setup
└── package.json
```

### Code Example of MVC Separation:

**1. models/userModel.js** (Mongoose Schema)
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: String,
    email: String
});

module.exports = mongoose.model('User', userSchema);
```

**2. controllers/userController.js**
```javascript
const User = require('../models/userModel'); // Import Model

exports.getUsers = async (req, res) => {
    try {
        // Business Logic: Fetch users from DB
        const users = await User.find();
        res.json(users); // The "View" output
    } catch (error) {
        res.status(500).json({ error: 'Server Error' });
    }
};
```

**3. routes/userRoutes.js**
```javascript
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController'); // Import Controller

// Map route to controller function
router.get('/', userController.getUsers);

module.exports = router;
```

**4. app.js**
```javascript
const express = require('express');
const app = express();
const userRoutes = require('./routes/userRoutes');

// Mount the modular router
app.use('/users', userRoutes);

app.listen(3000, () => console.log('MVC Server running'));
```

---

## 🗣️ Section 6 — Viva Questions & Answers

**1. Q: What is Node.js and how does it work?**
> **A:** Node.js is a server-side runtime environment built on Chrome's V8 JavaScript engine. It operates on a single-threaded, non-blocking, event-driven architecture, making it highly efficient and scalable for I/O-intensive web applications.

**2. Q: What is the Event Loop in Node.js?**
> **A:** The event loop handles asynchronous operations. While Node's main execution thread is single-threaded, the event loop offloads heavy I/O operations (like file reading or network requests) to the system kernel. When the operation finishes, a callback is queued and eventually executed on the main thread, preventing the server from blocking.

**3. Q: What is Express.js?**
> **A:** Express.js is a minimal and unopinionated web application framework for Node.js. It simplifies building robust web servers and RESTful APIs by providing essential utility features like routing, middleware support, and request/response enhancements.

**4. Q: What is Middleware in Express?**
> **A:** Middleware are functions that execute during the request-response cycle. They have access to `req`, `res`, and `next`. They can modify request/response objects, log data, parse bodies, handle authentication, and must either end the response cycle or call `next()` to pass control to the next function.

**5. Q: How do you parse JSON POST bodies in Express?**
> **A:** By using the built-in middleware: `app.use(express.json());`. This intercepts incoming requests, parses payloads formatted as JSON, and makes the resulting JavaScript object available on `req.body`.

**6. Q: What is the purpose of `next()` in Express?**
> **A:** `next()` is a callback function passed to middleware. When invoked, it tells Express to move to the succeeding middleware or route handler in the stack. If a middleware doesn't end the response (e.g., `res.send()`) and fails to call `next()`, the client's request will hang indefinitely.

**7. Q: Explain the MVC architecture in the context of an Express app.**
> **A:** MVC structures the app cleanly. **Models** handle DB operations (like querying MongoDB via Mongoose). **Controllers** contain the core business logic (validating inputs, asking models for data). **Views** format the output (rendering HTML or returning JSON). Express **Routers** act as the dispatcher, mapping specific URLs to Controller functions.

**8. Q: What is `express.Router` used for?**
> **A:** `express.Router` is a class used to create modular, mountable route handlers. It acts as a "mini-application," helping to organize routing logic into separate, manageable files instead of clustering every route in the main `app.js` file.

**9. Q: Differentiate between `req.params` and `req.query`.**
> **A:** 
> - `req.params` retrieves parameters embedded directly in the route path (e.g., Route: `/users/:id` -> URL: `/users/123` -> `req.params.id` is '123').
> - `req.query` retrieves parameters from the query string at the end of the URL (e.g., URL: `/users?sort=asc` -> `req.query.sort` is 'asc').

**10. Q: Why use Node.js instead of traditional multithreaded servers like Apache?**
> **A:** Node's non-blocking I/O makes it excellent for handling thousands of concurrent connections with very low memory overhead. It's ideal for real-time apps (chat, streaming). Traditional servers often create a new physical thread per request, which can consume significant RAM and CPU under heavy load due to thread context switching.

**11. Q: How do you handle errors in Express?**
> **A:** By creating a special error-handling middleware. It is defined with four arguments instead of three: `(err, req, res, next)`. It is typically placed at the very end of the middleware stack in `app.js` to catch any errors thrown by preceding routes or middlewares.

**12. Q: What is the `package.json` file?**
> **A:** It is the core manifest file for any Node.js project. It contains metadata about the project (name, version), custom scripts (like `npm start`), and most importantly, lists all the dependencies (packages) and their exact versions required by the application.

**13. Q: What is Mongoose and why do we use it with Express?**
> **A:** Mongoose is an Object Data Modeling (ODM) library for MongoDB and Node.js. While you can use the native MongoDB driver, Mongoose provides a rigorous schema-based solution to model your application data. It includes built-in type casting, validation, query building, and business logic hooks, which makes interacting with the database much easier and more predictable.

**14. Q: Explain the concept of Promises and async/await.**
> **A:** A Promise represents the eventual completion (or failure) of an asynchronous operation and its resulting value. `async/await` is syntactic sugar built on top of Promises that makes asynchronous code look and behave a bit more like synchronous code, making it much easier to read and maintain.

**15. Q: What is the difference between `res.send()`, `res.json()`, and `res.end()` in Express?**
> **A:** 
> - `res.send()` sends the HTTP response and automatically sets the `Content-Type` header based on the data passed (e.g., HTML, Buffer, String).
> - `res.json()` specifically formats the given data as a JSON string (using `JSON.stringify()`) and sets the `Content-Type` to `application/json`.
> - `res.end()` ends the response process quickly without sending any data. It's often used for quick 404s or status updates.

**16. Q: How do you handle CORS in Express?**
> **A:** CORS (Cross-Origin Resource Sharing) is a security feature implemented by browsers. In Express, you handle it by using the `cors` middleware package (`npm install cors`). You simply add `app.use(cors())` to allow your API to be accessed from frontends hosted on different domains/ports.

**17. Q: What are Streams in Node.js?**
> **A:** Streams are objects that let you read data from a source or write data to a destination in continuous chunks, rather than loading the entire data payload into memory at once. They are highly efficient for handling large files, like video streaming or parsing huge CSVs.

**18. Q: What is a REST API?**
> **A:** REST (Representational State Transfer) is an architectural style for designing networked applications. A REST API relies on stateless, client-server communication using standard HTTP methods (GET, POST, PUT, DELETE) where resources are identified by URLs (e.g., `/users/123`) and data is typically exchanged in JSON format.

**19. Q: How do you perform validation in Mongoose?**
> **A:** Mongoose handles validation at the Schema level. You can use built-in validators like `required: true`, `min`, `max`, `enum`, or `match` (for regex). You can also define custom validator functions. Validation runs automatically when you call `.save()` or explicitly via `runValidators: true` during updates.

**20. Q: What is `mongoose.Schema.Types.ObjectId`?**
> **A:** It is a special data type in Mongoose used to store the unique 12-byte identifier (`_id`) generated by MongoDB. It is heavily used to create relationships (Foreign Keys) between different collections, utilizing the `ref` property to populate related documents.

**21. Q: What are Mongoose Hooks (Middleware)?**
> **A:** Mongoose hooks (also called middleware) are functions that execute before (`pre`) or after (`post`) specific Mongoose actions like `save`, `update`, `remove`, or `validate`. They are highly useful for tasks like hashing passwords before saving a user or cascading deletes.

**22. Q: What is the purpose of `.env` files?**
> **A:** A `.env` file is used to store environment variables—sensitive configuration data like database connection strings, API keys, and secret tokens. This keeps sensitive data out of the source code (it shouldn't be pushed to GitHub) and allows different configurations for development, testing, and production environments. We typically use the `dotenv` package to load them.

**23. Q: Explain the difference between `dependencies` and `devDependencies` in package.json.**
> **A:** 
> - `dependencies` are packages required for the application to run in production (e.g., `express`, `mongoose`). 
> - `devDependencies` are packages only needed during local development and testing (e.g., `nodemon`, `jest`). They are not installed in production environments to save space and reduce security risks.

**24. Q: What is `nodemon`?**
> **A:** `nodemon` is a utility tool for Node.js developers. It monitors your project directory for any file changes and automatically restarts the server when a change is detected, saving you from having to manually stop and start the server after every code edit.

**25. Q: What is the difference between `module.exports` and `exports`?**
> **A:** In Node.js, `module.exports` is the actual object that gets returned by a `require()` call. `exports` is initially just a shorthand reference pointing to `module.exports`. If you assign a completely new object to `exports`, it breaks the reference, so you must attach properties to it (e.g., `exports.myFunc = ...`) or directly assign to `module.exports`.

---

## ⚡ Section 7 — Quick Revision Cheatsheet

### 🟢 Express.js Methods
| Method | Description | Example |
|---|---|---|
| `express()` | Initializes an Express application. | `const app = express();` |
| `app.listen()` | Starts the server on a specified port. | `app.listen(3000, () => ...)` |
| `app.use()` | Mounts middleware functions or routers. | `app.use(express.json());` |
| `app.get()`, `app.post()` | Defines route handlers for specific HTTP methods. | `app.get('/users', (req, res) => ...)` |
| `express.Router()` | Creates modular, mountable route handlers. | `const router = express.Router();` |

### 📥 Request (`req`) Object
| Property | Description | Example URL / Usage |
|---|---|---|
| `req.body` | Contains key-value pairs of data submitted in the request body (requires `express.json()`). | `POST /users` → `req.body.name` |
| `req.params` | Contains route parameters (variables embedded in the URL path). | `GET /users/5` → `req.params.id` |
| `req.query` | Contains the URL query string parameters. | `GET /users?sort=asc` → `req.query.sort` |

### 📤 Response (`res`) Object
| Method | Description | Example |
|---|---|---|
| `res.send()` | Sends the HTTP response (HTML, Buffer, etc.). | `res.send('Hello World');` |
| `res.json()` | Sends a JSON response (automatically sets Content-Type). | `res.json({ success: true });` |
| `res.status()` | Sets the HTTP status code for the response. Can be chained. | `res.status(404).json(...);` |
| `res.redirect()` | Redirects to a specified URL. | `res.redirect('/home');` |

### 🍃 Mongoose Setup & Models
| Method / Syntax | Description | Example |
|---|---|---|
| `mongoose.connect()` | Connects to a MongoDB database. | `mongoose.connect('mongodb://localhost/db')` |
| `new mongoose.Schema()` | Defines the structure, data types, and validations. | `new mongoose.Schema({ name: String })` |
| `mongoose.model()` | Compiles a Schema into a Model to interact with DB. | `mongoose.model('User', userSchema)` |

### 🔎 Mongoose Queries (Read)
| Method | Description | Example |
|---|---|---|
| `Model.find()` | Finds all documents matching the criteria. | `await User.find({ age: { $gte: 18 } })` |
| `Model.findById()` | Finds a single document by its `_id`. | `await User.findById(req.params.id)` |
| `Model.findOne()` | Finds the first document matching the criteria. | `await User.findOne({ email: 'x@y.com' })` |
| `.populate()` | Replaces a specified path (ObjectId) with document(s) from other collections. | `Issue.find().populate('book')` |

### ➕ Mongoose Create & Save
| Method | Description | Example |
|---|---|---|
| `new Model()` | Creates a new instance of a document in memory. | `const user = new User(req.body);` |
| `.save()` | Saves the document instance to the database. | `await user.save();` |
| `Model.create()` | Shortcut: creates and saves a document in one step. | `await User.create(req.body);` |

### ✏️ Mongoose Update
| Method | Description | Example |
|---|---|---|
| `Model.findByIdAndUpdate()` | Finds a document by ID and updates it. Passing `{ new: true }` returns the updated doc. | `User.findByIdAndUpdate(id, data, {new: true})` |
| `Model.updateOne()` | Updates the first document that matches the filter. | `User.updateOne({name: 'Bob'}, {age: 30})` |
| `doc.property = new_val` | You can mutate a fetched document manually, then call `.save()`. | `user.age = 30; await user.save();` |

### 🗑️ Mongoose Delete
| Method | Description | Example |
|---|---|---|
| `Model.findByIdAndDelete()` | Finds a document by ID, deletes it, and returns it. | `await User.findByIdAndDelete(req.params.id)` |
| `Model.deleteOne()` | Deletes the first document that matches the filter. | `await User.deleteOne({ email: 'x@y.com' })` |
