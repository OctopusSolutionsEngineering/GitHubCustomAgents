#!/usr/bin/env python3
"""
Generate release notes for an Octopus Deploy release.

This script uses the Octopus Deploy and GitHub MCP servers to:
1. Get the latest release deployed to a specific project, environment, and space in Octopus Deploy
2. Extract Git commit information from the release build information
3. Get detailed commit information from GitHub (message, author, date, diff)
4. Generate release notes in markdown format

Requirements:
- Octopus Deploy MCP server configured with valid API key
- GitHub MCP server configured with valid credentials
- Access to the specified Octopus space, project, and environment
"""

import os
import sys
import json
from datetime import datetime


# NOTE: This script is designed to work with MCP (Model Context Protocol) servers
# In a real implementation, these functions would make calls to the MCP servers
# through the appropriate API/SDK. For now, they demonstrate the workflow.


def get_latest_deployment(space_name, project_name, environment_name):
    """
    Get the latest deployment for a specific project and environment in Octopus Deploy.
    
    This function uses the Octopus Deploy MCP server tools to:
    1. List spaces (octopusdeploy-list_spaces) to find the space by name
    2. List projects (octopusdeploy-list_projects) to find the project by name
    3. List environments (octopusdeploy-list_environments) to find the environment by name  
    4. List deployments (octopusdeploy-list_deployments) filtered by project and environment
    5. Get release details (octopusdeploy-get_release_by_id) for the most recent deployment
    
    Args:
        space_name: Name of the Octopus space
        project_name: Name of the project
        environment_name: Name of the environment
        
    Returns:
        Dictionary containing deployment information including:
        - space: Space name
        - project: Project name
        - environment: Environment name
        - release_version: Version number of the release
        - deployed_at: Timestamp of deployment
        - release_id: Octopus release ID
        - commits: List of commit information from build metadata
    """
    print(f"📦 Fetching latest deployment for:")
    print(f"   Space: {space_name}")
    print(f"   Project: {project_name}")
    print(f"   Environment: {environment_name}")
    print()
    
    # In actual implementation with MCP server:
    # 1. Call octopusdeploy-list_spaces(partialName=space_name) to get space ID
    # 2. Call octopusdeploy-list_projects(spaceName=space_name, partialName=project_name) to get project ID
    # 3. Call octopusdeploy-list_environments(spaceName=space_name, partialName=environment_name) to get environment ID
    # 4. Call octopusdeploy-list_deployments(spaceName=space_name, projects=[project_id], environments=[environment_id], taskState="Success") 
    # 5. Sort by deployed date and get most recent
    # 6. Call octopusdeploy-get_release_by_id(spaceName=space_name, releaseId=release_id) to get full release details including build information
    
    # For demonstration, returning a sample structure that shows what the actual data would look like
    # The commits list would come from the release's BuildInformation metadata
    return {
        'space': space_name,
        'project': project_name,
        'environment': environment_name,
        'release_version': '1.0.0',
        'deployed_at': datetime.now().isoformat(),
        'release_id': 'Releases-123',
        'commits': [
            {
                'sha': 'abc123def456',
                'repository': 'owner/repo'
            }
        ]
    }


def get_commit_details(repository, commit_sha):
    """
    Get detailed commit information from GitHub.
    
    This function uses the GitHub MCP server to get commit details:
    - Calls github-mcp-server-get_commit(owner, repo, sha, include_diff=True)
    
    Args:
        repository: Repository in format 'owner/repo'
        commit_sha: Git commit SHA
        
    Returns:
        Dictionary containing commit details:
        - sha: Commit SHA
        - message: Commit message
        - author: Author name
        - date: Commit date
        - stats: File change statistics
        - diff: Unified diff of changes
    """
    print(f"🔍 Fetching commit details for {commit_sha} in {repository}")
    
    # Parse repository into owner and repo
    owner, repo = repository.split('/')
    
    # In actual implementation with MCP server:
    # Call github-mcp-server-get_commit(owner=owner, repo=repo, sha=commit_sha, include_diff=True)
    # Extract commit message, author name, commit date, and diff from response
    
    # For demonstration, returning a sample structure
    return {
        'sha': commit_sha,
        'message': 'Sample commit message',
        'author': 'John Doe',
        'date': datetime.now().isoformat(),
        'stats': {
            'additions': 10,
            'deletions': 5,
            'total': 15
        },
        'diff': '+ Added new feature\n- Removed old code'
    }


