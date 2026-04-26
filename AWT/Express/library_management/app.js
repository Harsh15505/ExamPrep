const express = require('express');
const mongoose = require('mongoose');
const libraryRoutes = require('./routes/library');

const app = express();
const PORT = 3000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/express_library', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log('✅ Connected to MongoDB'))
.catch(err => console.error('❌ MongoDB connection error:', err));

// Middleware to parse incoming JSON payloads
app.use(express.json());

// Routes
// We mount all routes under the /api prefix
app.use('/api', libraryRoutes);

// Start server
app.listen(PORT, () => {
    console.log(`🚀 REST API Server running on http://localhost:${PORT}`);
});
