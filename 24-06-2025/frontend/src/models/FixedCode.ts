import mongoose, { Schema, Document } from 'mongoose';

export interface IFixedCode extends Document {
  html: string;
  css: string;
  js: string;
  approved: boolean;
  createdAt: Date;
}

const FixedCodeSchema = new Schema<IFixedCode>({
  html: { type: String, required: true },
  css: { type: String, required: true },
  js: { type: String, required: true },
  approved: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now }
});

export default mongoose.models.FixedCode || mongoose.model<IFixedCode>('FixedCode', FixedCodeSchema);