# 📚 Library Management REST API (Express + MongoDB)

This is the backend-only REST API implementation of the Library Management System. There is no frontend (HTML/EJS). Data is exchanged purely in **JSON format**, making it perfect for testing via Postman or integrating with a React/Angular frontend.

---

## 🚀 Setup & Run Instructions

```bash
# 1. Ensure you have Node.js and MongoDB installed on your system.
# Start your local MongoDB server if it's not running automatically.

# 2. Open this folder in terminal and install dependencies
npm install

# 3. Start the server
npm start
# Expected Output:
# 🚀 REST API Server running on http://localhost:3000
# ✅ Connected to MongoDB
```

---

## 📖 Line-by-Line Code Breakdown

### 📄 `app.js` (The Entry Point)
```javascript
const express = require('express');
// Imports the Express framework to create our server.

const mongoose = require('mongoose');
// Imports Mongoose, the ODM library used to interact with MongoDB.

const libraryRoutes = require('./routes/library');
// Imports all our defined API routes from the library.js file.

const app = express();
// Initializes an Express application instance.

const PORT = 3000;
// Defines the port number the server will listen on.

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/express_library', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
// Attempts to connect to a local MongoDB instance.
// 'express_library' is the name of the database (created automatically if it doesn't exist).
// useNewUrlParser & useUnifiedTopology are options to prevent deprecation warnings in older Mongoose versions.
.then(() => console.log('✅ Connected to MongoDB'))
// If the promise resolves, it logs a success message.
.catch(err => console.error('❌ MongoDB connection error:', err));
// If the promise rejects (e.g., MongoDB isn't running), it logs the error.

// Middleware to parse incoming JSON payloads
app.use(express.json());
// Crucial Middleware! It intercepts incoming requests, checks if they contain a JSON body,
// parses the JSON, and attaches it to the `req.body` object.

// Routes
app.use('/api', libraryRoutes);
// Mounts our router. All routes inside `libraryRoutes` will now be prefixed with '/api'.
// Example: The `/books` route becomes `/api/books`.

// Start server
app.listen(PORT, () => {
    console.log(`🚀 REST API Server running on http://localhost:${PORT}`);
});
// Starts the HTTP server and listens for incoming connections on port 3000.
```

---

### 📄 `models/Book.js`
```javascript
const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
    // new mongoose.Schema defines the structure of our documents.
    title: { type: String, required: true },
    // 'title' must be a string and is mandatory (required: true).
    author: { type: String, required: true },
    isbn: { type: String, required: true, unique: true },
    // 'isbn' must be unique. No two books can have the same ISBN.
    total_copies: { type: Number, default: 1, min: 1 },
    // Defaults to 1 copy. 'min: 1' ensures we can't have 0 or negative total copies.
    available_copies: { type: Number, default: 1, min: 0 }
    // Defaults to 1. 'min: 0' ensures we never have negative available copies.
});

// Instance Method
bookSchema.methods.isAvailable = function() {
    return this.available_copies > 0;
};
// Adds a custom function to every Book document.
// We call `book.isAvailable()` to easily check if it's in stock.

module.exports = mongoose.model('Book', bookSchema);
// Compiles the schema into a Model named 'Book' and exports it.
// MongoDB will automatically create a collection named 'books' (lowercase, plural).
```

---

### 📄 `models/IssueRecord.js`
```javascript
const mongoose = require('mongoose');

const issueRecordSchema = new mongoose.Schema({
    book: { type: mongoose.Schema.Types.ObjectId, ref: 'Book', required: true },
    // This is a FOREIGN KEY equivalent. It stores the unique `_id` of a Book document.
    // `ref: 'Book'` tells Mongoose which model this ID belongs to, enabling the `.populate()` method.
    member: { type: mongoose.Schema.Types.ObjectId, ref: 'Member', required: true },
    // Stores the unique `_id` of a Member document.
    issue_date: { type: Date, default: Date.now },
    // Automatically sets the issue date to the exact moment the record is created.
    due_date: { type: Date, required: true },
    // The date the book must be returned.
    return_date: { type: Date },
    // Optional field. It remains undefined until the book is actually returned.
    returned: { type: Boolean, default: false }
    // A flag to track status. Defaults to false (not returned).
});

module.exports = mongoose.model('IssueRecord', issueRecordSchema);
```

---

### 📄 `routes/library.js` (Core API Logic)
```javascript
const express = require('express');
const router = express.Router();
// Creates a modular route handler.

const Book = require('../models/Book');
const Member = require('../models/Member');
const IssueRecord = require('../models/IssueRecord');
// Imports our 3 Mongoose models to interact with the DB.

// ========================
// BOOKS CRUD
// ========================

// GET /api/books - Get all books
router.get('/books', async (req, res) => {
    try {
        const books = await Book.find();
        // Awaits the DB query to fetch all documents in the 'books' collection.
        res.status(200).json(books);
        // Sends back a 200 OK status along with the array of books in JSON format.
    } catch (err) {
        res.status(500).json({ error: err.message });
        // If the DB crashes, catch the error and send a 500 Internal Server Error.
    }
});

