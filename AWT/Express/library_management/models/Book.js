const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
    title: { type: String, required: true },
    author: { type: String, required: true },
    isbn: { type: String, required: true, unique: true },
    total_copies: { type: Number, default: 1, min: 1 },
    available_copies: { type: Number, default: 1, min: 0 }
});

bookSchema.methods.isAvailable = function() {
    return this.available_copies > 0;
};

module.exports = mongoose.model('Book', bookSchema);
