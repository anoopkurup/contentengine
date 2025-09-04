// TypeScript types for ContentEngine application

export interface Company {
  id: string
  name: string
  description: string | null
  searchSettings: SearchSettings | null
  contentSettings: ContentSettings | null
  brandSettings: BrandSettings | null
  seoSettings: SeoSettings | null
  createdAt: Date
  updatedAt: Date
}

export interface Project {
  id: string
  companyId: string
  name: string
  description: string | null
  broadKeyword: string | null
  status: 'active' | 'completed' | 'paused'
  config: Record<string, any> | null
  createdAt: Date
  updatedAt: Date
}

export interface KeywordResearchSession {
  id: string
  projectId: string
  broadKeyword: string
  researchSettings: ResearchSettings | null
  totalKeywords: number
  totalClusters: number
  status: 'pending' | 'running' | 'completed' | 'failed'
  errorMessage: string | null
  createdAt: Date
  completedAt: Date | null
}

export interface KeywordCluster {
  id: string
  sessionId: string
  clusterName: string
  pillarKeyword: string | null
  keywordsCount: number
  totalSearchVolume: number
  avgSearchVolume: number
  avgCompetition: number
  createdAt: Date
}

export interface Keyword {
  id: string
  clusterId: string
  keyword: string
  searchVolume: number
  competition: number
  role: string | null // 'Pillar Post' or 'Cluster Post'
  serpUrls: Record<string, any> | null
  createdAt: Date
}

export interface PipelineStage {
  id: string
  projectId: string
  stageName: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  startedAt: Date | null
  completedAt: Date | null
  errorMessage: string | null
  outputData: Record<string, any> | null
  createdAt: Date
  updatedAt: Date
}

// Settings interfaces
export interface SearchSettings {
  targetLocation?: string
  targetLanguage?: string
  minSearchVolume?: number
  maxCompetition?: number
  serpOverlapThreshold?: number
  keywordExpansionLimit?: number
}

export interface ContentSettings {
  brandVoice?: string
  writingStyle?: string
  targetAudience?: string
  contentGuidelines?: string[]
}

export interface BrandSettings {
  brandVoice?: string
  writingStyle?: string
  targetAudience?: string
  contentGuidelines?: string[]
}

export interface SeoSettings {
  targetLocation?: string
  targetLanguage?: string
  minSearchVolume?: number
  maxCompetition?: number
}

export interface ResearchSettings {
  targetLocation?: string
  targetLanguage?: string
  minSearchVolume?: number
  maxCompetition?: number
  serpOverlapThreshold?: number
  keywordExpansionLimit?: number
}

// API Request/Response types
export interface CreateCompanyRequest {
  name: string
  description?: string
  searchSettings?: SearchSettings
  contentSettings?: ContentSettings
  brandSettings?: BrandSettings
  seoSettings?: SeoSettings
}

export interface UpdateCompanyRequest {
  name?: string
  description?: string
  searchSettings?: SearchSettings
  contentSettings?: ContentSettings
  brandSettings?: BrandSettings
  seoSettings?: SeoSettings
}

export interface CreateProjectRequest {
  companyId: string
  name: string
  description?: string
  broadKeyword?: string
  config?: Record<string, any>
}

export interface KeywordResearchRequest {
  projectId: string
  broadKeyword: string
  researchSettings: ResearchSettings
}

export interface DashboardData {
  stats: {
    totalCompanies: number
    totalProjects: number
    activeProjects: number
    completedProjects: number
  }
  recentProjects: Array<{
    id: string
    name: string
    description: string | null
    broadKeyword: string | null
    createdAt: string
    completion: number
  }>
}

// DataForSEO API types
export interface DataForSEOKeyword {
  keyword: string
  search_volume: number
  competition: number | string
}

export interface DataForSEOSerpItem {
  url: string
  title?: string
  description?: string
  position?: number
}

export interface KeywordClusterResult {
  Cluster: string
  'Pillar Keyword': string
  'Keywords in Cluster': number
  'Avg Search Volume': number
  'Total Search Volume': number
  'Avg Competition': number
}

export interface KeywordResult {
  Cluster: string
  Keyword: string
  'Search Volume': number
  Competition: number
  Role: string
}