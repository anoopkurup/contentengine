import { NextRequest, NextResponse } from 'next/server'
import { ProjectService } from '@/lib/services/database'
import { CreateProjectRequest } from '@/lib/types'

// GET /api/projects - List projects (optionally filtered by company_id)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const companyId = searchParams.get('company_id')
    
    const projects = await ProjectService.listProjects(companyId || undefined)
    return NextResponse.json(projects)
  } catch (error) {
    console.error('Error fetching projects:', error)
    return NextResponse.json(
      { error: 'Failed to fetch projects' },
      { status: 500 }
    )
  }
}

// POST /api/projects - Create new project
export async function POST(request: NextRequest) {
  try {
    const body: CreateProjectRequest = await request.json()
    
    // Validate required fields
    if (!body.name || !body.companyId) {
      return NextResponse.json(
        { error: 'Project name and company ID are required' },
        { status: 400 }
      )
    }

    const project = await ProjectService.createProject(body)
    return NextResponse.json(project, { status: 201 })
  } catch (error) {
    console.error('Error creating project:', error)
    return NextResponse.json(
      { error: 'Failed to create project' },
      { status: 500 }
    )
  }
}