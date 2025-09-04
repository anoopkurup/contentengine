// API client for ContentEngine - now using Next.js API routes
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

export interface Company {
  id: string;
  name: string;
  description: string;
  created_at: string;
  search_settings: Record<string, any>;
  content_settings: Record<string, any>;
  brand_settings: Record<string, any>;
  seo_settings: Record<string, any>;
}

export interface Project {
  id: string;
  company_id: string;
  name: string;
  description: string;
  broad_keyword: string;
  created_at: string;
  config: Record<string, any>;
}

export interface DashboardData {
  stats: {
    totalCompanies: number;
    totalProjects: number;
    activeProjects: number;
    completedProjects: number;
  };
  recentProjects: Array<{
    id: string;
    name: string;
    description: string;
    broadKeyword: string;
    createdAt: string;
    completion: number;
  }>;
}

export interface KeywordResearchRequest {
  projectId: string;
  broadKeyword: string;
  researchSettings: Record<string, any>;
}

class ContentEngineAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  // Dashboard
  async getDashboardData(): Promise<DashboardData> {
    return this.request<DashboardData>('/api/dashboard');
  }

  // Companies
  async getCompanies(): Promise<Company[]> {
    return this.request<Company[]>('/api/companies');
  }

  async getCompany(id: string): Promise<Company> {
    return this.request<Company>(`/api/companies/${id}`);
  }

  async createCompany(data: {
    name: string;
    description?: string;
    search_settings?: Record<string, any>;
    content_settings?: Record<string, any>;
    brand_settings?: Record<string, any>;
    seo_settings?: Record<string, any>;
  }): Promise<Company> {
    return this.request<Company>('/api/companies', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCompany(id: string, data: {
    name?: string;
    description?: string;
    search_settings?: Record<string, any>;
    content_settings?: Record<string, any>;
    brand_settings?: Record<string, any>;
    seo_settings?: Record<string, any>;
  }): Promise<Company> {
    return this.request<Company>(`/api/companies/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Projects
  async getProjects(companyId?: string): Promise<Project[]> {
    const params = companyId ? `?company_id=${encodeURIComponent(companyId)}` : '';
    return this.request<Project[]>(`/api/projects${params}`);
  }

  async getProject(id: string): Promise<Project> {
    return this.request<Project>(`/api/projects/${id}`);
  }

  async createProject(data: {
    companyId: string;
    name: string;
    description?: string;
    broadKeyword?: string;
    config?: Record<string, any>;
  }): Promise<Project> {
    return this.request<Project>('/api/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Keyword Research
  async startKeywordResearch(data: KeywordResearchRequest): Promise<{
    session_id: string;
    status: string;
    message: string;
  }> {
    return this.request('/api/keyword-research', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getResearchResults(session_id: string): Promise<any> {
    return this.request(`/api/keyword-research/${session_id}`);
  }

  async getProjectResearchSessions(project_id: string): Promise<any[]> {
    return this.request(`/api/projects/${project_id}/research-sessions`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string; service: string }> {
    return this.request('/api/health');
  }
}

export const api = new ContentEngineAPI();
export default api;