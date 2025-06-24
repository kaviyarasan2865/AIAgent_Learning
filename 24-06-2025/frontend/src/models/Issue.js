import mongoose from 'mongoose';
const IssueSchema = new mongoose.Schema({
  codeSubmission: { type: mongoose.Schema.Types.ObjectId, ref: 'CodeSubmission' },
  agent: String,
  type: String,
  description: String,
  location: String,
  severity: String,
  createdAt: { type: Date, default: Date.now }
});
export default mongoose.models.Issue || mongoose.model('Issue', IssueSchema);