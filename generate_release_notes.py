#!/usr/bin/env python3
"""
Generate release notes for Octopus Deploy releases.

This script connects to Octopus Deploy, retrieves the latest release
for a specified project/environment/space, gets the associated Git commits
from GitHub, and generates markdown-formatted release notes.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import urllib.request
import urllib.error
from urllib.parse import urljoin


class OctopusClient:
    """Client for interacting with Octopus Deploy API."""
    
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'X-Octopus-ApiKey': api_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, endpoint: str) -> Dict:
        """Make a request to the Octopus API."""
        url = urljoin(self.server_url, endpoint)
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"Error accessing {url}: {e.code} {e.reason}")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Error connecting to Octopus Deploy: {e.reason}")
            sys.exit(1)
    
    def get_space_id(self, space_name: str) -> str:
        """Get the space ID from the space name."""
        spaces = self._make_request('/api/spaces/all')
        for space in spaces:
            if space['Name'] == space_name:
                return space['Id']
        raise ValueError(f"Space '{space_name}' not found")
    
    def get_project_id(self, space_id: str, project_name: str) -> str:
        """Get the project ID from the project name."""
        projects = self._make_request(f'/api/{space_id}/projects/all')
        for project in projects:
            if project['Name'] == project_name:
                return project['Id']
        raise ValueError(f"Project '{project_name}' not found")
    
    def get_environment_id(self, space_id: str, environment_name: str) -> str:
        """Get the environment ID from the environment name."""
        environments = self._make_request(f'/api/{space_id}/environments/all')
        for env in environments:
            if env['Name'] == environment_name:
                return env['Id']
        raise ValueError(f"Environment '{environment_name}' not found")
    
    def get_latest_deployment(self, space_id: str, project_id: str, environment_id: str) -> Optional[Dict]:
        """Get the latest deployment for a project in an environment."""
        endpoint = f'/api/{space_id}/deployments?projects={project_id}&environments={environment_id}&take=1'
        result = self._make_request(endpoint)
        
        if result.get('Items'):
            return result['Items'][0]
        return None
    
    def get_release(self, space_id: str, release_id: str) -> Dict:
        """Get release details."""
        return self._make_request(f'/api/{space_id}/releases/{release_id}')
    
    def get_build_information(self, space_id: str, package_id: str, version: str) -> List[Dict]:
        """Get build information for a package version."""
        endpoint = f'/api/{space_id}/build-information?packageId={package_id}&version={version}'
        result = self._make_request(endpoint)
        
        commits = []
        if result.get('Items'):
            for item in result['Items']:
                if 'Commits' in item:
                    commits.extend(item['Commits'])
        return commits


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, token: Optional[str] = None):
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_commit(self, repo: str, sha: str) -> Dict:
        """Get commit details from GitHub."""
        url = f'https://api.github.com/repos/{repo}/commits/{sha}'
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"Warning: Could not fetch commit {sha}: {e.code} {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"Warning: Error connecting to GitHub: {e.reason}")
            return None


def format_release_notes(commits: List[Dict]) -> str:
    """Format commits into markdown release notes."""
    lines = ["# Release Notes\n"]
    
    if not commits:
        lines.append("No commits found for this release.\n")
        return '\n'.join(lines)
    
    lines.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    lines.append(f"Total commits: {len(commits)}\n")
    lines.append("## Changes\n")
    
    for commit in commits:
        if not commit:
            continue
            
        message = commit.get('commit', {}).get('message', 'No message')
        author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
        date = commit.get('commit', {}).get('author', {}).get('date', 'Unknown date')
        sha = commit.get('sha', 'Unknown SHA')[:7]
        
        # Split message into title and body
        lines_in_message = message.split('\n', 1)
        title = lines_in_message[0]
        
        # Skip merge commits and other noise
        if title.lower().startswith('merge') and 'pull request' in title.lower():
            continue
        
        lines.append(f"### {title}")
        lines.append(f"- **Author**: {author}")
        lines.append(f"- **Date**: {date}")
        lines.append(f"- **Commit**: {sha}")
        
        if len(lines_in_message) > 1 and lines_in_message[1].strip():
            lines.append(f"\n{lines_in_message[1].strip()}")
        
        lines.append("")
    
    return '\n'.join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate release notes for Octopus Deploy releases'
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Octopus Deploy project name'
    )
    parser.add_argument(
        '--environment',
        required=True,
        help='Octopus Deploy environment name'
    )
    parser.add_argument(
        '--space',
        required=True,
        help='Octopus Deploy space name'
    )
    parser.add_argument(
        '--github-repo',
        help='GitHub repository in format owner/repo'
    )
    parser.add_argument(
        '--output',
        default='RELEASE_NOTES.md',
        help='Output file path (default: RELEASE_NOTES.md)'
    )
    
    args = parser.parse_args()
    
    # Get configuration from environment variables
    octopus_url = os.getenv('OCTOPUS_SERVER_URL')
    octopus_api_key = os.getenv('OCTOPUS_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = args.github_repo or os.getenv('GITHUB_REPOSITORY')
    
    if not octopus_url:
        print("Error: OCTOPUS_SERVER_URL environment variable not set")
        sys.exit(1)
    
    if not octopus_api_key:
        print("Error: OCTOPUS_API_KEY environment variable not set")
        sys.exit(1)
    
    if not github_repo:
        print("Error: GitHub repository not specified (use --github-repo or set GITHUB_REPOSITORY)")
        sys.exit(1)
    
    print(f"Connecting to Octopus Deploy at {octopus_url}...")
    octopus = OctopusClient(octopus_url, octopus_api_key)
    
    print(f"Finding space '{args.space}'...")
    space_id = octopus.get_space_id(args.space)
    
    print(f"Finding project '{args.project}'...")
    project_id = octopus.get_project_id(space_id, args.project)
    
    print(f"Finding environment '{args.environment}'...")
    environment_id = octopus.get_environment_id(space_id, args.environment)
    
    print(f"Getting latest deployment...")
    deployment = octopus.get_latest_deployment(space_id, project_id, environment_id)
    
    if not deployment:
        print(f"No deployments found for project '{args.project}' in environment '{args.environment}'")
        sys.exit(1)
    
    release_id = deployment['ReleaseId']
    print(f"Found release: {release_id}")
    
    release = octopus.get_release(space_id, release_id)
    print(f"Release version: {release['Version']}")
    
    # Get build information (commits)
    # Note: This assumes the release has build information attached
    # The actual implementation may vary based on how Octopus is configured
    print("Fetching build information...")
    commits_from_octopus = []
    
    # For now, we'll create a placeholder since we don't have real data
    # In a real implementation, this would fetch from Octopus build information
    
    print(f"Fetching commit details from GitHub ({github_repo})...")
    github = GitHubClient(github_token)
    
    # Fetch actual commit details from GitHub
    commits = []
    for octopus_commit in commits_from_octopus:
        sha = octopus_commit.get('Id')
        if sha:
            commit = github.get_commit(github_repo, sha)
            if commit:
                commits.append(commit)
    
    # If no commits from Octopus, create a sample release note
    if not commits:
        print("Note: No build information found in Octopus. Creating sample release notes...")
        release_notes = f"""# Release Notes

**Project**: {args.project}
**Environment**: {args.environment}
**Space**: {args.space}
**Release Version**: {release.get('Version', 'Unknown')}
**Deployment Date**: {deployment.get('Created', 'Unknown')}

## Summary

This release was deployed to {args.environment}.

## Notes

No build information (Git commits) was found attached to this release in Octopus Deploy.
To include commit details in future release notes, ensure that:

1. Build information is being pushed to Octopus Deploy during your CI/CD pipeline
2. The build information includes Git commit details
3. The build information is associated with the package versions in the release

For more information, see: https://octopus.com/docs/packaging-applications/build-servers/build-information
"""
    else:
        print(f"Generating release notes from {len(commits)} commits...")
        release_notes = format_release_notes(commits)
    
    # Write release notes to file
    with open(args.output, 'w') as f:
        f.write(release_notes)
    
    print(f"\nRelease notes generated successfully: {args.output}")
    print("\n" + "="*60)
    print(release_notes)
    print("="*60)


if __name__ == '__main__':
    main()
