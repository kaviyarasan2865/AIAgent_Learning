import mongoose from 'mongoose';
const FixSchema = new mongoose.Schema({
  issue: { type: mongoose.Schema.Types.ObjectId, ref: 'Issue' },
  before: String,
  after: String,
  explanation: String,
  createdAt: { type: Date, default: Date.now }
});
export default mongoose.models.Fix || mongoose.model('Fix', FixSchema);