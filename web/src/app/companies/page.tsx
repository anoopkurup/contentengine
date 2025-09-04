'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api, Company } from '@/lib/api';

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [editingCompany, setEditingCompany] = useState<Company | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [newCompany, setNewCompany] = useState({
    name: '',
    description: '',
    target_location: 'India',
    target_language: 'en',
    min_search_volume: 100,
    max_competition: 0.3,
    brand_voice: '',
    writing_style: '',
    target_audience: '',
    content_guidelines: ''
  });

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setIsLoading(true);
      const data = await api.getCompanies();
      setCompanies(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load companies');
      console.error('Error loading companies:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateCompany = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const companyData = {
        name: newCompany.name,
        description: newCompany.description,
        search_settings: {
          target_location: newCompany.target_location,
          target_language: newCompany.target_language,
          min_search_volume: newCompany.min_search_volume,
          max_competition: newCompany.max_competition,
          serp_overlap_threshold: 0.3,
          keyword_expansion_limit: 50
        },
        brand_settings: {
          brand_voice: newCompany.brand_voice,
          writing_style: newCompany.writing_style,
          target_audience: newCompany.target_audience
        },
        content_settings: {
          content_guidelines: newCompany.content_guidelines.split('\n').filter(line => line.trim())
        }
      };
      
      await api.createCompany(companyData);
      setShowCreateForm(false);
      setNewCompany({
        name: '',
        description: '',
        target_location: 'India',
        target_language: 'en',
        min_search_volume: 100,
        max_competition: 0.3,
        brand_voice: '',
        writing_style: '',
        target_audience: '',
        content_guidelines: ''
      });
      await loadCompanies(); // Reload the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create company');
      console.error('Error creating company:', err);
    }
  };

  const handleEditCompany = (company: Company) => {
    setEditingCompany(company);
    setShowEditForm(true);
    setActiveTab(0);
    // Pre-populate the form with current company data
    setNewCompany({
      name: company.name,
      description: company.description || '',
      target_location: company.search_settings?.target_location || 'India',
      target_language: company.search_settings?.target_language || 'en',
      min_search_volume: company.search_settings?.min_search_volume || 100,
      max_competition: company.search_settings?.max_competition || 0.3,
      brand_voice: company.brand_settings?.brand_voice || '',
      writing_style: company.brand_settings?.writing_style || '',
      target_audience: company.brand_settings?.target_audience || '',
      content_guidelines: company.content_settings?.content_guidelines?.join('\n') || ''
    });
  };

  const handleUpdateCompany = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingCompany) return;
    
    try {
      const companyData = {
        name: newCompany.name,
        description: newCompany.description,
        search_settings: {
          target_location: newCompany.target_location,
          target_language: newCompany.target_language,
          min_search_volume: newCompany.min_search_volume,
          max_competition: newCompany.max_competition,
          serp_overlap_threshold: 0.3,
          keyword_expansion_limit: 50
        },
        brand_settings: {
          brand_voice: newCompany.brand_voice,
          writing_style: newCompany.writing_style,
          target_audience: newCompany.target_audience
        },
        content_settings: {
          content_guidelines: newCompany.content_guidelines.split('\n').filter(line => line.trim())
        }
      };
      
      await api.updateCompany(editingCompany.id, companyData);
      setShowEditForm(false);
      setEditingCompany(null);
      setNewCompany({
        name: '',
        description: '',
        target_location: 'India',
        target_language: 'en',
        min_search_volume: 100,
        max_competition: 0.3,
        brand_voice: '',
        writing_style: '',
        target_audience: '',
        content_guidelines: ''
      });
      await loadCompanies(); // Reload the list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update company');
      console.error('Error updating company:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="container py-8">
        <div className="text-center">
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
          <p>Loading companies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl mb-2">Company Management</h1>
          <p className="text-muted">
            Manage your companies and their content generation settings
          </p>
        </div>
        <div className="flex items-center" style={{ gap: '1rem' }}>
          <Link href="/" className="button button-secondary">
            ← Back to Dashboard
          </Link>
          <button 
            className="button"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : '+ New Company'}
          </button>
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
              loadCompanies();
            }}
          >
            Try Again
          </button>
        </div>
      )}

      {/* Create form */}
      {showCreateForm && (
        <div className="card mb-8">
          <h3 className="text-lg mb-4">Create New Company</h3>
          
          {/* Tab Navigation */}
          <div className="tab-nav">
            {['Basic Info', 'Search Settings', 'Brand & Content'].map((tab, index) => (
              <button
                key={index}
                type="button"
                className={`tab-button ${activeTab === index ? 'active' : ''}`}
                onClick={() => setActiveTab(index)}
              >
                {tab}
              </button>
            ))}
          </div>

          <form onSubmit={handleCreateCompany} className="space-y-4">
            {/* Tab 1: Basic Info */}
            {activeTab === 0 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Company Name *</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Acme Corp"
                      value={newCompany.name}
                      onChange={(e) => setNewCompany({...newCompany, name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Target Location</label>
                    <select
                      className="input"
                      value={newCompany.target_location}
                      onChange={(e) => setNewCompany({...newCompany, target_location: e.target.value})}
                    >
                      <option value="India">India</option>
                      <option value="United States">United States</option>
                      <option value="United Kingdom">United Kingdom</option>
                      <option value="Canada">Canada</option>
                      <option value="Australia">Australia</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Description</label>
                  <textarea
                    className="input"
                    placeholder="Brief description of the company..."
                    value={newCompany.description}
                    onChange={(e) => setNewCompany({...newCompany, description: e.target.value})}
                    rows={3}
                  />
                </div>
              </div>
            )}

            {/* Tab 2: Search Settings */}
            {activeTab === 1 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Target Language</label>
                    <select
                      className="input"
                      value={newCompany.target_language}
                      onChange={(e) => setNewCompany({...newCompany, target_language: e.target.value})}
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi</option>
                      <option value="es">Spanish</option>
                      <option value="fr">French</option>
                      <option value="de">German</option>
                    </select>
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Min Search Volume</label>
                    <input
                      type="number"
                      className="input"
                      value={newCompany.min_search_volume}
                      onChange={(e) => setNewCompany({...newCompany, min_search_volume: parseInt(e.target.value)})}
                      min="0"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Max Competition (0.0-1.0)</label>
                  <input
                    type="number"
                    className="input"
                    value={newCompany.max_competition}
                    onChange={(e) => setNewCompany({...newCompany, max_competition: parseFloat(e.target.value)})}
                    min="0"
                    max="1"
                    step="0.1"
                  />
                  <p className="text-sm text-muted">Higher values mean more competitive keywords are allowed</p>
                </div>
              </div>
            )}

            {/* Tab 3: Brand & Content */}
            {activeTab === 2 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Brand Voice</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Professional and approachable"
                      value={newCompany.brand_voice}
                      onChange={(e) => setNewCompany({...newCompany, brand_voice: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Writing Style</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Conversational yet informative"
                      value={newCompany.writing_style}
                      onChange={(e) => setNewCompany({...newCompany, writing_style: e.target.value})}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Target Audience</label>
                  <input
                    type="text"
                    className="input"
                    placeholder="e.g., Small business owners and entrepreneurs"
                    value={newCompany.target_audience}
                    onChange={(e) => setNewCompany({...newCompany, target_audience: e.target.value})}
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Content Guidelines (one per line)</label>
                  <textarea
                    className="input large"
                    placeholder="Always include actionable insights&#10;Use data and statistics to support points&#10;Keep paragraphs under 3 sentences&#10;Include relevant examples"
                    value={newCompany.content_guidelines}
                    onChange={(e) => setNewCompany({...newCompany, content_guidelines: e.target.value})}
                    rows={5}
                  />
                  <p className="text-sm text-muted">Enter each guideline on a separate line</p>
                </div>
              </div>
            )}

            <div className="flex justify-between items-center" style={{ paddingTop: '1rem', borderTop: '1px solid #e0e0e0' }}>
              <div className="flex" style={{ gap: '0.5rem' }}>
                {activeTab > 0 && (
                  <button 
                    type="button" 
                    className="button button-secondary"
                    onClick={() => setActiveTab(activeTab - 1)}
                  >
                    ← Previous
                  </button>
                )}
                {activeTab < 2 && (
                  <button 
                    type="button" 
                    className="button button-secondary"
                    onClick={() => setActiveTab(activeTab + 1)}
                  >
                    Next →
                  </button>
                )}
              </div>
              
              <div className="flex" style={{ gap: '0.5rem' }}>
                <button 
                  type="button" 
                  className="button button-secondary"
                  onClick={() => {
                    setShowCreateForm(false);
                    setActiveTab(0);
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="button">
                  Create Company
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* Edit form */}
      {showEditForm && editingCompany && (
        <div className="card mb-8">
          <h3 className="text-lg mb-4">Edit Company: {editingCompany.name}</h3>
          
          {/* Tab Navigation */}
          <div className="tab-nav">
            {['Basic Info', 'Search Settings', 'Brand & Content'].map((tab, index) => (
              <button
                key={index}
                type="button"
                className={`tab-button ${activeTab === index ? 'active' : ''}`}
                onClick={() => setActiveTab(index)}
              >
                {tab}
              </button>
            ))}
          </div>

          <form onSubmit={handleUpdateCompany} className="space-y-4">
            {/* Tab 1: Basic Info */}
            {activeTab === 0 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Company Name *</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Acme Corp"
                      value={newCompany.name}
                      onChange={(e) => setNewCompany({...newCompany, name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Target Location</label>
                    <select
                      className="input"
                      value={newCompany.target_location}
                      onChange={(e) => setNewCompany({...newCompany, target_location: e.target.value})}
                    >
                      <option value="India">India</option>
                      <option value="United States">United States</option>
                      <option value="United Kingdom">United Kingdom</option>
                      <option value="Canada">Canada</option>
                      <option value="Australia">Australia</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Description</label>
                  <textarea
                    className="input"
                    placeholder="Brief description of the company..."
                    value={newCompany.description}
                    onChange={(e) => setNewCompany({...newCompany, description: e.target.value})}
                    rows={3}
                  />
                </div>
              </div>
            )}

            {/* Tab 2: Search Settings */}
            {activeTab === 1 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Target Language</label>
                    <select
                      className="input"
                      value={newCompany.target_language}
                      onChange={(e) => setNewCompany({...newCompany, target_language: e.target.value})}
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi</option>
                      <option value="es">Spanish</option>
                      <option value="fr">French</option>
                      <option value="de">German</option>
                    </select>
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Min Search Volume</label>
                    <input
                      type="number"
                      className="input"
                      value={newCompany.min_search_volume}
                      onChange={(e) => setNewCompany({...newCompany, min_search_volume: parseInt(e.target.value)})}
                      min="0"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Max Competition (0.0-1.0)</label>
                  <input
                    type="number"
                    className="input"
                    value={newCompany.max_competition}
                    onChange={(e) => setNewCompany({...newCompany, max_competition: parseFloat(e.target.value)})}
                    min="0"
                    max="1"
                    step="0.1"
                  />
                  <p className="text-sm text-muted">Higher values mean more competitive keywords are allowed</p>
                </div>
              </div>
            )}

            {/* Tab 3: Brand & Content */}
            {activeTab === 2 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2">
                  <div className="space-y-2">
                    <label className="text-sm">Brand Voice</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Professional and approachable"
                      value={newCompany.brand_voice}
                      onChange={(e) => setNewCompany({...newCompany, brand_voice: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2" style={{ marginLeft: '1rem' }}>
                    <label className="text-sm">Writing Style</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Conversational yet informative"
                      value={newCompany.writing_style}
                      onChange={(e) => setNewCompany({...newCompany, writing_style: e.target.value})}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Target Audience</label>
                  <input
                    type="text"
                    className="input"
                    placeholder="e.g., Small business owners and entrepreneurs"
                    value={newCompany.target_audience}
                    onChange={(e) => setNewCompany({...newCompany, target_audience: e.target.value})}
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm">Content Guidelines (one per line)</label>
                  <textarea
                    className="input large"
                    placeholder="Always include actionable insights&#10;Use data and statistics to support points&#10;Keep paragraphs under 3 sentences&#10;Include relevant examples"
                    value={newCompany.content_guidelines}
                    onChange={(e) => setNewCompany({...newCompany, content_guidelines: e.target.value})}
                    rows={5}
                  />
                  <p className="text-sm text-muted">Enter each guideline on a separate line</p>
                </div>
              </div>
            )}

            <div className="flex justify-between items-center" style={{ paddingTop: '1rem', borderTop: '1px solid #e0e0e0' }}>
              <div className="flex" style={{ gap: '0.5rem' }}>
                {activeTab > 0 && (
                  <button 
                    type="button" 
                    className="button button-secondary"
                    onClick={() => setActiveTab(activeTab - 1)}
                  >
                    ← Previous
                  </button>
                )}
                {activeTab < 2 && (
                  <button 
                    type="button" 
                    className="button button-secondary"
                    onClick={() => setActiveTab(activeTab + 1)}
                  >
                    Next →
                  </button>
                )}
              </div>
              
              <div className="flex" style={{ gap: '0.5rem' }}>
                <button 
                  type="button" 
                  className="button button-secondary"
                  onClick={() => {
                    setShowEditForm(false);
                    setEditingCompany(null);
                    setActiveTab(0);
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="button">
                  Update Company
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* Companies list */}
      <div className="grid grid-cols-1">
        {companies.length > 0 ? (
          companies.map((company) => (
            <div key={company.id} className="card">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg mb-2">{company.name}</h3>
                  <p className="text-sm text-muted mb-4">
                    {company.description || 'No description'}
                  </p>
                  
                  {/* Brand & Content Info */}
                  {(company.brand_settings?.brand_voice || company.brand_settings?.writing_style || company.brand_settings?.target_audience) && (
                    <div className="mb-4 p-3" style={{ backgroundColor: '#f8fafc', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                      <h4 className="text-sm font-medium mb-2" style={{ color: '#374151' }}>Brand & Content</h4>
                      <div className="grid grid-cols-1 gap-2 text-sm">
                        {company.brand_settings?.brand_voice && (
                          <p><strong>Voice:</strong> {company.brand_settings.brand_voice}</p>
                        )}
                        {company.brand_settings?.writing_style && (
                          <p><strong>Style:</strong> {company.brand_settings.writing_style}</p>
                        )}
                        {company.brand_settings?.target_audience && (
                          <p><strong>Audience:</strong> {company.brand_settings.target_audience}</p>
                        )}
                        {company.content_settings?.content_guidelines && company.content_settings.content_guidelines.length > 0 && (
                          <div>
                            <strong>Guidelines:</strong>
                            <ul style={{ marginLeft: '1rem', marginTop: '0.25rem' }}>
                              {company.content_settings.content_guidelines.slice(0, 2).map((guideline: string, index: number) => (
                                <li key={index} style={{ fontSize: '0.75rem', color: '#6b7280' }}>• {guideline}</li>
                              ))}
                              {company.content_settings.content_guidelines.length > 2 && (
                                <li style={{ fontSize: '0.75rem', color: '#9ca3af', fontStyle: 'italic' }}>
                                  +{company.content_settings.content_guidelines.length - 2} more guidelines
                                </li>
                              )}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                  
                  {/* Search Settings */}
                  <div className="grid grid-cols-2 text-sm mb-3">
                    <div className="space-y-1">
                      <p><strong>Location:</strong> {company.search_settings?.target_location || 'Not set'}</p>
                      <p><strong>Language:</strong> {company.search_settings?.target_language || 'Not set'}</p>
                    </div>
                    <div className="space-y-1">
                      <p><strong>Min Volume:</strong> {company.search_settings?.min_search_volume || 0}</p>
                      <p><strong>Max Competition:</strong> {company.search_settings?.max_competition || 0}</p>
                    </div>
                  </div>
                  
                  <p className="text-sm text-muted">
                    Created: {company.created_at ? new Date(company.created_at).toLocaleDateString() : 'Unknown date'}
                  </p>
                </div>
                
                <div className="space-y-2" style={{ marginLeft: '2rem' }}>
                  <Link 
                    href={`/projects?company=${company.id}`}
                    className="button button-secondary"
                    style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}
                  >
                    View Projects
                  </Link>
                  <button 
                    className="button button-secondary w-full"
                    onClick={() => handleEditCompany(company)}
                  >
                    Edit Settings
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center">
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🏢</div>
            <h3 className="text-lg mb-2">No companies yet</h3>
            <p className="text-muted mb-4">
              Create your first company to start managing content projects
            </p>
            <button 
              className="button"
              onClick={() => setShowCreateForm(true)}
            >
              Create First Company
            </button>
          </div>
        )}
      </div>
    </div>
  );
}