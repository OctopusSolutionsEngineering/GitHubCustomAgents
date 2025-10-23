#!/usr/bin/env python3
"""
Generate release notes for Octopus Deploy releases.

This script:
1. Connects to Octopus Deploy API to get the latest release
2. Extracts commit information from the release's build information
3. Fetches commit details from GitHub
4. Generates release notes in markdown format
"""

import os
import sys
import requests
import argparse
from datetime import datetime
from typing import List, Dict, Optional


class OctopusReleaseNotesGenerator:
    """Generate release notes from Octopus Deploy releases."""
    
    def __init__(self, octopus_url: str, octopus_api_key: str, github_token: Optional[str] = None):
        """
        Initialize the release notes generator.
        
        Args:
            octopus_url: Base URL of the Octopus Deploy server
            octopus_api_key: API key for Octopus Deploy
            github_token: GitHub personal access token (optional)
        """
        self.octopus_url = octopus_url.rstrip('/')
        self.octopus_api_key = octopus_api_key
        self.github_token = github_token
        self.octopus_headers = {
            'X-Octopus-ApiKey': octopus_api_key,
            'Content-Type': 'application/json'
        }
        self.github_headers = {}
        if github_token:
            self.github_headers['Authorization'] = f'token {github_token}'
    
    def get_space_id(self, space_name: str) -> str:
        """Get the space ID from the space name."""
        url = f"{self.octopus_url}/api/spaces/all"
        response = requests.get(url, headers=self.octopus_headers)
        response.raise_for_status()
        
        spaces = response.json()
        for space in spaces:
            if space['Name'] == space_name:
                return space['Id']
        
        raise ValueError(f"Space '{space_name}' not found")
    
    def get_project_id(self, space_id: str, project_name: str) -> str:
        """Get the project ID from the project name."""
        url = f"{self.octopus_url}/api/{space_id}/projects/all"
        response = requests.get(url, headers=self.octopus_headers)
        response.raise_for_status()
        
        projects = response.json()
        for project in projects:
            if project['Name'] == project_name:
                return project['Id']
        
        raise ValueError(f"Project '{project_name}' not found")
    
    def get_environment_id(self, space_id: str, environment_name: str) -> str:
        """Get the environment ID from the environment name."""
        url = f"{self.octopus_url}/api/{space_id}/environments/all"
        response = requests.get(url, headers=self.octopus_headers)
        response.raise_for_status()
        
        environments = response.json()
        for environment in environments:
            if environment['Name'] == environment_name:
                return environment['Id']
        
        raise ValueError(f"Environment '{environment_name}' not found")
    
    def get_latest_deployment(self, space_id: str, project_id: str, environment_id: str) -> Dict:
        """Get the latest deployment for a project and environment."""
        url = f"{self.octopus_url}/api/{space_id}/deployments"
        params = {
            'projects': project_id,
            'environments': environment_id,
            'take': 1
        }
        response = requests.get(url, headers=self.octopus_headers, params=params)
        response.raise_for_status()
        
        deployments = response.json()
        if not deployments.get('Items'):
            raise ValueError(f"No deployments found for project and environment")
        
        return deployments['Items'][0]
    
    def get_release(self, space_id: str, release_id: str) -> Dict:
        """Get release details."""
        url = f"{self.octopus_url}/api/{space_id}/releases/{release_id}"
        response = requests.get(url, headers=self.octopus_headers)
        response.raise_for_status()
        return response.json()
    
    def get_build_information(self, space_id: str, release: Dict) -> List[Dict]:
        """Get build information associated with the release."""
        build_info_list = []
        
        # Get build information from the release
        if 'BuildInformation' in release:
            for build_info_ref in release['BuildInformation']:
                build_info_id = build_info_ref.get('Id')
                if build_info_id:
                    url = f"{self.octopus_url}/api/{space_id}/build-information/{build_info_id}"
                    response = requests.get(url, headers=self.octopus_headers)
                    if response.status_code == 200:
                        build_info_list.append(response.json())
        
        return build_info_list
    
    def get_commit_details_from_github(self, repo_owner: str, repo_name: str, commit_sha: str) -> Dict:
        """Get commit details from GitHub."""
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
        response = requests.get(url, headers=self.github_headers)
        response.raise_for_status()
        return response.json()
    
    def extract_commits_from_build_info(self, build_info_list: List[Dict]) -> List[Dict]:
        """Extract commit information from build information."""
        commits = []
        
        for build_info in build_info_list:
            if 'Commits' in build_info:
                for commit in build_info['Commits']:
                    commits.append({
                        'id': commit.get('Id'),
                        'comment': commit.get('Comment', ''),
                        'linkUrl': commit.get('LinkUrl', '')
                    })
        
        return commits
    
    def parse_github_url(self, url: str) -> tuple:
        """Parse GitHub URL to extract owner and repo."""
        # Expected format: https://github.com/owner/repo/commit/sha
        # Use proper URL parsing to avoid security issues
        from urllib.parse import urlparse
        
        try:
            parsed = urlparse(url)
            # Verify it's actually a GitHub URL
            if parsed.netloc != 'github.com':
                return None, None
            
            # Path should be /owner/repo/...
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2:
                return path_parts[0], path_parts[1]
        except Exception:
            pass
        
        return None, None
    
    def generate_release_notes(self, space_name: str, project_name: str, environment_name: str) -> str:
        """
        Generate release notes for the latest release.
        
        Args:
            space_name: Name of the Octopus space
            project_name: Name of the Octopus project
            environment_name: Name of the Octopus environment
            
        Returns:
            Markdown formatted release notes
        """
        # Get IDs from names
        print(f"Getting space ID for '{space_name}'...")
        space_id = self.get_space_id(space_name)
        
        print(f"Getting project ID for '{project_name}'...")
        project_id = self.get_project_id(space_id, project_name)
        
        print(f"Getting environment ID for '{environment_name}'...")
        environment_id = self.get_environment_id(space_id, environment_name)
        
        # Get latest deployment
        print(f"Getting latest deployment...")
        deployment = self.get_latest_deployment(space_id, project_id, environment_id)
        
        # Get release details
        release_id = deployment['ReleaseId']
        print(f"Getting release details for {release_id}...")
        release = self.get_release(space_id, release_id)
        
        # Get build information
        print(f"Getting build information...")
        build_info_list = self.get_build_information(space_id, release)
        
        # Extract commits
        commits = self.extract_commits_from_build_info(build_info_list)
        
        # Generate release notes
        release_notes = f"# Release Notes: {release['Version']}\n\n"
        release_notes += f"**Project:** {project_name}\n"
        release_notes += f"**Environment:** {environment_name}\n"
        release_notes += f"**Release Date:** {deployment.get('Created', 'N/A')}\n\n"
        release_notes += "## Changes\n\n"
        
        if not commits:
            release_notes += "No commit information available.\n"
        else:
            for commit in commits:
                commit_sha = commit['id']
                commit_message = commit['comment']
                commit_url = commit['linkUrl']
                
                # Try to get more details from GitHub if we have a token
                if self.github_token and commit_url:
                    owner, repo = self.parse_github_url(commit_url)
                    if owner and repo:
                        try:
                            github_commit = self.get_commit_details_from_github(owner, repo, commit_sha)
                            author = github_commit['commit']['author']['name']
                            date = github_commit['commit']['author']['date']
                            
                            release_notes += f"- **{commit_message}**\n"
                            release_notes += f"  - Author: {author}\n"
                            release_notes += f"  - Date: {date}\n"
                            release_notes += f"  - Commit: [{commit_sha[:7]}]({commit_url})\n\n"
                        except Exception as e:
                            print(f"Warning: Could not fetch GitHub details for commit {commit_sha}: {e}")
                            release_notes += f"- {commit_message} ([{commit_sha[:7]}]({commit_url}))\n"
                    else:
                        release_notes += f"- {commit_message} ([{commit_sha[:7]}]({commit_url}))\n"
                else:
                    # Basic format without GitHub details
                    if commit_url:
                        release_notes += f"- {commit_message} ([{commit_sha[:7]}]({commit_url}))\n"
                    else:
                        release_notes += f"- {commit_message} ({commit_sha[:7]})\n"
        
        return release_notes


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate release notes from Octopus Deploy')
    parser.add_argument('--space', required=True, help='Octopus space name')
    parser.add_argument('--project', required=True, help='Octopus project name')
    parser.add_argument('--environment', required=True, help='Octopus environment name')
    parser.add_argument('--octopus-url', help='Octopus server URL (default: from OCTOPUS_URL env var)')
    parser.add_argument('--octopus-api-key', help='Octopus API key (default: from OCTOPUS_API_KEY env var)')
    parser.add_argument('--github-token', help='GitHub token (default: from GITHUB_TOKEN env var)')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    # Get configuration from args or environment
    octopus_url = args.octopus_url or os.getenv('OCTOPUS_URL')
    octopus_api_key = args.octopus_api_key or os.getenv('OCTOPUS_API_KEY')
    github_token = args.github_token or os.getenv('GITHUB_TOKEN')
    
    if not octopus_url:
        print("Error: Octopus URL is required (--octopus-url or OCTOPUS_URL env var)", file=sys.stderr)
        sys.exit(1)
    
    if not octopus_api_key:
        print("Error: Octopus API key is required (--octopus-api-key or OCTOPUS_API_KEY env var)", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create generator
        generator = OctopusReleaseNotesGenerator(octopus_url, octopus_api_key, github_token)
        
        # Generate release notes
        release_notes = generator.generate_release_notes(
            args.space,
            args.project,
            args.environment
        )
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(release_notes)
            print(f"Release notes written to {args.output}")
        else:
            print(release_notes)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
