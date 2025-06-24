import mongoose from 'mongoose';
const ApprovalSchema = new mongoose.Schema({
  codeSubmission: { type: mongoose.Schema.Types.ObjectId, ref: 'CodeSubmission' },
  approved: Boolean,
  user: String,
  decisionAt: { type: Date, default: Date.now }
});
export default mongoose.models.Approval || mongoose.model('Approval', ApprovalSchema);