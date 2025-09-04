'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api, DashboardData } from '@/lib/api';

export default function Home() {
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    stats: {
      totalCompanies: 0,
      totalProjects: 0,
      activeProjects: 0,
      completedProjects: 0
    },
    recentProjects: []
  });

  const [keywordInput, setKeywordInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load dashboard data from API
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await api.getDashboardData();
        setDashboardData(data);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        setError('Failed to load dashboard data. Using demo data.');
      }
    };

    fetchDashboardData();
  }, []);

  const handleQuickResearch = () => {
    if (!keywordInput.trim()) {
      alert('Please enter a broad keyword first');
      return;
    }
    
    // Redirect to research page with keyword
    window.location.href = `/research?keyword=${encodeURIComponent(keywordInput)}`;
  };

  return (
    <div style={{ minHeight: '100vh' }}>
      <div className="container py-8">
        <div className="mb-8">
          <h1 className="text-2xl mb-2">
            ContentEngine
          </h1>
          <p className="text-muted text-lg">
            AI-Powered Content Creation with Beautiful UI
          </p>
        </div>

        {/* Error message */}
        {error && (
          <div className="card" style={{ backgroundColor: '#fef2f2', border: '1px solid #fecaca', marginBottom: '1rem' }}>
            <p style={{ color: '#dc2626', fontSize: '0.875rem' }}>⚠️ {error}</p>
          </div>
        )}

        <div className="grid grid-cols-3">
          <div className="card">
            <h3 className="text-lg mb-2">Dashboard</h3>
            <p className="text-sm text-muted mb-4">
              Overview of your content projects
            </p>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted">Total Projects</span>
                <span className="text-2xl">{dashboardData.stats.totalProjects}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted">Completed</span>
                <span className="text-2xl" style={{ color: '#10b981' }}>
                  {dashboardData.stats.completedProjects}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted">Companies</span>
                <span className="text-2xl">{dashboardData.stats.totalCompanies}</span>
              </div>
              <Link href="/projects" className="button w-full" style={{ textDecoration: 'none', textAlign: 'center' }}>
                View All Projects
              </Link>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg mb-2">Keyword Research</h3>
            <p className="text-sm text-muted mb-4">
              Research and cluster keywords for your content
            </p>
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="keyword" className="text-sm">Broad Keyword</label>
                <input 
                  id="keyword" 
                  className="input" 
                  placeholder="e.g., digital marketing"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleQuickResearch();
                    }
                  }}
                />
              </div>
              <Link 
                href="/research"
                className="button button-secondary w-full"
                style={{ textDecoration: 'none', textAlign: 'center' }}
              >
                Start Research
              </Link>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg mb-2">Quick Actions</h3>
            <p className="text-sm text-muted mb-4">
              Common tasks and shortcuts
            </p>
            <div className="space-y-4">
              <Link 
                href="/projects"
                className="button button-secondary w-full"
                style={{ textDecoration: 'none', textAlign: 'center' }}
              >
                Create New Project
              </Link>
              <Link 
                href="/research"
                className="button button-secondary w-full"
                style={{ textDecoration: 'none', textAlign: 'center' }}
              >
                Run Pipeline
              </Link>
              <Link 
                href="/companies"
                className="button button-secondary w-full"
                style={{ textDecoration: 'none', textAlign: 'center' }}
              >
                Manage Companies
              </Link>
            </div>
          </div>
        </div>

        <div className="card mt-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h3 className="text-lg mb-2">Recent Projects</h3>
              <p className="text-sm text-muted">
                Your latest content creation projects
              </p>
            </div>
            {dashboardData.stats.totalProjects > 0 && (
              <Link href="/projects" className="button button-secondary" style={{ textDecoration: 'none' }}>
                View All
              </Link>
            )}
          </div>
          
          <div className="space-y-4">
            {dashboardData.recentProjects.length > 0 ? (
              dashboardData.recentProjects.map((project: any, index: number) => (
                <div key={project.id || index} className="flex items-center justify-between" style={{ padding: '1rem', border: '1px solid #e0e0e0', borderRadius: '6px' }}>
                  <div>
                    <h4 style={{ fontWeight: '600' }}>{project.name || `Project ${index + 1}`}</h4>
                    <p className="text-sm text-muted">
                      {project.description || 'Digital marketing content for SaaS companies'}
                    </p>
                    {project.broadKeyword && (
                      <p className="text-sm" style={{ color: '#2563eb' }}>
                        Keywords: {project.broadKeyword}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center" style={{ gap: '0.5rem' }}>
                    <span className="text-sm text-muted">{project.completion || 0}% complete</span>
                    <Link 
                      href={`/research?project=${project.id}`}
                      className="button" 
                      style={{ padding: '0.5rem 1rem', fontSize: '0.75rem', textDecoration: 'none' }}
                    >
                      Research
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              // Show getting started guide when no real data
              <div className="text-center" style={{ padding: '3rem' }}>
                <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🚀</div>
                <h4 className="text-lg mb-2">Welcome to ContentEngine!</h4>
                <p className="text-muted mb-6">
                  Get started by creating your first company and project
                </p>
                
                <div className="grid grid-cols-1" style={{ maxWidth: '600px', margin: '0 auto' }}>
                  <div className="flex items-center" style={{ gap: '1rem', padding: '1rem', border: '1px solid #e0e0e0', borderRadius: '6px', marginBottom: '1rem' }}>
                    <div style={{ fontSize: '2rem' }}>1️⃣</div>
                    <div className="flex-1 text-left">
                      <h5 style={{ fontWeight: '600', marginBottom: '0.25rem' }}>Create a Company</h5>
                      <p className="text-sm text-muted">Set up your organization with search and content settings</p>
                    </div>
                    <Link href="/companies" className="button" style={{ textDecoration: 'none' }}>
                      Create
                    </Link>
                  </div>
                  
                  <div className="flex items-center" style={{ gap: '1rem', padding: '1rem', border: '1px solid #e0e0e0', borderRadius: '6px', marginBottom: '1rem' }}>
                    <div style={{ fontSize: '2rem' }}>2️⃣</div>
                    <div className="flex-1 text-left">
                      <h5 style={{ fontWeight: '600', marginBottom: '0.25rem' }}>Create a Project</h5>
                      <p className="text-sm text-muted">Define your content project with broad keywords</p>
                    </div>
                    <Link href="/projects" className="button" style={{ textDecoration: 'none' }}>
                      Create
                    </Link>
                  </div>
                  
                  <div className="flex items-center" style={{ gap: '1rem', padding: '1rem', border: '1px solid #e0e0e0', borderRadius: '6px' }}>
                    <div style={{ fontSize: '2rem' }}>3️⃣</div>
                    <div className="flex-1 text-left">
                      <h5 style={{ fontWeight: '600', marginBottom: '0.25rem' }}>Run Research</h5>
                      <p className="text-sm text-muted">Generate keyword clusters and content briefs</p>
                    </div>
                    <Link href="/research" className="button" style={{ textDecoration: 'none' }}>
                      Research
                    </Link>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Status indicator */}
        <div className="card mt-8" style={{ backgroundColor: '#f0f9ff', border: '1px solid #bae6fd' }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center" style={{ gap: '0.5rem' }}>
              <div style={{ width: '8px', height: '8px', backgroundColor: '#22c55e', borderRadius: '50%' }}></div>
              <span className="text-sm">
                <strong>ContentEngine Status:</strong> Unified Next.js App ✅
              </span>
            </div>
            <div className="flex" style={{ gap: '0.5rem' }}>
              <a 
                href="/api/health" 
                target="_blank" 
                rel="noopener noreferrer"
                className="button button-secondary"
                style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem', textDecoration: 'none' }}
              >
                API Health
              </a>
            </div>
          </div>
          <p className="text-sm text-muted mt-2">
            Running unified Next.js application with integrated API routes and database
          </p>
        </div>
      </div>
    </div>
  );
}