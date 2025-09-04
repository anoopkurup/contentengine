'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { api, Project, Company } from '@/lib/api';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedCompanyFilter, setSelectedCompanyFilter] = useState<string>('');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [projectSessions, setProjectSessions] = useState<any[]>([]);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    broadKeyword: '',
    companyId: ''
  });

  const searchParams = useSearchParams();
  const companyParam = searchParams.get('company');

  useEffect(() => {
    loadData();
    if (companyParam) {
      setSelectedCompanyFilter(companyParam);
    }
  }, [companyParam]);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [projectsData, companiesData] = await Promise.all([
        api.getProjects(companyParam || undefined),
        api.getCompanies()
      ]);
      setProjects(projectsData);
      setCompanies(companiesData);
      
      // Set first company as default for new projects
      if (companiesData.length > 0 && !newProject.companyId) {
        setNewProject(prev => ({
          ...prev,
          companyId: companyParam || companiesData[0].id
        }));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('Error loading data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProject.companyId) {
      setError('Please select a company first');
      return;
    }
    
    try {
      await api.createProject(newProject);
      setShowCreateForm(false);
      setNewProject({
        name: '',
        description: '',
        broadKeyword: '',
        companyId: companies[0]?.id || ''
      });
      await loadData(); // Reload the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
      console.error('Error creating project:', err);
    }
  };

  const handleViewDetails = async (project: Project) => {
    try {
      setSelectedProject(project);
      // Load research sessions for this project
      const sessions = await api.getProjectResearchSessions(project.id);
      setProjectSessions(sessions);
    } catch (err) {
      console.error('Error loading project details:', err);
      setError('Failed to load project details');
    }
  };

  const filteredProjects = selectedCompanyFilter 
    ? projects.filter(p => p.company_id === selectedCompanyFilter)
    : projects;

  const getCompanyName = (companyId: string) => {
    const company = companies.find(c => c.id === companyId);
    return company?.name || 'Unknown Company';
  };

  if (isLoading) {
    return (
      <div className="container py-8">
        <div className="text-center">
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
          <p>Loading projects...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl mb-2">Project Management</h1>
          <p className="text-muted">
            Manage your content projects and research sessions
          </p>
        </div>
        <div className="flex items-center" style={{ gap: '1rem' }}>
          <Link href="/" className="button button-secondary">
            ← Back to Dashboard
          </Link>
          {companies.length > 0 ? (
            <button 
              className="button"
              onClick={() => setShowCreateForm(!showCreateForm)}
            >
              {showCreateForm ? 'Cancel' : '+ New Project'}
            </button>
          ) : (
            <Link href="/companies" className="button">
              Create Company First
            </Link>
          )}
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="card" style={{ backgroundColor: '#fef2f2', border: '1px solid #fecaca', marginBottom: '1rem' }}>
          <p style={{ color: '#dc2626' }}>❌ {error}</p>
          <button 
            className="button button-secondary" 
            style={{ marginTop: '0.5rem' }}
            onClick={() => {
              setError(null);
              loadData();
            }}
          >
            Try Again
          </button>
        </div>
      )}

      {/* Filters */}
      {companies.length > 0 && (
        <div className="card mb-6">
          <div className="flex items-center" style={{ gap: '1rem' }}>
            <label className="text-sm">Filter by Company:</label>
            <select
              className="input"
              style={{ width: '200px' }}
              value={selectedCompanyFilter}
              onChange={(e) => setSelectedCompanyFilter(e.target.value)}
            >
              <option value="">All Companies</option>
              {companies.map((company) => (
                <option key={company.id} value={company.id}>
                  {company.name}
                </option>
              ))}
            </select>
            <span className="text-sm text-muted">
              Showing {filteredProjects.length} of {projects.length} projects
            </span>
          </div>
        </div>
      )}

      {/* Create form */}
      {showCreateForm && (
        <div className="card mb-8">
          <h3 className="text-lg mb-4">Create New Project</h3>
          <form onSubmit={handleCreateProject} className="space-y-4">
            <div className="grid grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm">Project Name *</label>
                <input
                  type="text"
                  className="input"
                  placeholder="e.g., AI Marketing Campaign"
                  value={newProject.name}
                  onChange={(e) => setNewProject({...newProject, name: e.target.value})}
                  required
                />
              </div>
              <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                <label className="text-sm">Company *</label>
                <select
                  className="input"
                  value={newProject.companyId}
                  onChange={(e) => setNewProject({...newProject, companyId: e.target.value})}
                  required
                >
                  <option value="">Select Company</option>
                  {companies.map((company) => (
                    <option key={company.id} value={company.id}>
                      {company.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm">Description</label>
              <textarea
                className="input"
                placeholder="Brief description of this content project..."
                value={newProject.description}
                onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                rows={2}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm">Broad Keyword</label>
              <input
                type="text"
                className="input"
                placeholder="e.g., digital marketing"
                value={newProject.broadKeyword}
                onChange={(e) => setNewProject({...newProject, broadKeyword: e.target.value})}
              />
              <p className="text-sm text-muted">
                Main keyword for content research and generation
              </p>
            </div>

            <div className="flex" style={{ gap: '0.5rem' }}>
              <button type="submit" className="button">
                Create Project
              </button>
              <button 
                type="button" 
                className="button button-secondary"
                onClick={() => setShowCreateForm(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Project Details Modal */}
      {selectedProject && (
        <div className="card mb-8">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg">📋 Project Details: {selectedProject.name}</h3>
            <button 
              className="button button-secondary"
              onClick={() => {
                setSelectedProject(null);
                setProjectSessions([]);
              }}
            >
              Close
            </button>
          </div>
          
          <div className="grid grid-cols-2 mb-4">
            <div>
              <p className="text-sm"><strong>Company:</strong> {getCompanyName(selectedProject.company_id)}</p>
              <p className="text-sm"><strong>Description:</strong> {selectedProject.description || 'No description'}</p>
              <p className="text-sm"><strong>Broad Keyword:</strong> {selectedProject.broad_keyword || 'Not set'}</p>
            </div>
            <div>
              <p className="text-sm"><strong>Created:</strong> {new Date(selectedProject.created_at).toLocaleDateString()}</p>
              <p className="text-sm"><strong>Research Sessions:</strong> {projectSessions.length}</p>
            </div>
          </div>

          {projectSessions.length > 0 && (
            <div>
              <h4 className="text-md mb-3" style={{ fontWeight: '600' }}>Research Sessions</h4>
              <div className="space-y-2">
                {projectSessions.map((session: any, index: number) => (
                  <div key={session.id} className="card" style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-sm" style={{ fontWeight: '500' }}>{session.broad_keyword}</p>
                        <p className="text-sm text-muted">
                          Status: <span style={{ 
                            color: session.status === 'completed' ? '#10b981' : 
                                   session.status === 'running' ? '#f59e0b' : '#6b7280' 
                          }}>
                            {session.status}
                          </span>
                        </p>
                      </div>
                      <div className="text-right text-sm">
                        {session.status === 'completed' && (
                          <>
                            <p><strong>{session.total_keywords || 0}</strong> keywords</p>
                            <p><strong>{session.total_clusters || 0}</strong> clusters</p>
                          </>
                        )}
                        <p className="text-muted">{new Date(session.created_at).toLocaleDateString()}</p>
                      </div>
                    </div>
                    {session.status === 'completed' && (
                      <div className="mt-2">
                        <Link 
                          href={`/research?project=${selectedProject.id}&session=${session.id}`}
                          className="button button-secondary"
                          style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem', textDecoration: 'none' }}
                        >
                          View Results
                        </Link>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {projectSessions.length === 0 && (
            <div className="text-center" style={{ padding: '2rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔍</div>
              <p className="text-muted">No research sessions yet</p>
              <Link 
                href={`/research?project=${selectedProject.id}`}
                className="button"
                style={{ marginTop: '1rem', textDecoration: 'none' }}
              >
                Start First Research
              </Link>
            </div>
          )}
        </div>
      )}

      {/* Projects list */}
      <div className="grid grid-cols-1">
        {filteredProjects.length > 0 ? (
          filteredProjects.map((project) => (
            <div key={project.id} className="card">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center mb-2" style={{ gap: '0.5rem' }}>
                    <h3 className="text-lg">{project.name}</h3>
                    <span className="text-sm" style={{ 
                      backgroundColor: '#f3f4f6', 
                      padding: '0.25rem 0.5rem', 
                      borderRadius: '4px',
                      color: '#6b7280'
                    }}>
                      {getCompanyName(project.company_id)}
                    </span>
                  </div>
                  
                  {project.description && (
                    <p className="text-sm text-muted mb-2">
                      {project.description}
                    </p>
                  )}
                  
                  {project.broad_keyword && (
                    <p className="text-sm mb-2">
                      <strong>Keyword:</strong>{' '}
                      <span style={{ color: '#2563eb' }}>{project.broad_keyword}</span>
                    </p>
                  )}
                  
                  <p className="text-sm text-muted">
                    Created: {new Date(project.created_at).toLocaleDateString()}
                  </p>
                </div>
                
                <div className="space-y-2" style={{ marginLeft: '2rem' }}>
                  <Link 
                    href={`/research?project=${project.id}`}
                    className="button"
                    style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}
                  >
                    🔍 Start Research
                  </Link>
                  <button 
                    className="button button-secondary w-full"
                    onClick={() => handleViewDetails(project)}
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : companies.length === 0 ? (
          <div className="card text-center">
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🏢</div>
            <h3 className="text-lg mb-2">No companies found</h3>
            <p className="text-muted mb-4">
              Create a company first before creating projects
            </p>
            <Link href="/companies" className="button">
              Create Company
            </Link>
          </div>
        ) : (
          <div className="card text-center">
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📋</div>
            <h3 className="text-lg mb-2">
              {selectedCompanyFilter ? 'No projects for this company' : 'No projects yet'}
            </h3>
            <p className="text-muted mb-4">
              Create your first project to start content research and generation
            </p>
            <button 
              className="button"
              onClick={() => setShowCreateForm(true)}
            >
              Create First Project
            </button>
          </div>
        )}
      </div>
    </div>
  );
}