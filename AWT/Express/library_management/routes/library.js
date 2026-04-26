const express = require('express');
const router = express.Router();
const Book = require('../models/Book');
const Member = require('../models/Member');
const IssueRecord = require('../models/IssueRecord');

// ========================
// BOOKS CRUD
// ========================
// GET /api/books - Get all books
router.get('/books', async (req, res) => {
    try {
        const books = await Book.find();
        res.status(200).json(books);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// POST /api/books - Add a new book
router.post('/books', async (req, res) => {
    try {
        const newBook = new Book(req.body);
        const savedBook = await newBook.save();
        res.status(201).json(savedBook);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// DELETE /api/books/:id - Delete a book
router.delete('/books/:id', async (req, res) => {
    try {
        const deletedBook = await Book.findByIdAndDelete(req.params.id);
        if (!deletedBook) return res.status(404).json({ message: 'Book not found' });
        res.status(200).json({ message: 'Book deleted successfully' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


// ========================
// MEMBERS CRUD
// ========================
// GET /api/members - Get all members
router.get('/members', async (req, res) => {
    try {
        const members = await Member.find();
        res.status(200).json(members);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// POST /api/members - Add a new member
router.post('/members', async (req, res) => {
    try {
        const newMember = new Member(req.body);
        const savedMember = await newMember.save();
        res.status(201).json(savedMember);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// DELETE /api/members/:id - Delete a member
router.delete('/members/:id', async (req, res) => {
    try {
        const deletedMember = await Member.findByIdAndDelete(req.params.id);
        if (!deletedMember) return res.status(404).json({ message: 'Member not found' });
        res.status(200).json({ message: 'Member deleted successfully' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


// ========================
// ISSUE / RETURN LOGIC
// ========================
// GET /api/issues - Get all issue records
router.get('/issues', async (req, res) => {
    try {
        const issues = await IssueRecord.find().populate('book').populate('member');
        res.status(200).json(issues);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// POST /api/issues - Issue a book to a member
router.post('/issues', async (req, res) => {
    try {
        const { book, member, due_date } = req.body;
        
        // Find the book to check availability
        const bookData = await Book.findById(book);
        if (!bookData) return res.status(404).json({ message: 'Book not found' });
        
        // Check Availability using instance method
        if (!bookData.isAvailable()) {
            return res.status(400).json({ message: 'Book is currently out of stock!' });
        }

        // Create Issue Record
        const newIssue = new IssueRecord({ book, member, due_date });
        const savedIssue = await newIssue.save();
        
        // Decrement available copies
        bookData.available_copies -= 1;
        await bookData.save();

        res.status(201).json(savedIssue);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
});

// PUT /api/issues/:id/return - Return a book
router.put('/issues/:id/return', async (req, res) => {
    try {
        const issue = await IssueRecord.findById(req.params.id).populate('book');
        
        if (!issue) return res.status(404).json({ message: 'Issue record not found' });
        if (issue.returned) return res.status(400).json({ message: 'Book is already returned' });

        // Mark as returned
        issue.returned = true;
        issue.return_date = Date.now();
        await issue.save();

        // Increment available copies
        issue.book.available_copies += 1;
        await issue.book.save();

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
            due_date: { $lt: today } // due_date is Less Than today
        }).populate('book').populate('member');

        res.status(200).json(overdueIssues);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// GET /api/members/:id/books - Get books issued by a specific member
router.get('/members/:id/books', async (req, res) => {
    try {
        const issues = await IssueRecord.find({ member: req.params.id }).populate('book');
        res.status(200).json(issues);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
