# Release Notes Generation Guide

## Overview

This document explains how to generate release notes for the "Octopus Copilot Function" project deployed to the "Production" environment in the "Octopus Copilot" space.

## Prerequisites

1. **Octopus Deploy Access**
   - Octopus Server URL
   - API Key with read access to:
     - Spaces
     - Projects
     - Releases
     - Deployments
     - Build Information

2. **GitHub Access**
   - Access to the repository containing the source code
   - Ability to read commit history and diffs

## Setup

### Environment Variables

Set the following environment variables:

```bash
export OCTOPUS_SERVER="https://your-octopus-server.com"
export OCTOPUS_API_KEY="API-XXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Using the MCP Server

If you're using the Octopus Deploy MCP Server (as configured in `.github/agents/releasenotes.md`), the following tools are available:

- `list_spaces` - List all Octopus spaces
- `list_projects` - List all projects in a space
- `list_environments` - List all environments
- `list_deployments` - List deployments for filtering
- `list_releases_for_project` - Get releases for a specific project
- `get_release_by_id` - Get detailed release information including build information

## Process

### Step 1: Get Space, Project, and Environment IDs

1. Use `list_spaces` to find the "Octopus Copilot" space ID
2. Use `list_projects` with the space ID to find "Octopus Copilot Function" project ID
3. Use `list_environments` with the space ID to find "Production" environment ID

### Step 2: Get Latest Release

1. Use `list_deployments` filtered by:
   - Project ID
   - Environment ID
   - Take: 1 (most recent)
2. Extract the Release ID from the latest deployment
3. Use `get_release_by_id` to get full release details

### Step 3: Extract Commit Information

From the release object, extract:
- Build Information section
- For each build info entry, get the commits array
- Each commit contains:
  - Commit SHA/ID
  - Commit message
  - Author information
  - Date/timestamp

### Step 4: Enrich with GitHub Data

For each commit SHA:
1. Use GitHub API or git commands to fetch:
   - Full commit message (including body)
   - Author name and email
   - Commit date
   - File changes (diff stats)
   - Modified files list

### Step 5: Generate Release Notes

Create a markdown document with:

1. **Header Section**
   - Project name
   - Version/release number
   - Release date
   - Environment
   - Space

2. **Summary Section**
   - Total number of commits
   - High-level overview

3. **Changes by Category**
   - Features (feat:, feature)
   - Bug Fixes (fix:, bug)
   - Improvements (perf:, refactor:, improve)
   - Other changes

4. **Detailed Commit Information**
   - Full commit details
   - Author
   - Date
   - Diff statistics

5. **Contributors Section**
   - List of unique contributors

## Filtering Commits

The following commits are filtered out as irrelevant:

- Automated merge commits
- Formatting/whitespace only changes
- Comment-only changes
- README updates (unless substantial)
- CI configuration changes (unless mentioned otherwise)

## Output Format

The release notes are generated in Markdown format and include:

- Emoji indicators for different change types
- Code blocks for commit messages and diffs
- Collapsible sections for detailed information
- Links to commits (when connected to GitHub)

## Example Usage

### Using the Python Script

```bash
# With Octopus credentials
export OCTOPUS_SERVER="https://your-server.octopus.app"
export OCTOPUS_API_KEY="API-XXXXXXXXXX"
python3 generate_release_notes.py

# Demo mode (uses recent commits from current repo)
python3 generate_release_notes.py
```

### Output

The script outputs the release notes to stdout, which can be redirected to a file:

```bash
python3 generate_release_notes.py > RELEASE_NOTES.md
```

## Customization

You can customize the release notes by modifying:

1. **Filtering Logic** - Adjust `is_relevant_commit()` function
2. **Categorization** - Modify how commits are grouped
3. **Format** - Change the markdown template in `generate_release_notes()`
4. **Diff Detail** - Adjust how much diff information is included

## Troubleshooting

### No Octopus Credentials

If Octopus credentials are not provided, the script runs in demo mode using recent commits from the local repository.

### Missing Commits

Ensure the repository is fully cloned (not shallow) to access all commit history:

```bash
git fetch --unshallow
```

### API Rate Limits

If hitting GitHub API rate limits, consider:
- Using git commands instead of API calls
- Implementing caching
- Using authenticated requests

## Integration

This can be integrated into:

1. **CI/CD Pipeline** - Automatically generate on release
2. **Octopus Deployment** - Trigger after successful deployment
3. **GitHub Actions** - Create release notes on tag push
4. **Manual Process** - Run on-demand for any release

## See Also

- [Octopus Deploy API Documentation](https://octopus.com/docs/octopus-rest-api)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Conventional Commits](https://www.conventionalcommits.org/)
