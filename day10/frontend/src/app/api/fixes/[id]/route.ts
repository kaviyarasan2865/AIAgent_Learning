import dbConnect from '@/lib/db';
import Fix from '@/models/Fix';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  await dbConnect();
  const fixes = await Fix.find({ issue: params.id });
  return NextResponse.json(fixes);
}