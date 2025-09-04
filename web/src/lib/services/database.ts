/**
 * Database Service Layer
 * TypeScript replacement for Python database services
 */

import { db } from '@/lib/db'
import {
  Company,
  Project,
  KeywordResearchSession,
  CreateCompanyRequest,
  UpdateCompanyRequest,
  CreateProjectRequest,
  DashboardData
} from '@/lib/types'

export class CompanyService {
  /**
   * Create a new company
   */
  static async createCompany(data: CreateCompanyRequest): Promise<Company> {
    const company = await db.company.create({
      data: {
        name: data.name,
        description: data.description || null,
        searchSettings: data.searchSettings || null,
        contentSettings: data.contentSettings || null,
        brandSettings: data.brandSettings || null,
        seoSettings: data.seoSettings || null
      }
    })

    // Map database fields to API field names
    return {
      id: company.id,
      name: company.name,
      description: company.description,
      created_at: company.createdAt.toISOString(),
      search_settings: company.searchSettings,
      content_settings: company.contentSettings,
      brand_settings: company.brandSettings,
      seo_settings: company.seoSettings
    }
  }

  /**
   * Get company by ID
   */
  static async getCompany(id: string): Promise<Company | null> {
    const company = await db.company.findUnique({
      where: { id }
    })
    
    if (!company) return null
    
    // Map database fields to API field names
    return {
      id: company.id,
      name: company.name,
      description: company.description,
      created_at: company.createdAt.toISOString(),
      search_settings: company.searchSettings,
      content_settings: company.contentSettings,
      brand_settings: company.brandSettings,
      seo_settings: company.seoSettings
    }
  }

  /**
   * List all companies
   */
  static async listCompanies(): Promise<Company[]> {
    const companies = await db.company.findMany({
      orderBy: { createdAt: 'desc' }
    })
    
    // Map database fields to API field names
    return companies.map(company => ({
      id: company.id,
      name: company.name,
      description: company.description,
      created_at: company.createdAt.toISOString(),
      search_settings: company.searchSettings,
      content_settings: company.contentSettings,
      brand_settings: company.brandSettings,
      seo_settings: company.seoSettings
    }))
  }

  /**
   * Update company
   */
  static async updateCompany(id: string, data: UpdateCompanyRequest): Promise<Company> {
    const company = await db.company.update({
      where: { id },
      data: {
        ...(data.name && { name: data.name }),
        ...(data.description !== undefined && { description: data.description }),
        ...(data.searchSettings && { searchSettings: data.searchSettings }),
        ...(data.contentSettings && { contentSettings: data.contentSettings }),
        ...(data.brandSettings && { brandSettings: data.brandSettings }),
        ...(data.seoSettings && { seoSettings: data.seoSettings })
      }
    })

    // Map database fields to API field names
    return {
      id: company.id,
      name: company.name,
      description: company.description,
      created_at: company.createdAt.toISOString(),
      search_settings: company.searchSettings,
      content_settings: company.contentSettings,
      brand_settings: company.brandSettings,
      seo_settings: company.seoSettings
    }
  }

  /**
   * Delete company
   */
  static async deleteCompany(id: string): Promise<void> {
    await db.company.delete({
      where: { id }
    })
  }
}

export class ProjectService {
  /**
   * Create a new project
   */
  static async createProject(data: CreateProjectRequest): Promise<Project> {
    const project = await db.project.create({
      data: {
        companyId: data.companyId,
        name: data.name,
        description: data.description || null,
        broadKeyword: data.broadKeyword || null,
        config: data.config || null
      }
    })

    return project
  }

  /**
   * Get project by ID
   */
  static async getProject(id: string): Promise<Project | null> {
    return await db.project.findUnique({
      where: { id },
      include: {
        company: true
      }
    })
  }

  /**
   * List projects, optionally filtered by company
   */
  static async listProjects(companyId?: string): Promise<Project[]> {
    return await db.project.findMany({
      where: companyId ? { companyId } : undefined,
      orderBy: { createdAt: 'desc' },
      include: {
        company: true
      }
    })
  }

  /**
   * Update project
   */
  static async updateProject(id: string, data: Partial<CreateProjectRequest>): Promise<Project> {
    return await db.project.update({
      where: { id },
      data: {
        ...(data.name && { name: data.name }),
        ...(data.description !== undefined && { description: data.description }),
        ...(data.broadKeyword !== undefined && { broadKeyword: data.broadKeyword }),
        ...(data.config && { config: data.config })
      }
    })
  }

  /**
   * Delete project
   */
  static async deleteProject(id: string): Promise<void> {
    await db.project.delete({
      where: { id }
    })
  }
}

