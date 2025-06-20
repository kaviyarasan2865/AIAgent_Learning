import mongoose from 'mongoose';
const CodeSubmissionSchema = new mongoose.Schema({
  html: String,
  css: String,
  javascript: String,
  createdAt: { type: Date, default: Date.now }
});
export default mongoose.models.CodeSubmission || mongoose.model('CodeSubmission', CodeSubmissionSchema);