// POST /api/books - Add a new book
router.post('/books', async (req, res) => {
    try {
        const newBook = new Book(req.body);
        // Creates a new Book instance in memory using the JSON data sent in `req.body`.
        const savedBook = await newBook.save();
        // Awaits the actual save operation to the database.
        res.status(201).json(savedBook);
        // Sends back 201 Created and the newly created book object (including its generated `_id`).
    } catch (err) {
        res.status(400).json({ error: err.message });
        // Sends 400 Bad Request if validation fails (e.g., missing title).
    }
});

// ... (Other standard CRUD routes for Members and Books follow the exact same pattern) ...

// ========================
// ISSUE / RETURN LOGIC
// ========================

// POST /api/issues - Issue a book to a member
router.post('/issues', async (req, res) => {
    try {
        const { book, member, due_date } = req.body;
        // Destructures the book ID, member ID, and due date from the incoming JSON.
        
        const bookData = await Book.findById(book);
        // Fetches the specific book document from the database using its ID.
        if (!bookData) return res.status(404).json({ message: 'Book not found' });
        // If the ID is invalid, abort and return 404.
        
        if (!bookData.isAvailable()) {
            return res.status(400).json({ message: 'Book is currently out of stock!' });
        }
        // Uses our custom schema method to check if available_copies > 0.
        // If out of stock, abort and return 400 Bad Request.

        const newIssue = new IssueRecord({ book, member, due_date });
        const savedIssue = await newIssue.save();
        // Creates and saves the new issue record.
        
        bookData.available_copies -= 1;
        // Decrements the available copies count of the book in memory.
        await bookData.save();
        // Saves the updated book document back to the database.

        res.status(201).json(savedIssue);
        // Returns the created issue record.
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// PUT /api/issues/:id/return - Return a book
router.put('/issues/:id/return', async (req, res) => {
    try {
        const issue = await IssueRecord.findById(req.params.id).populate('book');
        // Fetches the issue record by URL parameter ID.
        // `.populate('book')` tells Mongoose to replace the `book` ObjectId with the ACTUAL Book document data.
        // This allows us to access `issue.book.available_copies` directly!
        
        if (!issue) return res.status(404).json({ message: 'Issue record not found' });
        if (issue.returned) return res.status(400).json({ message: 'Book is already returned' });
        // Prevents returning the same book twice.

        issue.returned = true;
        issue.return_date = Date.now();
        await issue.save();
        // Updates the issue record to indicate it has been returned.

        issue.book.available_copies += 1;
        await issue.book.save();
        // Since we used `.populate()`, `issue.book` is a fully functional Mongoose document.
        // We increment the copies and save the related book back to the DB.

        res.status(200).json({ message: 'Book returned successfully', issue });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// GET /api/issues/overdue - Get all overdue books
router.get('/issues/overdue', async (req, res) => {
    try {
        const today = new Date();
        const overdueIssues = await IssueRecord.find({
            returned: false,
            due_date: { $lt: today } 
            // MongoDB Query Operator: $lt stands for "Less Than".
            // We want records where due_date is strictly older than `today`.
        }).populate('book').populate('member');
        // Replaces both object IDs with actual book and member data for a rich JSON response.

        res.status(200).json(overdueIssues);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});
```

---

## 🧪 Postman Testing Guide

Open Postman and follow these steps to test the entire flow:

### 1. Add a Book
- **Method:** `POST`
- **URL:** `http://localhost:3000/api/books`
- **Headers:** `Content-Type: application/json`
- **Body (raw):**
  ```json
  {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "9780132350884",
    "total_copies": 3,
    "available_copies": 3
  }
  ```
- **Action:** Click Send. *Copy the `_id` from the response (e.g., `64f1a...`). We'll call this `BOOK_ID`.*

### 2. Add a Member
- **Method:** `POST`
- **URL:** `http://localhost:3000/api/members`
- **Body (raw):**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210"
  }
  ```
- **Action:** Click Send. *Copy the `_id` from the response. We'll call this `MEMBER_ID`.*

### 3. Issue the Book to the Member
- **Method:** `POST`
- **URL:** `http://localhost:3000/api/issues`
- **Body (raw):**
  ```json
  {
    "book": "PASTE_BOOK_ID_HERE",
    "member": "PASTE_MEMBER_ID_HERE",
    "due_date": "2023-12-01T00:00:00Z" 
  }
  ```
- **Action:** Click Send. You should get a 201 Created response. *Copy the `_id` of this issue record. We'll call this `ISSUE_ID`.*
- **Verify:** Make a `GET` request to `http://localhost:3000/api/books`. You will see the `available_copies` has dropped from 3 to 2.

### 4. Check Overdue Books
- **Method:** `GET`
- **URL:** `http://localhost:3000/api/issues/overdue`
- **Action:** Click Send. If you used the past due date (`2023-12-01`) from step 3, the issue record will show up here as it hasn't been returned yet!

### 5. Return the Book
- **Method:** `PUT`
- **URL:** `http://localhost:3000/api/issues/PASTE_ISSUE_ID_HERE/return`
- **Action:** Click Send. 
- **Verify:** Make a `GET` request to `http://localhost:3000/api/books`. You will see `available_copies` is back to 3!
