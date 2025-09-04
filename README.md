# ContentEngine

**Modern AI-Powered Content Creation Platform**

ContentEngine is a unified Next.js application that automates the entire content creation workflow—from keyword research to multi-platform content distribution. Built with TypeScript, Prisma, and integrated AI services for professional content marketing.

[![Next.js 15](https://img.shields.io/badge/Next.js-15.5.2-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Prisma](https://img.shields.io/badge/Prisma-Latest-2D3748)](https://www.prisma.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- DataForSEO API credentials (for keyword research)

### Installation

1. **Clone and Setup**
   ```bash
   cd ContentEngine/web
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

3. **Setup Database**
   ```bash
   npx prisma generate
   npx prisma db push
   ```

4. **Launch Application**
   ```bash
   npm run dev
   ```

Visit http://localhost:3000 to access ContentEngine.

## 🏗️ Architecture

ContentEngine is built as a **unified Next.js application** with integrated backend services:

```
🏢 Company Setup → 📋 Project Creation → 🔍 Keyword Research → 📝 Content Generation → 📊 Results Management
```

### 🖥️ Application Stack

- **Frontend**: Next.js 15 with App Router
- **Backend**: Next.js API Routes 
- **Database**: SQLite with Prisma ORM
- **Language**: TypeScript throughout
- **Styling**: Custom CSS with responsive design
- **AI Integration**: DataForSEO API + TypeScript keyword research service

### 🎯 Core Features

- **🏢 Company Management**: Multi-company support with brand settings
- **📋 Project Organization**: Structured project workflow management  
- **🔍 Advanced Keyword Research**: SERP-based clustering and analysis
- **📊 Real-time Dashboard**: Live project status and statistics
- **🎨 Modern UI**: Clean, responsive interface with intuitive navigation

## ✨ Key Features

### 🏢 Company Management
- **Brand Voice Configuration**: Define writing style, target audience, content guidelines
- **Search Settings**: Configure location targeting, language, competition thresholds
- **Multi-company Support**: Manage content for multiple clients or brands
- **Settings Management**: Easy editing of company configurations

### 📋 Project Management  
- **Structured Projects**: Link projects to companies with specific keywords
- **Broad Keyword Focus**: Each project targets a main keyword theme
- **Status Tracking**: Monitor project progress and completion
- **Research Integration**: Seamless connection to keyword research workflows

### 🔍 Keyword Research Engine
- **DataForSEO Integration**: Professional keyword research with real search data
- **SERP Analysis**: Analyze competitor content and identify gaps
- **Keyword Clustering**: Automatic grouping based on search intent
- **Competition Analysis**: Filter by search volume and competition metrics
- **Results Export**: Download research data for external analysis

### 📊 Unified Dashboard
- **Project Overview**: See all projects and their current status
- **Quick Actions**: Fast access to common tasks and workflows
- **Real-time Stats**: Live updates on companies, projects, and research sessions
- **Intuitive Navigation**: Clean interface designed for productivity

## ⚙️ Configuration

### Required API Credentials

Add to your `.env` file:

```env
# Database
DATABASE_URL="file:./dev.db"

# DataForSEO API Credentials (Required)
DATAFORSEO_LOGIN="your_email@example.com"
DATAFORSEO_PASSWORD="your_api_password"

# Application Settings
NEXT_PUBLIC_APP_NAME="ContentEngine"
NEXT_PUBLIC_API_URL="http://localhost:3000"

# Content Configuration
TARGET_LOCATION="India"
TARGET_LANGUAGE="en"
SERP_OVERLAP_THRESHOLD="0.3"
MIN_SEARCH_VOLUME="100"
MAX_COMPETITION="0.3"
```

### Database Configuration

ContentEngine uses SQLite with Prisma ORM. The database schema includes:

- **Companies**: Brand settings, search preferences, content guidelines
- **Projects**: Linked to companies with broad keywords and descriptions  
- **Research Sessions**: Keyword research data and results
- **Keywords**: Individual keyword data with search volume and competition
- **Clusters**: Grouped keywords based on search intent

## 🎯 Getting Started

### 1. Create Your First Company

1. Navigate to **Companies** from the dashboard
2. Click **"+ New Company"** 
3. Configure in 3 tabs:
   - **Basic Info**: Company name, description, location
   - **Search Settings**: Language, search volume, competition thresholds
   - **Brand & Content**: Brand voice, writing style, target audience, content guidelines

### 2. Create a Project

1. Go to **Projects** from the main menu
2. Click **"+ New Project"**
3. Fill in project details:
   - Link to a company
   - Add broad keyword (e.g., "digital marketing")
   - Provide project description

### 3. Run Keyword Research

1. Navigate to **Research** from the dashboard
2. Select your project from the dropdown
3. Review and customize research settings
4. Click **"🔍 Start Keyword Research"**
5. View results with keyword clusters and search volumes

### 4. Manage Your Content

- **Dashboard**: Overview of all projects and their status
- **Projects**: Detailed view of individual projects and research sessions
- **Companies**: Manage brand settings and configurations
- **Research**: Run and view keyword research results

## 📁 Project Structure

```
ContentEngine/
├── web/                           # Next.js application
│   ├── src/
│   │   ├── app/                   # Next.js App Router
│   │   │   ├── page.tsx           # Dashboard
│   │   │   ├── companies/         # Company management
│   │   │   ├── projects/          # Project management  
│   │   │   ├── research/          # Keyword research
│   │   │   └── api/               # API routes
│   │   │       ├── companies/     # Company CRUD operations
│   │   │       ├── projects/      # Project CRUD operations
│   │   │       ├── dashboard/     # Dashboard data
│   │   │       └── keyword-research/ # Research API
│   │   ├── lib/
│   │   │   ├── api.ts             # Frontend API client
│   │   │   ├── types.ts           # TypeScript interfaces
│   │   │   └── services/          # Backend services
│   │   │       ├── database.ts    # Database operations
│   │   │       └── keywordResearcher.ts # Research engine
│   │   └── styles/                # CSS styling
│   ├── prisma/
│   │   └── schema.prisma          # Database schema
│   ├── package.json               # Dependencies
│   └── .env                       # Configuration
├── Writing Instructions.md        # Brand voice guidelines
└── README.md                      # This file
```

## 🔧 Development

### Database Management

```bash
# Generate Prisma client
npx prisma generate

# Apply schema changes
npx prisma db push

# View database in browser
npx prisma studio

# Reset database (removes all data)
npx prisma db push --force-reset
```

### API Development

The application uses Next.js API routes for all backend operations:

- **GET/POST /api/companies** - Company management
- **GET/POST /api/projects** - Project operations  
- **POST /api/keyword-research** - Start keyword research
- **GET /api/keyword-research/[id]** - Get research results
- **GET /api/dashboard** - Dashboard statistics

### Adding Features

1. **Database Changes**: Update `prisma/schema.prisma` and run `npx prisma db push`
2. **API Endpoints**: Add new routes in `src/app/api/`
3. **Frontend Pages**: Create new pages in `src/app/`
4. **Types**: Update `src/lib/types.ts` for TypeScript support
5. **Services**: Add business logic in `src/lib/services/`

## 🛠️ Advanced Features

### 🔍 Keyword Research Intelligence

- **DataForSEO Integration**: Professional-grade keyword data
- **SERP Analysis**: Competitor content analysis and gap identification
- **Cluster Detection**: Automatic grouping based on search result overlap
- **Competition Scoring**: Detailed competition analysis with volume filtering
- **Export Capabilities**: Download results in multiple formats

### 📊 Data Management

- **Real-time Updates**: Live dashboard updates and progress tracking
- **File Organization**: Structured data storage with relational database
- **Export Options**: Download project data and research results
- **Data Persistence**: All data stored in SQLite database

### ⚙️ Configuration Management

- **Company Templates**: Reusable brand and search configurations
- **Environment Variables**: Secure credential and settings management
- **API Integration**: Seamless DataForSEO connectivity with error handling
- **Input Validation**: Comprehensive validation throughout the application

## 🔒 Security & Best Practices

- ✅ **Environment Variables**: All credentials stored securely in `.env`
- ✅ **Git Security**: Database and sensitive files excluded from version control
- ✅ **Input Validation**: Server-side validation on all API endpoints
- ✅ **Error Handling**: User-friendly error messages without exposing internals
- ✅ **Type Safety**: Full TypeScript coverage for compile-time safety

## 🎯 Target Use Cases

### Marketing Agencies
- **Client Management**: Handle multiple client accounts with separate branding
- **Scalable Research**: Efficient keyword research for multiple campaigns
- **Brand Consistency**: Maintain distinct brand voices across client projects

### Content Teams  
- **Research-Driven Planning**: Data-driven keyword research for content calendars
- **SEO Optimization**: Professional keyword analysis and competition research
- **Workflow Management**: Structured project management with clear status tracking

### Solo Consultants
- **Professional Tools**: Enterprise-grade keyword research capabilities
- **Time Efficiency**: Streamlined workflow from research to content planning
- **Client Reports**: Professional research outputs for client deliverables

## 📊 System Requirements

### Minimum Requirements
- **Node.js**: 18.0 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space for database and cache
- **Network**: Stable internet connection for API calls

### API Requirements
- **DataForSEO Account**: Required for keyword research functionality
- **API Quota**: Varies based on research volume and frequency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and test thoroughly
4. Run type checking: `npm run build`
5. Commit: `git commit -m 'Add new feature'`
6. Push: `git push origin feature/new-feature`  
7. Submit a Pull Request

## 🔗 Links

- **DataForSEO API**: https://dataforseo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Prisma Documentation**: https://www.prisma.io/docs
- **TypeScript Handbook**: https://www.typescriptlang.org/docs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built for modern content creators who demand professional tools and efficient workflows.**

*ContentEngine combines enterprise-grade keyword research with intuitive project management, making professional content strategy accessible to teams of all sizes.*