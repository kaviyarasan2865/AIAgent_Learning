import dbConnect from '@/lib/db';
import Approval from '@/models/Approval';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  await dbConnect();
  const { codeSubmissionId, approved, user } = await req.json();
  const approval = await Approval.create({ codeSubmission: codeSubmissionId, approved, user });
  return NextResponse.json(approval);
}