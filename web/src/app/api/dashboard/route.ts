import { NextResponse } from 'next/server'
import { AnalyticsService } from '@/lib/services/database'

// GET /api/dashboard - Get dashboard data
export async function GET() {
  try {
    const dashboardData = await AnalyticsService.getDashboardData()
    return NextResponse.json(dashboardData)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    return NextResponse.json(
      { error: 'Failed to fetch dashboard data' },
      { status: 500 }
    )
  }
}