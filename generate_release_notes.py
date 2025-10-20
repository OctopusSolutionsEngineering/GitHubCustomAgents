#!/usr/bin/env python3
"""
Generate release notes for Octopus Copilot Function project.
This script fetches the latest release from Octopus Deploy and generates comprehensive release notes.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Any

# Configuration
OCTOPUS_SERVER = os.environ.get('OCTOPUS_SERVER', 'https://octopus.example.com')
OCTOPUS_API_KEY = os.environ.get('OCTOPUS_API_KEY', '')
OCTOPUS_SPACE = 'Octopus Copilot'
OCTOPUS_PROJECT = 'Octopus Copilot Function'
OCTOPUS_ENVIRONMENT = 'Production'
GITHUB_REPO_OWNER = 'mcasperson'
GITHUB_REPO_NAME = 'GitHubCustomAgents'


def get_octopus_headers():
    """Get headers for Octopus API requests."""
    if not OCTOPUS_API_KEY:
        print("ERROR: OCTOPUS_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return {
        'X-Octopus-ApiKey': OCTOPUS_API_KEY,
        'Content-Type': 'application/json'
    }


def make_octopus_request(endpoint: str) -> Dict[str, Any]:
    """Make a request to the Octopus API."""
    import urllib.request
    url = f"{OCTOPUS_SERVER}/api/{endpoint}"
    req = urllib.request.Request(url, headers=get_octopus_headers())
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"ERROR: Failed to make request to {url}: {e}", file=sys.stderr)
        sys.exit(1)


def get_space_id() -> str:
    """Get the Space ID for the given space name."""
    spaces = make_octopus_request('spaces/all')
    for space in spaces:
        if space['Name'] == OCTOPUS_SPACE:
            return space['Id']
    
    print(f"ERROR: Space '{OCTOPUS_SPACE}' not found.", file=sys.stderr)
    sys.exit(1)


def get_project_id(space_id: str) -> str:
    """Get the Project ID for the given project name."""
    projects = make_octopus_request(f'{space_id}/projects/all')
    for project in projects:
        if project['Name'] == OCTOPUS_PROJECT:
            return project['Id']
    
    print(f"ERROR: Project '{OCTOPUS_PROJECT}' not found.", file=sys.stderr)
    sys.exit(1)


def get_environment_id(space_id: str) -> str:
    """Get the Environment ID for the given environment name."""
    environments = make_octopus_request(f'{space_id}/environments/all')
    for env in environments:
        if env['Name'] == OCTOPUS_ENVIRONMENT:
            return env['Id']
    
    print(f"ERROR: Environment '{OCTOPUS_ENVIRONMENT}' not found.", file=sys.stderr)
    sys.exit(1)


def get_latest_release(space_id: str, project_id: str, environment_id: str) -> Dict[str, Any]:
    """Get the latest release deployed to the specified environment."""
    # Get deployments for the project in the environment
    deployments = make_octopus_request(
        f'{space_id}/deployments?projects={project_id}&environments={environment_id}&take=1'
    )
    
    if not deployments.get('Items'):
        print(f"ERROR: No deployments found for project in {OCTOPUS_ENVIRONMENT}.", file=sys.stderr)
        sys.exit(1)
    
    latest_deployment = deployments['Items'][0]
    release_id = latest_deployment['ReleaseId']
    
    # Get the release details
    release = make_octopus_request(f'{space_id}/releases/{release_id}')
    return release


def get_build_information(space_id: str, release: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get build information (including commits) for the release."""
    commits = []
    
    # Get package versions from the release
    if 'BuildInformation' in release:
        for build_info in release['BuildInformation']:
            build_info_id = build_info['Id']
            build_data = make_octopus_request(f'{space_id}/build-information/{build_info_id}')
            
            if 'Commits' in build_data:
                commits.extend(build_data['Commits'])
    
    return commits


