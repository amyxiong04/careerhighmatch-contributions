-- Table to store the overall GitHub profile summary
CREATE TABLE IF NOT EXISTS github_profiles (
    id SERIAL PRIMARY KEY,
    github_username TEXT NOT NULL,
    top_languages TEXT[],
    top_topics TEXT[],
    public_repo_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store detailed information about each repository
CREATE TABLE IF NOT EXISTS github_repos (
    id SERIAL PRIMARY KEY,
    github_profile_id INTEGER REFERENCES github_profiles(id),
    repo_name TEXT,
    description TEXT,
    stars INTEGER,
    forks INTEGER,
    watchers INTEGER,
    open_issues INTEGER,
    language_main TEXT,
    languages TEXT[],
    topics TEXT[],
    is_fork BOOLEAN,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
