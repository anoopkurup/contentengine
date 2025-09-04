/**
 * Keyword Research Service - TypeScript implementation
 * Converted from Python KeywordResearcher.py
 */

import { db } from '@/lib/db'
import {
  DataForSEOKeyword,
  DataForSEOSerpItem,
  ResearchSettings,
  KeywordClusterResult,
  KeywordResult
} from '@/lib/types'

// DataForSEO API configuration
const DATAFORSEO_API_BASE = 'https://api.dataforseo.com/v3'

export class KeywordResearcher {
  private apiLogin: string
  private apiPassword: string
  private baseUrl: string

  constructor() {
    this.apiLogin = process.env.DATAFORSEO_LOGIN || ''
    this.apiPassword = process.env.DATAFORSEO_PASSWORD || ''
    this.baseUrl = DATAFORSEO_API_BASE

    if (!this.apiLogin || !this.apiPassword) {
      throw new Error('DataForSEO credentials not found. Please set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables.')
    }
  }

  /**
   * Make authenticated request to DataForSEO API
   */
  private async makeRequest(endpoint: string, payload: any[]): Promise<any> {
    const url = `${this.baseUrl}/${endpoint}`
    const auth = Buffer.from(`${this.apiLogin}:${this.apiPassword}`).toString('base64')

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      throw new Error(`DataForSEO API error: ${response.status} ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get keyword ideas from DataForSEO Keywords for Keywords endpoint
   */
  private async getKeywordIdeas(
    broadKeyword: string,
    location: string,
    language: string,
    expansionLimit: number = 50
  ): Promise<DataForSEOKeyword[]> {
    const payload = [{
      keywords: [broadKeyword],
      location_name: location,
      language_code: language,
      limit: expansionLimit
    }]

    const response = await this.makeRequest('keywords_data/google_ads/keywords_for_keywords/live', payload)
    
    if (!response.tasks || !response.tasks[0] || !response.tasks[0].result) {
      throw new Error('Invalid response from DataForSEO Keywords API')
    }

    const keywords: DataForSEOKeyword[] = []
    
    for (const kw of response.tasks[0].result) {
      // Handle competition field - convert string to numeric if needed
      let competition = kw.competition || 0.0
      if (typeof competition === 'string') {
        const competitionMap: Record<string, number> = {
          'LOW': 0.1,
          'MEDIUM': 0.5,
          'HIGH': 0.9
        }
        competition = competitionMap[competition.toUpperCase()] || 0.0
      }

      keywords.push({
        keyword: kw.keyword,
        search_volume: kw.search_volume || 0,
        competition: competition as number
      })
    }

    return keywords
  }

  /**
   * Get SERP results for keywords
   */
  private async getSerpResults(
    keywords: string[],
    location: string,
    language: string
  ): Promise<Record<string, string[]>> {
    const serpResults: Record<string, string[]> = {}

    // Process keywords in batches to avoid API rate limits
    for (const keyword of keywords) {
      const payload = [{
        keyword: keyword,
        location_name: location,
        language_code: language,
        se_domain: 'google.com',
        search_engine: 'google'
      }]

      try {
        const response = await this.makeRequest('serp/google/organic/live/advanced', payload)
        
        if (response.tasks && response.tasks[0] && response.tasks[0].result && response.tasks[0].result[0]) {
          const items = response.tasks[0].result[0].items || []
          const urls = items
            .filter((item: DataForSEOSerpItem) => item.url)
            .slice(0, 10) // Top 10 results
            .map((item: DataForSEOSerpItem) => item.url)
          
          serpResults[keyword] = urls
        } else {
          serpResults[keyword] = []
        }

        // Rate limiting - wait 2 seconds between requests
        await new Promise(resolve => setTimeout(resolve, 2000))
      } catch (error) {
        console.error(`Error fetching SERP for keyword "${keyword}":`, error)
        serpResults[keyword] = []
      }
    }

    return serpResults
  }

  /**
   * Cluster keywords based on SERP overlap
   */
  private clusterKeywords(
    serpResults: Record<string, string[]>,
    threshold: number = 0.3
  ): string[][] {
    const keywords = Object.keys(serpResults)
    const clusters: string[][] = []
    const visited = new Set<string>()

    for (const keyword of keywords) {
      if (visited.has(keyword)) continue

      const cluster = [keyword]
      visited.add(keyword)

      for (const otherKeyword of keywords) {
        if (visited.has(otherKeyword)) continue

        const overlap = this.calculateSerpOverlap(
          serpResults[keyword],
          serpResults[otherKeyword]
        )

        if (overlap >= threshold) {
          cluster.push(otherKeyword)
          visited.add(otherKeyword)
        }
      }

      clusters.push(cluster)
    }

    return clusters
  }

  /**
   * Calculate SERP overlap between two keyword result sets
   */
  private calculateSerpOverlap(urls1: string[], urls2: string[]): number {
    const set1 = new Set(urls1)
    const set2 = new Set(urls2)
    const intersection = new Set([...set1].filter(x => set2.has(x)))
    
    // Calculate overlap as intersection / max(10, max results)
    const maxResults = Math.max(urls1.length, urls2.length, 10)
    return intersection.size / maxResults
  }

  /**
   * Main keyword research workflow
   */
  async runKeywordResearch(
    broadKeyword: string,
    settings: ResearchSettings,
    projectId: string
  ): Promise<{ success: boolean; sessionId?: string; error?: string }> {
    try {
      console.log(`Starting keyword research for: "${broadKeyword}"`)
      console.log(`Settings:`, settings)

      // Create research session in database
      const session = await db.keywordResearchSession.create({
        data: {
          projectId,
          broadKeyword,
          researchSettings: settings,
          status: 'running'
        }
      })

      try {
        // Step 1: Get keyword ideas
        console.log('Step 1: Getting keyword ideas...')
        const keywords = await this.getKeywordIdeas(
          broadKeyword,
          settings.targetLocation || 'India',
          settings.targetLanguage || 'en',
          settings.keywordExpansionLimit || 50
        )
        
        console.log(`Found ${keywords.length} initial keywords`)

        // Step 2: Filter keywords
        const filteredKeywords = keywords.filter(kw => 
          kw.competition <= (settings.maxCompetition || 0.3) &&
          kw.search_volume >= (settings.minSearchVolume || 100)
        )

        console.log(`After filtering: ${filteredKeywords.length} keywords`)

        if (filteredKeywords.length === 0) {
          throw new Error('No keywords found matching criteria. Try lowering filters.')
        }

        // Step 3: Get SERP data (limit to 30 for API efficiency)
        const serpLimit = Math.min(filteredKeywords.length, 30)
        console.log(`Step 3: Fetching SERP data for top ${serpLimit} keywords...`)
        
        const keywordsList = filteredKeywords.slice(0, serpLimit).map(kw => kw.keyword)
        const serpData = await this.getSerpResults(
          keywordsList,
          settings.targetLocation || 'India',
          settings.targetLanguage || 'en'
        )

        console.log('SERP data collected')

        // Step 4: Cluster keywords
        console.log('Step 4: Clustering keywords...')
        const clusters = this.clusterKeywords(
          serpData,
          settings.serpOverlapThreshold || 0.3
        )
        
        console.log(`Created ${clusters.length} keyword clusters`)

        // Step 5: Process results and save to database
        const clusterData: KeywordClusterResult[] = []
        const keywordData: KeywordResult[] = []

        for (let i = 0; i < clusters.length; i++) {
          const clusterKeywords = clusters[i]
          const clusterName = `Cluster ${i + 1}`

          // Find keyword with max search volume = Pillar
          const clusterKeywordData = clusterKeywords
            .map(kw => filteredKeywords.find(fkw => fkw.keyword === kw))
            .filter(Boolean) as DataForSEOKeyword[]

          if (clusterKeywordData.length === 0) continue

          const pillarKeyword = clusterKeywordData.reduce((max, kw) => 
            kw.search_volume > max.search_volume ? kw : max
          )

          const volumes = clusterKeywordData.map(kw => kw.search_volume)
          const competitions = clusterKeywordData.map(kw => kw.competition)

          // Create cluster summary
          clusterData.push({
            'Cluster': clusterName,
            'Pillar Keyword': pillarKeyword.keyword,
            'Keywords in Cluster': clusterKeywordData.length,
            'Avg Search Volume': Math.round(volumes.reduce((a, b) => a + b, 0) / volumes.length * 10) / 10,
            'Total Search Volume': volumes.reduce((a, b) => a + b, 0),
            'Avg Competition': Math.round(competitions.reduce((a, b) => a + b, 0) / competitions.length * 1000) / 1000
          })

          // Create individual keyword records
          for (const kw of clusterKeywordData) {
            const role = kw.keyword === pillarKeyword.keyword ? 'Pillar Post' : 'Cluster Post'
            keywordData.push({
              'Cluster': clusterName,
              'Keyword': kw.keyword,
              'Search Volume': kw.search_volume,
              'Competition': kw.competition,
              'Role': role
            })
          }
        }

        // Save results to database
        await this.saveResultsToDatabase(session.id, clusterData, keywordData)

        // Update session status
        await db.keywordResearchSession.update({
          where: { id: session.id },
          data: {
            status: 'completed',
            completedAt: new Date(),
            totalClusters: clusterData.length,
            totalKeywords: keywordData.length
          }
        })

        console.log(`✅ Research completed successfully!`)
        console.log(`📄 ${keywordData.length} keywords in ${clusterData.length} clusters`)
        console.log(`📊 Session ID: ${session.id}`)

        return { success: true, sessionId: session.id }

      } catch (error) {
        // Mark session as failed
        await db.keywordResearchSession.update({
          where: { id: session.id },
          data: {
            status: 'failed',
            errorMessage: error instanceof Error ? error.message : 'Unknown error',
            completedAt: new Date()
          }
        })

        throw error
      }

    } catch (error) {
      console.error('Keyword research failed:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  }

  /**
   * Save research results to database
   */
  private async saveResultsToDatabase(
    sessionId: string,
    clusterData: KeywordClusterResult[],
    keywordData: KeywordResult[]
  ): Promise<void> {
    // Group keywords by cluster for efficient insertion
    const keywordsByCluster: Record<string, KeywordResult[]> = {}
    for (const keyword of keywordData) {
      if (!keywordsByCluster[keyword.Cluster]) {
        keywordsByCluster[keyword.Cluster] = []
      }
      keywordsByCluster[keyword.Cluster].push(keyword)
    }

    // Create clusters and their keywords
    for (const cluster of clusterData) {
      const clusterRecord = await db.keywordCluster.create({
        data: {
          sessionId,
          clusterName: cluster.Cluster,
          pillarKeyword: cluster['Pillar Keyword'],
          keywordsCount: cluster['Keywords in Cluster'],
          totalSearchVolume: cluster['Total Search Volume'],
          avgSearchVolume: cluster['Avg Search Volume'],
          avgCompetition: cluster['Avg Competition']
        }
      })

      // Create keywords for this cluster
      const clusterKeywords = keywordsByCluster[cluster.Cluster] || []
      if (clusterKeywords.length > 0) {
        await db.keyword.createMany({
          data: clusterKeywords.map(kw => ({
            clusterId: clusterRecord.id,
            keyword: kw.Keyword,
            searchVolume: kw['Search Volume'],
            competition: kw.Competition,
            role: kw.Role
          }))
        })
      }
    }
  }

  /**
   * Get research session results
   */
  async getSessionResults(sessionId: string): Promise<any> {
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

    const clusterData: KeywordClusterResult[] = session.clusters.map(cluster => ({
      'Cluster': cluster.clusterName,
      'Pillar Keyword': cluster.pillarKeyword || '',
      'Keywords in Cluster': cluster.keywordsCount,
      'Avg Search Volume': cluster.avgSearchVolume,
      'Total Search Volume': cluster.totalSearchVolume,
      'Avg Competition': cluster.avgCompetition
    }))

    const keywordData: KeywordResult[] = []
    for (const cluster of session.clusters) {
      for (const keyword of cluster.keywords) {
        keywordData.push({
          'Cluster': cluster.clusterName,
          'Keyword': keyword.keyword,
          'Search Volume': keyword.searchVolume,
          'Competition': keyword.competition,
          'Role': keyword.role || ''
        })
      }
    }

    return {
      session: {
        id: session.id,
        projectId: session.projectId,
        broadKeyword: session.broadKeyword,
        status: session.status,
        createdAt: session.createdAt,
        completedAt: session.completedAt,
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