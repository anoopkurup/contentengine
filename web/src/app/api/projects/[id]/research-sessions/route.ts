import { NextRequest, NextResponse } from 'next/server'
import { KeywordResearchService } from '@/lib/services/database'

// GET /api/projects/[id]/research-sessions - Get all research sessions for a project
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const sessions = await KeywordResearchService.getProjectResearchSessions(id)
    
    // Format sessions for API response
    const formattedSessions = sessions.map(session => ({
      id: session.id,
      broad_keyword: session.broadKeyword,
      status: session.status,
      created_at: session.createdAt.toISOString(),
      completed_at: session.completedAt?.toISOString() || null,
      total_keywords: session.totalKeywords,
      total_clusters: session.totalClusters
    }))

    return NextResponse.json(formattedSessions)
  } catch (error) {
    console.error('Error fetching research sessions:', error)
    return NextResponse.json(
      { error: 'Failed to fetch research sessions' },
      { status: 500 }
    )
  }
}