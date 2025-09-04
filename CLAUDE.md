# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ContentEngine is a unified Next.js TypeScript application for AI-powered content creation. The system manages companies, projects, and keyword research through a modern web interface with integrated database operations.

## Architecture

### Technology Stack
- **Frontend**: Next.js 15 with App Router, TypeScript, React 19
- **Backend**: Next.js API Routes
- **Database**: SQLite with Prisma ORM
- **Styling**: Custom CSS (no Tailwind classes in components)
- **APIs**: DataForSEO integration for keyword research

### Core Data Flow
1. **Companies** → **Projects** → **Research Sessions** → **Keyword Clusters** → **Keywords**
2. Each company has brand settings (voice, style, guidelines) and search settings
3. Projects belong to companies and have broad keywords for research
4. Research sessions generate keyword clusters with SERP analysis
5. All data persists in SQLite with Prisma ORM relationships

### Directory Structure
```
web/
├── src/app/                    # Next.js App Router
│   ├── api/                   # API Routes (backend)
│   │   ├── companies/         # Company CRUD
│   │   ├── projects/          # Project CRUD  
│   │   ├── keyword-research/  # Research engine
│   │   └── dashboard/         # Aggregated data
│   ├── companies/page.tsx     # Company management UI
│   ├── projects/page.tsx      # Project management UI
│   ├── research/page.tsx      # Keyword research UI
│   └── page.tsx              # Dashboard
├── src/lib/
│   ├── api.ts                # Frontend API client
│   ├── types.ts              # TypeScript interfaces
│   ├── db.ts                 # Prisma client
│   └── services/             # Backend business logic
│       ├── database.ts       # Database operations
│       └── keywordResearcher.ts # Research engine
└── prisma/schema.prisma      # Database schema
```

## Common Commands

### Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

### Database Operations
```bash
# Generate Prisma client after schema changes
npx prisma generate

# Push schema changes to database
npx prisma db push

# Reset database (removes all data)
npx prisma db push --force-reset

# Open database browser
npx prisma studio
```

## Key Architecture Patterns

### API Route Structure
- All API routes follow REST conventions with proper HTTP methods
- Database operations use Prisma with proper error handling
- API responses use consistent JSON structure with camelCase
- Field naming: Database uses snake_case, API/Frontend uses camelCase

### Component Architecture
- Pages are in `src/app/[page]/page.tsx` using Next.js App Router
- All components use TypeScript with proper interface definitions
- State management uses React hooks (useState, useEffect)
- API calls use the centralized `api.ts` client

### Database Schema Design
- Primary entities: Company → Project → KeywordResearchSession → KeywordCluster → Keyword
- All models use cuid() for IDs and proper cascading deletes
- JSON fields store complex configurations (searchSettings, brandSettings, etc.)
- DateTime fields with proper mapping (createdAt, updatedAt)

### Service Layer Pattern
- `CompanyService`, `ProjectService`, `DashboardService` in `database.ts`
- `KeywordResearcher` class handles DataForSEO API integration
- Services return properly typed objects, not raw Prisma models
- Error handling with user-friendly messages

## Environment Configuration

Required environment variables:
```
DATABASE_URL="file:./dev.db"
DATAFORSEO_LOGIN="your_email"
DATAFORSEO_PASSWORD="your_api_password"
NEXT_PUBLIC_APP_NAME="ContentEngine"
NEXT_PUBLIC_API_URL="http://localhost:3000"
TARGET_LOCATION="India"
TARGET_LANGUAGE="en"
SERP_OVERLAP_THRESHOLD="0.3"
MIN_SEARCH_VOLUME="100"
MAX_COMPETITION="0.3"
```

## Key Integration Points

### DataForSEO API Integration
- `KeywordResearcher` class handles all DataForSEO API calls
- Implements keyword expansion, SERP analysis, and clustering algorithms
- Results stored in database with proper relationships
- API credentials validated on class instantiation

### Frontend-Backend Communication
- Frontend uses `src/lib/api.ts` client for all API calls
- API routes in `src/app/api/` handle database operations
- Consistent error handling with user-friendly messages
- Real-time updates through React state management

### Database Relationships
- Companies have many Projects (cascading delete)
- Projects have many KeywordResearchSessions (cascading delete)
- Research sessions have many KeywordClusters (cascading delete)
- Clusters have many Keywords (cascading delete)

## Content Creation Workflow

1. **Company Creation**: Brand settings, search preferences, content guidelines
2. **Project Setup**: Link to company, define broad keyword, set description
3. **Keyword Research**: Run DataForSEO analysis, generate clusters
4. **Results Management**: View research results, analyze keyword opportunities

## Important Notes

- This is a **unified Next.js application** - there are no separate Python scripts or Streamlit interfaces
- All content generation logic is integrated into TypeScript services
- Database operations use Prisma ORM exclusively
- The system replaced a legacy Python-based architecture completely
- Custom CSS is used instead of Tailwind classes in components