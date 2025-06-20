import dbConnect from '@/lib/db';
import Issue from '@/models/Issue';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  await dbConnect();
  const issues = await Issue.find({ codeSubmission: params.id });
  return NextResponse.json(issues);
}