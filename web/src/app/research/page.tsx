'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { api, Project, Company } from '@/lib/api';

export default function KeywordResearchPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isResearching, setIsResearching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [researchResult, setResearchResult] = useState<any>(null);
  const [showResults, setShowResults] = useState(false);
  const [researchSettings, setResearchSettings] = useState({
    target_location: 'India',
    target_language: 'en',
    min_search_volume: 100,
    max_competition: 0.3,
    serp_overlap_threshold: 0.3,
    keyword_expansion_limit: 50
  });

  const searchParams = useSearchParams();
  const projectParam = searchParams.get('project');
  const sessionParam = searchParams.get('session');

  useEffect(() => {
    loadData();
  }, [projectParam]);

  useEffect(() => {
    // If session parameter is provided, automatically load results
    if (sessionParam) {
      handleCheckResults(sessionParam);
    }
  }, [sessionParam]);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [projectsData, companiesData] = await Promise.all([
        api.getProjects(),
        api.getCompanies()
      ]);
      setProjects(projectsData);
      setCompanies(companiesData);
      
      // Set selected project from URL param
      if (projectParam) {
        const project = projectsData.find(p => p.id === projectParam);
        if (project) {
          setSelectedProject(project);
          // Load company settings for defaults
          const company = companiesData.find(c => c.id === project.company_id);
          if (company && company.search_settings) {
            setResearchSettings(prev => ({
              ...prev,
              ...company.search_settings
            }));
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('Error loading data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartResearch = async () => {
    if (!selectedProject) {
      setError('Please select a project first');
      return;
    }

    if (!selectedProject.broad_keyword) {
      setError('Selected project needs a broad keyword. Please edit the project first.');
      return;
    }

    try {
      setIsResearching(true);
      setError(null);

      const result = await api.startKeywordResearch({
        projectId: selectedProject.id,
        broadKeyword: selectedProject.broad_keyword,
        researchSettings: researchSettings
      });

      // Research completed automatically in the unified system
      if (result.status === 'completed') {
        // Load and display results immediately
        const results = await api.getResearchResults(result.session_id);
        if (results && results.keyword_data) {
          setResearchResult({
            ...results,
            session_id: result.session_id,
            status: 'completed',
            message: result.message
          });
          setShowResults(true);
        }
      } else {
        // Show result status
        setResearchResult({
          session_id: result.session_id,
          status: result.status,
          message: result.message || 'Research completed!'
        });
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start keyword research');
      console.error('Error starting research:', err);
    } finally {
      setIsResearching(false);
    }
  };

  const handleCheckResults = async (sessionId: string) => {
    try {
      setIsLoading(true);
      const results = await api.getResearchResults(sessionId);
      if (results && results.keyword_data) {
        setResearchResult({
          ...results,
          session_id: sessionId,
          status: 'completed',
          message: 'Research results loaded successfully!'
        });
        setShowResults(true);
      } else {
        setError('No results found for this research session. Please run the research process first.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load research results');
      console.error('Error loading results:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getCompanyName = (companyId: string) => {
    const company = companies.find(c => c.id === companyId);
    return company?.name || 'Unknown Company';
  };

  if (isLoading) {
    return (
      <div className="container py-8">
        <div className="text-center">
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
          <p>Loading keyword research interface...</p>
        </div>
      </div>
    );
  }

  const eligibleProjects = projects.filter(p => p.broad_keyword && p.broad_keyword.trim());

  return (
    <div className="container py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl mb-2">🔍 Keyword Research</h1>
          <p className="text-muted">
            Research and cluster keywords for your content projects using SERP data analysis
          </p>
        </div>
        <div className="flex items-center" style={{ gap: '1rem' }}>
          <Link href="/projects" className="button button-secondary">
            ← Back to Projects
          </Link>
          <Link href="/" className="button button-secondary">
            Dashboard
          </Link>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="card" style={{ backgroundColor: '#fef2f2', border: '1px solid #fecaca', marginBottom: '1rem' }}>
          <p style={{ color: '#dc2626' }}>❌ {error}</p>
          <button 
            className="button button-secondary" 
            style={{ marginTop: '0.5rem' }}
            onClick={() => setError(null)}
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Research result notification */}
      {researchResult && (
        <div className="card" style={{ 
          backgroundColor: researchResult.status === 'completed' ? '#f0fdf4' : '#fffbeb', 
          border: `1px solid ${researchResult.status === 'completed' ? '#bbf7d0' : '#fed7aa'}`, 
          marginBottom: '1rem' 
        }}>
          <div className="flex justify-between items-start">
            <div>
              <p style={{ color: researchResult.status === 'completed' ? '#15803d' : '#92400e', fontWeight: '600' }}>
                {researchResult.status === 'completed' ? '✅ Research Complete!' : '🎉 Research Started!'}
              </p>
              <p className="text-sm text-muted mt-1">
                {researchResult.message}
              </p>
              <p className="text-sm text-muted mt-1">
                <strong>Session ID:</strong> {researchResult.session_id}
              </p>
              {researchResult.status !== 'completed' && (
                <div className="mt-3">
                  <p className="text-sm" style={{ color: '#92400e' }}>
                    Research is processing automatically in the unified system.
                  </p>
                  <div className="mt-3">
                    <button 
                      className="button button-secondary"
                      onClick={() => handleCheckResults(researchResult.session_id)}
                      style={{ fontSize: '0.875rem' }}
                    >
                      🔍 Check for Results
                    </button>
                  </div>
                </div>
              )}
            </div>
            <button 
              className="button button-secondary" 
              style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
              onClick={() => setResearchResult(null)}
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      {/* Research Results */}
      {showResults && researchResult && researchResult.keyword_data && (
        <div className="card mb-8">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg">📊 Research Results</h3>
            <button 
              className="button button-secondary"
              onClick={() => setShowResults(false)}
            >
              Hide Results
            </button>
          </div>
          
          <div className="grid grid-cols-1 mb-4">
            <div className="card" style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0' }}>
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm"><strong>Total Keywords Found:</strong> {researchResult.total_keywords || 0}</p>
                  <p className="text-sm"><strong>Keyword Clusters:</strong> {researchResult.total_clusters || 0}</p>
                </div>
                <div>
                  <p className="text-sm text-muted">Session: {researchResult.session_id}</p>
                </div>
              </div>
            </div>
          </div>

          {researchResult.cluster_data && researchResult.cluster_data.length > 0 && (
            <div>
              <h4 className="text-md mb-3" style={{ fontWeight: '600' }}>Keyword Clusters</h4>
              <div className="space-y-3">
                {researchResult.cluster_data.slice(0, 3).map((cluster: any, index: number) => (
                  <div key={index} className="card" style={{ backgroundColor: '#fefffe', border: '1px solid #d1fae5' }}>
                    <div className="flex justify-between items-start">
                      <div>
                        <h5 style={{ fontWeight: '600', color: '#065f46' }}>{cluster.Cluster}</h5>
                        <p className="text-sm text-muted">
                          <strong>Pillar Keyword:</strong> {cluster['Pillar Keyword']}
                        </p>
                      </div>
                      <div className="text-right text-sm">
                        <p><strong>{cluster['Keywords in Cluster']}</strong> keywords</p>
                        <p className="text-muted">{cluster['Total Search Volume'].toLocaleString()} total volume</p>
                      </div>
                    </div>
                  </div>
                ))}
                {researchResult.cluster_data.length > 3 && (
                  <p className="text-sm text-muted text-center">
                    +{researchResult.cluster_data.length - 3} more clusters available in full results
                  </p>
                )}
              </div>
            </div>
          )}

          {researchResult.keyword_data && researchResult.keyword_data.length > 0 && (
            <div className="mt-6">
              <h4 className="text-md mb-3" style={{ fontWeight: '600' }}>Sample Keywords</h4>
              <div className="space-y-2">
                {researchResult.keyword_data.slice(0, 10).map((keyword: any, index: number) => (
                  <div key={index} className="flex justify-between items-center" style={{ 
                    padding: '0.5rem', 
                    backgroundColor: '#f9fafb', 
                    borderRadius: '4px',
                    border: '1px solid #f3f4f6'
                  }}>
                    <div>
                      <span className="text-sm" style={{ fontWeight: '500' }}>{keyword.Keyword}</span>
                      <span className="text-sm text-muted" style={{ marginLeft: '0.5rem' }}>
                        ({keyword.Cluster})
                      </span>
                    </div>
                    <div className="text-right text-sm">
                      <span>{keyword['Search Volume'].toLocaleString()} vol</span>
                      <span className="text-muted" style={{ marginLeft: '0.5rem' }}>
                        {keyword.Competition.toFixed(2)} comp
                      </span>
                    </div>
                  </div>
                ))}
                {researchResult.keyword_data.length > 10 && (
                  <p className="text-sm text-muted text-center">
                    +{researchResult.keyword_data.length - 10} more keywords in full dataset
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Project Selection */}
      <div className="card mb-8">
        <h3 className="text-lg mb-4">📋 Project Selection</h3>
        
        {eligibleProjects.length > 0 ? (
          <>
            <div className="space-y-2 mb-4">
              <label className="text-sm">Select Project for Keyword Research</label>
              <select
                className="input"
                value={selectedProject?.id || ''}
                onChange={(e) => {
                  const project = projects.find(p => p.id === e.target.value);
                  setSelectedProject(project || null);
                }}
              >
                <option value="">Choose a project...</option>
                {eligibleProjects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name} ({getCompanyName(project.company_id)})
                  </option>
                ))}
              </select>
              <p className="text-sm text-muted">
                Only projects with broad keywords are shown
              </p>
            </div>

            {selectedProject && (
              <div className="card" style={{ backgroundColor: '#f0f9ff', border: '1px solid #bae6fd' }}>
                <h4 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>
                  Selected: {selectedProject.name}
                </h4>
                <p className="text-sm text-muted mb-2">
                  <strong>Company:</strong> {getCompanyName(selectedProject.company_id)}
                </p>
                <p className="text-sm mb-2">
                  <strong>Broad Keyword:</strong>{' '}
                  <span style={{ color: '#2563eb' }}>{selectedProject.broad_keyword}</span>
                </p>
                {selectedProject.description && (
                  <p className="text-sm text-muted">
                    {selectedProject.description}
                  </p>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="text-center" style={{ padding: '2rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📝</div>
            <h4 className="text-lg mb-2">No projects with broad keywords found</h4>
            <p className="text-muted mb-4">
              Create projects with broad keywords first to enable keyword research
            </p>
            <Link href="/projects" className="button">
              Go to Projects
            </Link>
          </div>
        )}
      </div>

      {/* Research Settings */}
      {selectedProject && (
        <div className="card mb-8">
          <h3 className="text-lg mb-4">⚙️ Research Settings</h3>
          <p className="text-sm text-muted mb-4">
            These settings are inherited from your company but can be customized for this research
          </p>
          
          <div className="grid grid-cols-2">
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm">Target Location</label>
                <select
                  className="input"
                  value={researchSettings.target_location}
                  onChange={(e) => setResearchSettings({...researchSettings, target_location: e.target.value})}
                >
                  <option value="India">India</option>
                  <option value="United States">United States</option>
                  <option value="United Kingdom">United Kingdom</option>
                  <option value="Canada">Canada</option>
                  <option value="Australia">Australia</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm">Min Search Volume</label>
                <input
                  type="number"
                  className="input"
                  value={researchSettings.min_search_volume}
                  onChange={(e) => setResearchSettings({...researchSettings, min_search_volume: parseInt(e.target.value)})}
                  min="0"
                  max="10000"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm">Keyword Expansion Limit</label>
                <input
                  type="number"
                  className="input"
                  value={researchSettings.keyword_expansion_limit}
                  onChange={(e) => setResearchSettings({...researchSettings, keyword_expansion_limit: parseInt(e.target.value)})}
                  min="10"
                  max="200"
                />
              </div>
            </div>

            <div className="space-y-4" style={{ marginLeft: '1rem' }}>
              <div className="space-y-2">
                <label className="text-sm">Target Language</label>
                <select
                  className="input"
                  value={researchSettings.target_language}
                  onChange={(e) => setResearchSettings({...researchSettings, target_language: e.target.value})}
                >
                  <option value="en">English</option>
                  <option value="hi">Hindi</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm">Max Competition Level (0.0-1.0)</label>
                <input
                  type="number"
                  className="input"
                  value={researchSettings.max_competition}
                  onChange={(e) => setResearchSettings({...researchSettings, max_competition: parseFloat(e.target.value)})}
                  min="0"
                  max="1"
                  step="0.1"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm">SERP Overlap Threshold (0.0-1.0)</label>
                <input
                  type="number"
                  className="input"
                  value={researchSettings.serp_overlap_threshold}
                  onChange={(e) => setResearchSettings({...researchSettings, serp_overlap_threshold: parseFloat(e.target.value)})}
                  min="0"
                  max="1"
                  step="0.1"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Start Research */}
      {selectedProject && (
        <div className="card">
          <h3 className="text-lg mb-4">🚀 Run Research</h3>
          
          <div className="card" style={{ backgroundColor: '#fef3c7', border: '1px solid #fbbf24', marginBottom: '1rem' }}>
            <div className="flex items-center" style={{ gap: '0.5rem' }}>
              <div style={{ fontSize: '1.5rem' }}>⚠️</div>
              <div>
                <p className="text-sm" style={{ color: '#92400e' }}>
                  <strong>DataForSEO API Required</strong>
                </p>
                <p className="text-sm text-muted">
                  Make sure your DataForSEO credentials are set in the backend .env file
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm mb-2">
                <strong>Ready to research:</strong> {selectedProject.broad_keyword}
              </p>
              <p className="text-sm text-muted">
                This will run keyword research automatically and return results immediately
              </p>
            </div>
            
            <button 
              className="button"
              onClick={handleStartResearch}
              disabled={isResearching}
              style={{ fontSize: '1rem', padding: '1rem 2rem' }}
            >
              {isResearching ? '🔄 Starting...' : '🔍 Start Keyword Research'}
            </button>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="card mt-8" style={{ backgroundColor: '#f0f9ff', border: '1px solid #bae6fd' }}>
        <h3 className="text-lg mb-2">💡 How it Works</h3>
        <div className="text-sm space-y-2">
          <p>1. <strong>Start Research:</strong> Click the button above to run automatic keyword research</p>
          <p>2. <strong>Processing:</strong> The system automatically processes keywords using DataForSEO API</p>
          <p>3. <strong>View Results:</strong> Results appear immediately with keyword clusters and search volumes</p>
          <p>4. <strong>Integration:</strong> All data is stored in the database for use in content generation</p>
        </div>
      </div>
    </div>
  );
}