import { NextRequest, NextResponse } from 'next/server'
import { KeywordResearcher } from '@/lib/services/keywordResearcher'

// GET /api/keyword-research/[id] - Get keyword research results
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const researcher = new KeywordResearcher()
    const results = await researcher.getSessionResults(id)
    
    if (!results) {
      return NextResponse.json(
        { error: 'Research session not found' },
        { status: 404 }
      )
    }

    return NextResponse.json(results)
  } catch (error) {
    console.error('Error fetching research results:', error)
    return NextResponse.json(
      { error: 'Failed to fetch research results' },
      { status: 500 }
    )
  }
}