import { NextResponse } from 'next/server'

// GET /api/health - Health check endpoint
export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'ContentEngine API',
    timestamp: new Date().toISOString()
  })
}