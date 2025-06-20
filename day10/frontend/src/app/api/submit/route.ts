import dbConnect from '@/lib/db';
import CodeSubmission from '@/models/CodeSubmission';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  await dbConnect();
  const { html, css, javascript } = await req.json();
  const submission = await CodeSubmission.create({ html, css, javascript });
  // Call your Python backend here and store issues/fixes as needed
  return NextResponse.json({ id: submission._id });
}