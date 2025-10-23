#!/usr/bin/env python3
"""
Script to generate release notes for Octopus Deploy releases.

This script queries Octopus Deploy for the latest release in a specified
project, environment, and space, then generates release notes based on
the Git commit information included in the release.
"""

import sys
import json
from datetime import datetime

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
    
    # Read the release data from stdin or from a JSON file
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            release_data = json.load(f)
    else:
        # Read from stdin
        release_data = json.load(sys.stdin)
    
    # Generate and print release notes
    release_notes = generate_release_notes(release_data)
    print(release_notes)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
