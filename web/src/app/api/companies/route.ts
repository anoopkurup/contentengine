import { NextRequest, NextResponse } from 'next/server'
import { CompanyService } from '@/lib/services/database'
import { CreateCompanyRequest } from '@/lib/types'

// GET /api/companies - List all companies
export async function GET() {
  try {
    const companies = await CompanyService.listCompanies()
    return NextResponse.json(companies)
  } catch (error) {
    console.error('Error fetching companies:', error)
    return NextResponse.json(
      { error: 'Failed to fetch companies' },
      { status: 500 }
    )
  }
}

// POST /api/companies - Create new company
export async function POST(request: NextRequest) {
  try {
    const body: CreateCompanyRequest = await request.json()
    
    // Validate required fields
    if (!body.name) {
      return NextResponse.json(
        { error: 'Company name is required' },
        { status: 400 }
      )
    }

    const company = await CompanyService.createCompany(body)
    return NextResponse.json(company, { status: 201 })
  } catch (error) {
    console.error('Error creating company:', error)
    return NextResponse.json(
      { error: 'Failed to create company' },
      { status: 500 }
    )
  }
}