def generate_release_notes(deployment, commits):
    """
    Generate markdown-formatted release notes.
    
    Summarizes the changes from Git commits, filtering out irrelevant commits
    such as merge commits and minor formatting changes.
    
    Args:
        deployment: Deployment information dictionary
        commits: List of commit detail dictionaries
        
    Returns:
        String containing markdown-formatted release notes
    """
    notes = []
    
    # Header
    notes.append(f"# Release Notes - {deployment['project']}")
    notes.append(f"")
    notes.append(f"**Version:** {deployment['release_version']}")
    notes.append(f"**Environment:** {deployment['environment']}")
    notes.append(f"**Space:** {deployment['space']}")
    notes.append(f"**Deployed:** {deployment['deployed_at']}")
    notes.append("")
    notes.append("---")
    notes.append("")
    
    # Changes section
    notes.append("## Changes")
    notes.append("")
    
    if not commits:
        notes.append("*No commits found in this release.*")
    else:
        included_count = 0
        skipped_count = 0
        
        for commit in commits:
            # Skip irrelevant commits (e.g., merge commits, minor formatting)
            if should_include_commit(commit['message']):
                included_count += 1
                # Get first line of commit message as title
                message_lines = commit['message'].split('\n')
                title = message_lines[0]
                
                notes.append(f"### {title}")
                notes.append("")
                notes.append(f"- **Author:** {commit['author']}")
                notes.append(f"- **Date:** {commit['date']}")
                notes.append(f"- **Commit:** `{commit['sha'][:7]}`")
                
                # Add additional lines of commit message if present
                if len(message_lines) > 1:
                    notes.append("")
                    for line in message_lines[1:]:
                        if line.strip():
                            notes.append(f"{line}")
                
                # Add summary of changes if available
                if commit.get('stats'):
                    stats = commit['stats']
                    notes.append("")
                    notes.append(f"**Changes:** +{stats.get('additions', 0)} / -{stats.get('deletions', 0)} lines")
                
                notes.append("")
            else:
                skipped_count += 1
        
        # Add summary footer
        notes.append("---")
        notes.append("")
        notes.append(f"*Total: {included_count} commit(s) included, {skipped_count} commit(s) skipped*")
    
    return "\n".join(notes)


def should_include_commit(message):
    """
    Determine if a commit should be included in release notes.
    
    Args:
        message: Commit message
        
    Returns:
        Boolean indicating if commit should be included
    """
    # Skip merge commits
    if message.lower().startswith('merge'):
        return False
    
    # Skip minor formatting/whitespace changes
    skip_keywords = ['formatting', 'whitespace', 'typo', 'minor fix']
    if any(keyword in message.lower() for keyword in skip_keywords):
        return False
    
    return True


def main():
    """Main function to generate release notes."""
    # Parse command line arguments
    if len(sys.argv) != 4:
        print("Usage: python generate_release_notes.py <space> <project> <environment>")
        print()
        print("Example:")
        print('  python generate_release_notes.py "Octopus Copilot" "Octopus Copilot Function" "Production"')
        sys.exit(1)
    
    space_name = sys.argv[1]
    project_name = sys.argv[2]
    environment_name = sys.argv[3]
    
    print("=" * 80)
    print("Octopus Deploy Release Notes Generator")
    print("=" * 80)
    print()
    
    # Step 1: Get the latest deployment
    deployment = get_latest_deployment(space_name, project_name, environment_name)
    
    # Step 2: Get commit details for each commit in the release
    commits = []
    for commit_info in deployment.get('commits', []):
        commit_details = get_commit_details(
            commit_info['repository'],
            commit_info['sha']
        )
        commits.append(commit_details)
    
    print()
    
    # Step 3: Generate release notes
    release_notes = generate_release_notes(deployment, commits)
    
    # Output the release notes
    print("=" * 80)
    print("Generated Release Notes")
    print("=" * 80)
    print()
    print(release_notes)
    
    # Also save to a file
    output_file = f"release_notes_{deployment['release_version']}.md"
    with open(output_file, 'w') as f:
        f.write(release_notes)
    
    print()
    print(f"📝 Release notes saved to: {output_file}")


if __name__ == '__main__':
    main()
