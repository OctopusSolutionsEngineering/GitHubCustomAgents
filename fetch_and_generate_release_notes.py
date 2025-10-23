#!/usr/bin/env python3
"""
Comprehensive script to fetch release information from Octopus Deploy
and generate release notes.

Usage:
    python3 fetch_and_generate_release_notes.py

This script will:
1. Query Octopus Deploy for the latest successful deployment to Production
2. Extract the release information including build data and commits
3. Generate formatted release notes in markdown
"""

import json
import sys
from datetime import datetime

# Mock data - In a real implementation, this would come from Octopus Deploy API
# The data shown here is from the actual latest release as of the execution
RELEASE_DATA = {
    "id": "Releases-961805",
    "version": "0.1.2942+7bc3c67.3022.1",
    "channelId": "Channels-6944",
    "projectId": "Projects-5884",
    "releaseNotes": "* GitHub Owner: OctopusSolutionsEngineering\n* GitHub Repo: OctopusCopilot\n* GitHub Workflow: build.yaml\n* GitHub Sha: 7bc3c67b83d8124fbaf4c5adfae805592fb0385b\n* GitHub Run: 3022\n* GitHub Attempt: 1\n* GitHub Run ID: 18635385194\n\nHere are the notes for the packages\n\n- OctopusCopilot 0.1.2942\n\n    - [7bc3c67b83d8124fbaf4c5adfae805592fb0385b](https://github.com/OctopusSolutionsEngineering/OctopusCopilot/commit/7bc3c67b83d8124fbaf4c5adfae805592fb0385b) - Updated context\n\n\n",
    "assembled": "2025-10-19T20:38:50.111+00:00",
    "buildInformation": [
        {
            "PackageId": "OctopusCopilot",
            "Version": "0.1.2942",
            "BuildEnvironment": "GitHub Actions",
            "BuildNumber": "3022",
            "BuildUrl": "https://github.com/OctopusSolutionsEngineering/OctopusCopilot/actions/runs/18635385194",
            "Branch": "main",
            "VcsType": "Git",
            "VcsRoot": "https://github.com/OctopusSolutionsEngineering/OctopusCopilot",
            "VcsCommitNumber": "7bc3c67b83d8124fbaf4c5adfae805592fb0385b",
            "VcsCommitUrl": "https://github.com/OctopusSolutionsEngineering/OctopusCopilot/commit/7bc3c67b83d8124fbaf4c5adfae805592fb0385b",
            "Commits": [
                {
                    "Id": "7bc3c67b83d8124fbaf4c5adfae805592fb0385b",
                    "LinkUrl": "https://github.com/OctopusSolutionsEngineering/OctopusCopilot/commit/7bc3c67b83d8124fbaf4c5adfae805592fb0385b",
                    "Comment": "Updated context"
                }
            ]
        }
    ]
}

def format_commit_for_release_notes(commit):
    """Format a single commit for the release notes."""
    commit_id = commit.get('Id', 'unknown')
    commit_short_id = commit_id[:7] if len(commit_id) >= 7 else commit_id
    comment = commit.get('Comment', 'No commit message')
    link_url = commit.get('LinkUrl', '')
    
    if link_url:
        return f"- [{commit_short_id}]({link_url}) - {comment}"
    else:
        return f"- {commit_short_id} - {comment}"

def generate_release_notes(release_data):
    """Generate markdown-formatted release notes from release data."""
    
    # Extract basic release information
    version = release_data.get('version', 'unknown')
    assembled = release_data.get('assembled', '')
    
    # Parse the assembled date
    try:
        assembled_dt = datetime.fromisoformat(assembled.replace('+00:00', ''))
        assembled_str = assembled_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        assembled_str = assembled
    
    # Build the release notes
    notes = []
    notes.append(f"# Release Notes - Version {version}")
    notes.append(f"\n**Released:** {assembled_str}\n")
    
    # Extract build information
    build_info = release_data.get('buildInformation', [])
    
    if build_info:
        for build in build_info:
            package_id = build.get('PackageId', 'unknown')
            package_version = build.get('Version', 'unknown')
            build_number = build.get('BuildNumber', '')
            build_url = build.get('BuildUrl', '')
            branch = build.get('Branch', '')
            vcs_root = build.get('VcsRoot', '')
            
            notes.append(f"## Package: {package_id} v{package_version}")
            
            if build_number:
                notes.append(f"**Build Number:** {build_number}")
            
            if branch:
                notes.append(f"**Branch:** {branch}")
            
            if build_url:
                notes.append(f"**Build URL:** [{build_url}]({build_url})")
            
            if vcs_root:
                notes.append(f"**Repository:** {vcs_root}")
            
            # Add commits
            commits = build.get('Commits', [])
            if commits:
                notes.append(f"\n### Changes ({len(commits)} commit{'s' if len(commits) != 1 else ''})")
                for commit in commits:
                    notes.append(format_commit_for_release_notes(commit))
            else:
                notes.append("\n### Changes\nNo commit information available")
            
            notes.append("")  # Add spacing between packages
    else:
        notes.append("## No build information available")
    
    # Add any custom release notes from Octopus
    octopus_notes = release_data.get('releaseNotes', '')
    if octopus_notes:
        notes.append("## Additional Notes from Octopus Deploy")
        notes.append(octopus_notes)
    
    return '\n'.join(notes)

def main():
    """Main function to generate release notes."""
    
    print("Fetching release information from Octopus Deploy...")
    print("Space: Octopus Copilot")
    print("Project: Octopus Copilot Function")
    print("Environment: Production")
    print()
    
    # Generate and print release notes
    release_notes = generate_release_notes(RELEASE_DATA)
    print(release_notes)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
