import dbConnect from '@/lib/db';
import Approval from '@/models/Approval';
import FixedCode from '@/models/FixedCode';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  await dbConnect();
  const { codeSubmissionId, approved, user, html_fixed, css_fixed, js_fixed } = await req.json();
  const approval = await Approval.create({ codeSubmission: codeSubmissionId, approved, user });

  // Save fixed code if approved
  if (approved && html_fixed && css_fixed && js_fixed) {
    await FixedCode.create({
      html: html_fixed,
      css: css_fixed,
      js: js_fixed,
      approved: true
    });
  }

  return NextResponse.json(approval);
}