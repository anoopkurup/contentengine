-- CreateTable
CREATE TABLE "companies" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "search_settings" JSONB,
    "content_settings" JSONB,
    "brand_settings" JSONB,
    "seo_settings" JSONB,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "projects" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "company_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "broad_keyword" TEXT,
    "status" TEXT NOT NULL DEFAULT 'active',
    "config" JSONB,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" DATETIME NOT NULL,
    CONSTRAINT "projects_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "companies" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "keyword_research_sessions" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "project_id" TEXT NOT NULL,
    "broad_keyword" TEXT NOT NULL,
    "research_settings" JSONB,
    "total_keywords" INTEGER NOT NULL DEFAULT 0,
    "total_clusters" INTEGER NOT NULL DEFAULT 0,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "error_message" TEXT,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completed_at" DATETIME,
    CONSTRAINT "keyword_research_sessions_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES "projects" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "keyword_clusters" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "session_id" TEXT NOT NULL,
    "cluster_name" TEXT NOT NULL,
    "pillar_keyword" TEXT,
    "keywords_count" INTEGER NOT NULL DEFAULT 0,
    "total_search_volume" INTEGER NOT NULL DEFAULT 0,
    "avg_search_volume" REAL NOT NULL DEFAULT 0.0,
    "avg_competition" REAL NOT NULL DEFAULT 0.0,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "keyword_clusters_session_id_fkey" FOREIGN KEY ("session_id") REFERENCES "keyword_research_sessions" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "keywords" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "cluster_id" TEXT NOT NULL,
    "keyword" TEXT NOT NULL,
    "search_volume" INTEGER NOT NULL DEFAULT 0,
    "competition" REAL NOT NULL DEFAULT 0.0,
    "role" TEXT,
    "serp_urls" JSONB,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "keywords_cluster_id_fkey" FOREIGN KEY ("cluster_id") REFERENCES "keyword_clusters" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "pipeline_stages" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "project_id" TEXT NOT NULL,
    "stage_name" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "started_at" DATETIME,
    "completed_at" DATETIME,
    "error_message" TEXT,
    "output_data" JSONB,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" DATETIME NOT NULL,
    CONSTRAINT "pipeline_stages_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES "projects" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