def get_commit_details_from_github(commit_sha: str) -> Dict[str, Any]:
    """Get commit details from GitHub using git command."""
    try:
        # Get commit message
        message = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%s%n%n%b', commit_sha],
            cwd=f'/home/runner/work/{GITHUB_REPO_NAME}/{GITHUB_REPO_NAME}',
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Get commit author
        author = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%an <%ae>', commit_sha],
            cwd=f'/home/runner/work/{GITHUB_REPO_NAME}/{GITHUB_REPO_NAME}',
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Get commit date
        date = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%ai', commit_sha],
            cwd=f'/home/runner/work/{GITHUB_REPO_NAME}/{GITHUB_REPO_NAME}',
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Get commit diff (limited to avoid too much output)
        diff = subprocess.check_output(
            ['git', 'show', '--stat', commit_sha],
            cwd=f'/home/runner/work/{GITHUB_REPO_NAME}/{GITHUB_REPO_NAME}',
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        return {
            'sha': commit_sha,
            'message': message,
            'author': author,
            'date': date,
            'diff': diff
        }
    except subprocess.CalledProcessError:
        return {
            'sha': commit_sha,
            'message': 'Unable to fetch commit details',
            'author': 'Unknown',
            'date': 'Unknown',
            'diff': ''
        }


def is_relevant_commit(commit: Dict[str, Any]) -> bool:
    """Determine if a commit is relevant for release notes."""
    message = commit.get('message', '').lower()
    
    # Skip merge commits from automated systems
    if 'merge pull request' in message or 'merge branch' in message:
        return False
    
    # Skip trivial commits
    trivial_keywords = ['typo', 'formatting', 'whitespace', 'comment', 'readme update']
    if any(keyword in message for keyword in trivial_keywords):
        return False
    
    return True


def generate_release_notes(release: Dict[str, Any], commits: List[Dict[str, Any]]) -> str:
    """Generate markdown release notes from release and commit data."""
    release_version = release.get('Version', 'Unknown')
    release_date = release.get('Assembled', datetime.now().isoformat())
    
    # Parse and format the date
    try:
        release_datetime = datetime.fromisoformat(release_date.replace('Z', '+00:00'))
        formatted_date = release_datetime.strftime('%B %d, %Y at %H:%M UTC')
    except:
        formatted_date = release_date
    
    notes = f"""# Release Notes: {OCTOPUS_PROJECT}

## Version {release_version}
**Released:** {formatted_date}  
**Environment:** {OCTOPUS_ENVIRONMENT}  
**Space:** {OCTOPUS_SPACE}

---

## Summary

This release contains {len(commits)} commit(s) with updates and improvements to the Octopus Copilot Function.

---

## Changes

"""
    
    # Group commits by type based on conventional commits or content
    features = []
    fixes = []
    improvements = []
    other = []
    
    for commit in commits:
        message = commit.get('message', '').split('\n')[0]  # First line only
        message_lower = message.lower()
        
        if message_lower.startswith('feat:') or 'feature' in message_lower:
            features.append(commit)
        elif message_lower.startswith('fix:') or 'bug' in message_lower or 'fix' in message_lower:
            fixes.append(commit)
        elif message_lower.startswith('perf:') or message_lower.startswith('refactor:') or 'improve' in message_lower:
            improvements.append(commit)
        else:
            other.append(commit)
    
    # Add features section
    if features:
        notes += "### ✨ Features\n\n"
        for commit in features:
            notes += format_commit(commit)
        notes += "\n"
    
    # Add fixes section
    if fixes:
        notes += "### 🐛 Bug Fixes\n\n"
        for commit in fixes:
            notes += format_commit(commit)
        notes += "\n"
    
    # Add improvements section
    if improvements:
        notes += "### 🔧 Improvements\n\n"
        for commit in improvements:
            notes += format_commit(commit)
        notes += "\n"
    
    # Add other changes
    if other:
        notes += "### 📝 Other Changes\n\n"
        for commit in other:
            notes += format_commit(commit)
        notes += "\n"
    
    # Add detailed commit information
    notes += "---\n\n## Detailed Commit Information\n\n"
    for commit in commits:
        notes += format_detailed_commit(commit)
    
    # Add contributors section
    contributors = set(commit.get('author', 'Unknown') for commit in commits)
    notes += "---\n\n## Contributors\n\n"
    notes += f"This release includes contributions from {len(contributors)} contributor(s):\n\n"
    for contributor in sorted(contributors):
        notes += f"- {contributor}\n"
    
    notes += "\n---\n\n"
    notes += f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*\n"
    
    return notes


def format_commit(commit: Dict[str, Any]) -> str:
    """Format a commit for the summary section."""
    sha = commit.get('sha', 'unknown')[:7]
    message = commit.get('message', 'No message').split('\n')[0]
    author = commit.get('author', 'Unknown')
    
    return f"- **{message}** (`{sha}`) - {author}\n"


def format_detailed_commit(commit: Dict[str, Any]) -> str:
    """Format a commit with full details."""
    sha = commit.get('sha', 'unknown')
    message = commit.get('message', 'No message')
    author = commit.get('author', 'Unknown')
    date = commit.get('date', 'Unknown')
    diff = commit.get('diff', '')
    
    # Limit diff to first 50 lines to keep notes readable
    diff_lines = diff.split('\n')
    if len(diff_lines) > 50:
        diff = '\n'.join(diff_lines[:50]) + '\n... (diff truncated)'
    
    detailed = f"""### Commit {sha[:7]}

**Author:** {author}  
**Date:** {date}

**Message:**
```
{message}
```

**Changes:**
```
{diff}
```

---

"""
    return detailed


def main():
    """Main function to generate release notes."""
    print(f"Generating release notes for {OCTOPUS_PROJECT}...", file=sys.stderr)
    print(f"Space: {OCTOPUS_SPACE}", file=sys.stderr)
    print(f"Environment: {OCTOPUS_ENVIRONMENT}", file=sys.stderr)
    print("", file=sys.stderr)
    
    # Check if we're in demo mode (no Octopus credentials)
    if not OCTOPUS_API_KEY:
        print("NOTICE: Running in demo mode (no Octopus credentials)", file=sys.stderr)
        print("Will generate sample release notes based on recent commits", file=sys.stderr)
        print("", file=sys.stderr)
        
        # Get recent commits from the current repository
        try:
            commit_shas = subprocess.check_output(
                ['git', 'log', '--pretty=format:%H', '-n', '10'],
                cwd='/home/runner/work/GitHubCustomAgents/GitHubCustomAgents'
            ).decode('utf-8').strip().split('\n')
            
            commits = []
            for sha in commit_shas:
                if sha:
                    commits.append(get_commit_details_from_github(sha))
            
            # Filter relevant commits
            relevant_commits = [c for c in commits if is_relevant_commit(c)]
            
            # Create a mock release object
            release = {
                'Version': '1.0.0-demo',
                'Assembled': datetime.now().isoformat()
            }
            
            # Generate and output release notes
            notes = generate_release_notes(release, relevant_commits)
            print(notes)
            
        except Exception as e:
            print(f"ERROR: Failed to generate demo release notes: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Normal mode with Octopus credentials
    try:
        # Get IDs for space, project, and environment
        print("Fetching Space ID...", file=sys.stderr)
        space_id = get_space_id()
        print(f"Space ID: {space_id}", file=sys.stderr)
        
        print("Fetching Project ID...", file=sys.stderr)
        project_id = get_project_id(space_id)
        print(f"Project ID: {project_id}", file=sys.stderr)
        
        print("Fetching Environment ID...", file=sys.stderr)
        environment_id = get_environment_id(space_id)
        print(f"Environment ID: {environment_id}", file=sys.stderr)
        
        # Get the latest release
        print("Fetching latest release...", file=sys.stderr)
        release = get_latest_release(space_id, project_id, environment_id)
        print(f"Release Version: {release.get('Version')}", file=sys.stderr)
        
        # Get build information with commits
        print("Fetching build information...", file=sys.stderr)
        octopus_commits = get_build_information(space_id, release)
        print(f"Found {len(octopus_commits)} commits in build information", file=sys.stderr)
        
        # Get detailed commit information from GitHub
        print("Fetching commit details from GitHub...", file=sys.stderr)
        commits = []
        for octopus_commit in octopus_commits:
            commit_sha = octopus_commit.get('Id') or octopus_commit.get('CommitId')
            if commit_sha:
                commit_details = get_commit_details_from_github(commit_sha)
                commits.append(commit_details)
        
        # Filter relevant commits
        relevant_commits = [c for c in commits if is_relevant_commit(c)]
        print(f"Filtered to {len(relevant_commits)} relevant commits", file=sys.stderr)
        
        # Generate release notes
        print("Generating release notes...", file=sys.stderr)
        notes = generate_release_notes(release, relevant_commits)
        
        # Output release notes
        print(notes)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
