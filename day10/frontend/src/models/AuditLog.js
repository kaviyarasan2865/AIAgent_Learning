import mongoose from 'mongoose';
const AuditLogSchema = new mongoose.Schema({
  action: String,
  details: mongoose.Schema.Types.Mixed,
  user: String,
  createdAt: { type: Date, default: Date.now }
});
export default mongoose.models.AuditLog || mongoose.model('AuditLog', AuditLogSchema);