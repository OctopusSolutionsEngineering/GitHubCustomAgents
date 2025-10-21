#!/usr/bin/env python3
"""
Script to generate release notes from Octopus Deploy and GitHub
"""
import os
import sys
import json
import requests
from datetime import datetime

# Configuration
OCTOPUS_SERVER_URL = os.environ.get('OCTOPUS_SERVER_URL', 'https://octopus.example.com')
OCTOPUS_API_KEY = os.environ.get('OCTOPUS_API_KEY', '')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY', 'mcasperson/GitHubCustomAgents')

SPACE_NAME = "Octopus Copilot"
PROJECT_NAME = "Octopus Copilot Function"
ENVIRONMENT_NAME = "Production"

def get_octopus_headers():
    return {
        'X-Octopus-ApiKey': OCTOPUS_API_KEY,
        'Content-Type': 'application/json'
    }

def get_github_headers():
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

def get_space_id():
    """Get the Space ID from space name"""
    url = f"{OCTOPUS_SERVER_URL}/api/spaces/all"
    response = requests.get(url, headers=get_octopus_headers())
    response.raise_for_status()
    
    spaces = response.json()
    for space in spaces:
        if space['Name'] == SPACE_NAME:
            return space['Id']
    
    raise ValueError(f"Space '{SPACE_NAME}' not found")

def get_project_id(space_id):
    """Get the Project ID from project name"""
    url = f"{OCTOPUS_SERVER_URL}/api/{space_id}/projects/all"
    response = requests.get(url, headers=get_octopus_headers())
    response.raise_for_status()
    
    projects = response.json()
    for project in projects:
        if project['Name'] == PROJECT_NAME:
            return project['Id']
    
    raise ValueError(f"Project '{PROJECT_NAME}' not found")

def get_environment_id(space_id):
    """Get the Environment ID from environment name"""
    url = f"{OCTOPUS_SERVER_URL}/api/{space_id}/environments/all"
    response = requests.get(url, headers=get_octopus_headers())
    response.raise_for_status()
    
    environments = response.json()
    for env in environments:
        if env['Name'] == ENVIRONMENT_NAME:
            return env['Id']
    
    raise ValueError(f"Environment '{ENVIRONMENT_NAME}' not found")

def get_latest_deployment(space_id, project_id, environment_id):
    """Get the latest deployment for the project in the environment"""
    url = f"{OCTOPUS_SERVER_URL}/api/{space_id}/deployments"
    params = {
        'projects': project_id,
        'environments': environment_id,
        'take': 1
    }
    response = requests.get(url, headers=get_octopus_headers(), params=params)
    response.raise_for_status()
    
    deployments = response.json()
    if deployments['Items']:
        return deployments['Items'][0]
    
    raise ValueError(f"No deployments found for project '{PROJECT_NAME}' in environment '{ENVIRONMENT_NAME}'")

def get_release_build_info(space_id, release_id):
    """Get build information for a release"""
    url = f"{OCTOPUS_SERVER_URL}/api/{space_id}/releases/{release_id}"
    response = requests.get(url, headers=get_octopus_headers())
    response.raise_for_status()
    
    release = response.json()
    
    # Get build information
    build_info_url = f"{OCTOPUS_SERVER_URL}/api/{space_id}/releases/{release_id}/buildinformation"
    build_response = requests.get(build_info_url, headers=get_octopus_headers())
    
    if build_response.status_code == 200:
        return release, build_response.json()
    
    return release, None

def get_github_commit_info(commit_sha):
    """Get commit information from GitHub"""
    owner, repo = GITHUB_REPO.split('/')
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    
    response = requests.get(url, headers=get_github_headers())
    if response.status_code == 200:
        return response.json()
    
    return None

def generate_release_notes(release, build_info):
    """Generate markdown release notes"""
    notes = []
    notes.append(f"# Release Notes: {release.get('Version', 'Unknown')}\n")
    notes.append(f"**Project:** {PROJECT_NAME}\n")
    notes.append(f"**Environment:** {ENVIRONMENT_NAME}\n")
    notes.append(f"**Release Date:** {release.get('Assembled', 'Unknown')}\n")
    notes.append("\n---\n")
    
    if build_info and 'Items' in build_info:
        notes.append("\n## Changes\n")
        
        for item in build_info['Items']:
            if 'Commits' in item:
                for commit in item['Commits']:
                    commit_id = commit.get('Id', '')
                    
                    # Get detailed commit info from GitHub
                    commit_info = get_github_commit_info(commit_id)
                    
                    if commit_info:
                        author = commit_info['commit']['author']['name']
                        date = commit_info['commit']['author']['date']
                        message = commit_info['commit']['message']
                        
                        # Skip certain commit messages
                        skip_patterns = ['Merge', 'merge', 'Initial plan', 'WIP', 'wip']
                        if any(pattern in message for pattern in skip_patterns):
                            continue
                        
                        notes.append(f"\n### {message.split(chr(10))[0]}\n")
                        notes.append(f"- **Author:** {author}\n")
                        notes.append(f"- **Date:** {date}\n")
                        notes.append(f"- **Commit:** `{commit_id[:7]}`\n")
                        
                        # Add files changed
                        if 'files' in commit_info:
                            notes.append(f"- **Files Changed:** {len(commit_info['files'])}\n")
                    else:
                        # Fallback to basic info
                        message = commit.get('Comment', 'No message')
                        notes.append(f"\n- {message} (`{commit_id[:7]}`)\n")
    else:
        notes.append("\n*No build information available*\n")
    
    return ''.join(notes)

def main():
    print("Fetching Octopus Deploy release information...")
    
    if not OCTOPUS_API_KEY:
        print("Error: OCTOPUS_API_KEY environment variable not set")
        sys.exit(1)
    
    try:
        # Get IDs
        space_id = get_space_id()
        project_id = get_project_id(space_id)
        environment_id = get_environment_id(space_id)
        
        # Get latest deployment
        deployment = get_latest_deployment(space_id, project_id, environment_id)
        release_id = deployment['ReleaseId']
        
        # Get release and build info
        release, build_info = get_release_build_info(space_id, release_id)
        
        # Generate release notes
        release_notes = generate_release_notes(release, build_info)
        
        # Save to file
        output_file = '/home/runner/work/GitHubCustomAgents/GitHubCustomAgents/release-notes.md'
        with open(output_file, 'w') as f:
            f.write(release_notes)
        
        print(f"Release notes saved to {output_file}")
        print("\n" + "="*50)
        print(release_notes)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
