import { NextRequest, NextResponse } from 'next/server'
import { KeywordResearcher } from '@/lib/services/keywordResearcher'
import { KeywordResearchRequest } from '@/lib/types'

// POST /api/keyword-research - Start keyword research
export async function POST(request: NextRequest) {
  try {
    const body: KeywordResearchRequest = await request.json()
    
    // Validate required fields
    if (!body.projectId || !body.broadKeyword) {
      return NextResponse.json(
        { error: 'Project ID and broad keyword are required' },
        { status: 400 }
      )
    }

    console.log(`Starting keyword research for project ${body.projectId} with keyword "${body.broadKeyword}"`)

    // Initialize keyword researcher
    const researcher = new KeywordResearcher()
    
    // Run keyword research (this is now automatic, not manual like before)
    const result = await researcher.runKeywordResearch(
      body.broadKeyword,
      body.researchSettings,
      body.projectId
    )

    if (result.success) {
      return NextResponse.json({
        session_id: result.sessionId,
        status: 'completed',
        message: 'Keyword research completed successfully!'
      })
    } else {
      return NextResponse.json(
        { 
          error: result.error || 'Keyword research failed',
          status: 'failed'
        },
        { status: 500 }
      )
    }

  } catch (error) {
    console.error('Error starting keyword research:', error)
    return NextResponse.json(
      { error: 'Failed to start keyword research' },
      { status: 500 }
    )
  }
}