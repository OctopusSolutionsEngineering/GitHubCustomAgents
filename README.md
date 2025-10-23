# Octopus Deploy Release Notes Generator

This repository contains a tool for generating release notes from Octopus Deploy deployments.

## Overview

The `generate_release_notes.py` script generates comprehensive release notes for Octopus Deploy releases by:

1. Querying Octopus Deploy for the latest deployment to a specific project, environment, and space
2. Extracting commit information from the release's build metadata
3. Fetching detailed commit information from GitHub (messages, authors, dates, diffs)
4. Generating well-formatted markdown release notes

## Requirements

- Python 3.x
- Access to Octopus Deploy MCP server (with valid API key)
- Access to GitHub MCP server (with valid credentials)
- Permissions to access the specified Octopus space, project, and environment

## Usage

```bash
python3 generate_release_notes.py <space> <project> <environment>
```

### Example

```bash
python3 generate_release_notes.py "Octopus Copilot" "Octopus Copilot Function" "Production"
```

This will:
- Query Octopus Deploy for the latest deployment of "Octopus Copilot Function" to "Production" in the "Octopus Copilot" space
- Fetch commit details from GitHub
- Generate release notes and save them to `release_notes_<version>.md`

## Output

The script generates a markdown file with the following structure:

- Release header with version, environment, space, and deployment date
- List of changes with commit details (message, author, date, stats)
- Summary of included/skipped commits

### Sample Output

```markdown
# Release Notes - Octopus Copilot Function

**Version:** 1.0.0
**Environment:** Production
**Space:** Octopus Copilot
**Deployed:** 2025-10-23T23:18:24.524629

---

## Changes

### Added new feature

- **Author:** John Doe
- **Date:** 2025-10-23T23:18:24
- **Commit:** `abc123d`

**Changes:** +10 / -5 lines

---

*Total: 1 commit(s) included, 0 commit(s) skipped*
```

## How It Works

### 1. Get Latest Deployment

Uses Octopus Deploy MCP server tools:
- `octopusdeploy-list_spaces` - Find the space by name
- `octopusdeploy-list_projects` - Find the project by name
- `octopusdeploy-list_environments` - Find the environment by name
- `octopusdeploy-list_deployments` - Get deployments for the project/environment
- `octopusdeploy-get_release_by_id` - Get release details including build information

### 2. Get Commit Details

Uses GitHub MCP server tools:
- `github-mcp-server-get_commit` - Fetch commit message, author, date, and diff for each commit

### 3. Generate Release Notes

- Filters out irrelevant commits (merges, formatting changes, etc.)
- Formats commits into readable markdown
- Includes commit statistics and metadata
- Saves output to a timestamped file

## Filtering

The script automatically filters out:
- Merge commits (starting with "merge")
- Minor formatting changes
- Whitespace-only changes
- Typo fixes

This ensures the release notes focus on meaningful changes.

## Customization

You can modify the `should_include_commit()` function to customize which commits are included in the release notes.

## MCP Server Integration

This script is designed to work with the Model Context Protocol (MCP) servers for Octopus Deploy and GitHub. These servers must be properly configured with authentication credentials before running the script.
