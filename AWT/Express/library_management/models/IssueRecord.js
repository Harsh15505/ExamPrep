const mongoose = require('mongoose');

const issueRecordSchema = new mongoose.Schema({
    book: { type: mongoose.Schema.Types.ObjectId, ref: 'Book', required: true },
    member: { type: mongoose.Schema.Types.ObjectId, ref: 'Member', required: true },
    issue_date: { type: Date, default: Date.now },
    due_date: { type: Date, required: true },
    return_date: { type: Date },
    returned: { type: Boolean, default: false }
});

module.exports = mongoose.model('IssueRecord', issueRecordSchema);