export class KeywordResearchService {
  /**
   * Create research session
   */
  static async createResearchSession(
    projectId: string,
    broadKeyword: string,
    researchSettings: any
  ): Promise<KeywordResearchSession> {
    return await db.keywordResearchSession.create({
      data: {
        projectId,
        broadKeyword,
        researchSettings,
        status: 'pending'
      }
    })
  }

  /**
   * Get research session by ID
   */
  static async getResearchSession(id: string): Promise<KeywordResearchSession | null> {
    return await db.keywordResearchSession.findUnique({
      where: { id },
      include: {
        project: true,
        clusters: {
          include: {
            keywords: true
          }
        }
      }
    })
  }

  /**
   * Get all research sessions for a project
   */
  static async getProjectResearchSessions(projectId: string): Promise<KeywordResearchSession[]> {
    return await db.keywordResearchSession.findMany({
      where: { projectId },
      orderBy: { createdAt: 'desc' },
      include: {
        clusters: true
      }
    })
  }

  /**
   * Update research session status
   */
  static async updateSessionStatus(
    id: string,
    status: 'pending' | 'running' | 'completed' | 'failed',
    errorMessage?: string
  ): Promise<KeywordResearchSession> {
    return await db.keywordResearchSession.update({
      where: { id },
      data: {
        status,
        ...(errorMessage && { errorMessage }),
        ...(status === 'completed' || status === 'failed') && { completedAt: new Date() }
      }
    })
  }

  /**
   * Get session results formatted for API
   */
  static async getSessionResults(sessionId: string): Promise<any> {
    const session = await db.keywordResearchSession.findUnique({
      where: { id: sessionId },
      include: {
        clusters: {
          include: {
            keywords: true
          }
        }
      }
    })

    if (!session) {
      return null
    }

    const clusterData = session.clusters.map(cluster => ({
      Cluster: cluster.clusterName,
      'Pillar Keyword': cluster.pillarKeyword || '',
      'Keywords in Cluster': cluster.keywordsCount,
      'Avg Search Volume': cluster.avgSearchVolume,
      'Total Search Volume': cluster.totalSearchVolume,
      'Avg Competition': cluster.avgCompetition
    }))

    const keywordData = []
    for (const cluster of session.clusters) {
      for (const keyword of cluster.keywords) {
        keywordData.push({
          Cluster: cluster.clusterName,
          Keyword: keyword.keyword,
          'Search Volume': keyword.searchVolume,
          Competition: keyword.competition,
          Role: keyword.role || ''
        })
      }
    }

    return {
      session: {
        id: session.id,
        projectId: session.projectId,
        broadKeyword: session.broadKeyword,
        status: session.status,
        createdAt: session.createdAt.toISOString(),
        completedAt: session.completedAt?.toISOString() || null,
        totalKeywords: session.totalKeywords,
        totalClusters: session.totalClusters,
        researchSettings: session.researchSettings
      },
      cluster_data: clusterData,
      keyword_data: keywordData,
      total_keywords: keywordData.length,
      total_clusters: clusterData.length
    }
  }
}

export class AnalyticsService {
  /**
   * Get project analytics
   */
  static async getProjectAnalytics(projectId: string): Promise<any> {
    const project = await db.project.findUnique({
      where: { id: projectId },
      include: {
        company: true,
        researchSessions: true
      }
    })

    if (!project) {
      return null
    }

    const sessionsCount = project.researchSessions.length
    const completedSessions = project.researchSessions.filter(s => s.status === 'completed')
    const totalKeywords = completedSessions.reduce((sum, s) => sum + s.totalKeywords, 0)
    const totalClusters = completedSessions.reduce((sum, s) => sum + s.totalClusters, 0)
    const latestSession = project.researchSessions[0] // Already ordered by date

    return {
      project,
      research_sessions: sessionsCount,
      total_keywords: totalKeywords,
      total_clusters: totalClusters,
      latest_session: latestSession
    }
  }

  /**
   * Get dashboard data
   */
  static async getDashboardData(): Promise<DashboardData> {
    const [companies, projects] = await Promise.all([
      db.company.count(),
      db.project.findMany({
        orderBy: { createdAt: 'desc' },
        take: 5,
        include: {
          researchSessions: {
            where: { status: 'completed' }
          }
        }
      })
    ])

    const totalProjects = await db.project.count()
    const activeProjects = await db.project.count({
      where: { status: 'active' }
    })
    const completedProjects = await db.project.count({
      where: { status: 'completed' }
    })

    const recentProjects = projects.map(project => ({
      id: project.id,
      name: project.name,
      description: project.description,
      broadKeyword: project.broadKeyword,
      createdAt: project.createdAt.toISOString(),
      completion: project.researchSessions.length > 0 ? 100 : 0 // Basic completion logic
    }))

    return {
      stats: {
        totalCompanies: companies,
        totalProjects,
        activeProjects,
        completedProjects
      },
      recentProjects
    }
  }
}