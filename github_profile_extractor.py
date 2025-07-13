import requests
from collections import Counter
import json

GITHUB_TOKEN = ""  # your github token here
HEADERS = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_repo_languages(repo):
    url = repo['languages_url']
    response = requests.get(url, headers=HEADERS)
    return list(response.json().keys())

def get_repo_topics(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/topics"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("names", [])

def extract_profile(username):
    repos = get_repos(username)
    if isinstance(repos, dict) and repos.get("message"):
        print("Error:", repos.get("message"))
        return

    all_languages = []
    all_topics = []
    repo_summaries = []

    for repo in repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        
        languages = get_repo_languages(repo)
        topics = get_repo_topics(owner, repo_name)

        all_languages.extend(languages)
        all_topics.extend(topics)

        repo_summaries.append({
            "repo_name": repo_name,
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "watchers": repo.get("watchers_count"),
            "open_issues": repo.get("open_issues_count"),
            "language_main": repo.get("language"),
            "languages": languages,
            "topics": topics,
            "is_fork": repo.get("fork"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at")
        })

    language_counter = Counter(all_languages)
    topic_counter = Counter(all_topics)

    profile_summary = {
        "github_username": username,
        "top_languages": [lang for lang, _ in language_counter.most_common(5)],
        "top_topics": [topic for topic, _ in topic_counter.most_common(5)],
        "public_repo_count": len(repos),
        "repos": repo_summaries
    }

    return profile_summary


if __name__ == "__main__":
    username = input("Enter GitHub username: ")
    profile = extract_profile(username)
    
    if profile:
        with open(f"{username}_github_profile.json", "w") as f:
            json.dump(profile, f, indent=4)
        print(f"Profile data saved to {username}_github_profile.json")
