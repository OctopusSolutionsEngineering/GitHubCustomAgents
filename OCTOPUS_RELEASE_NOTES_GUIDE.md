# Octopus Deploy Release Notes Generator Guide

## Overview

This guide explains how to generate release notes for an Octopus Deploy project by extracting commit information from GitHub.

## Problem Statement

Generate release notes for the latest release of project **"Octopus Copilot Function"** in the **"Production"** environment.

## Prerequisites

Before running the release notes generator, ensure:

1. **Octopus Deploy Server Access**
   - Server URL must be configured
   - API key must be available
   - Currently getting "Invalid URL" error - Octopus server configuration needed

2. **GitHub Access**
   - Repository access for commit details
   - Available through GitHub MCP server tools

3. **Space Name**
   - The problem statement appears incomplete ("in the sp...")
   - Common space names: "Default", "Production", etc.
   - This needs to be provided to complete the task

## Workflow

### Step 1: List Available Spaces

Use the Octopus Deploy MCP tool to list all spaces:

```javascript
octopusdeploy-list_spaces()
```

Verify the space exists and get its exact name.

### Step 2: Find the Project

List projects in the space to find "Octopus Copilot Function":

```javascript
octopusdeploy-list_projects({
  spaceName: "<space-name>",
  partialName: "Octopus Copilot Function"
})
```

Extract the project ID from the results.

### Step 3: Find the Environment

List environments to find "Production":

```javascript
octopusdeploy-list_environments({
  spaceName: "<space-name>",
  partialName: "Production"
})
```

Extract the environment ID from the results.

### Step 4: Get Latest Deployment

Retrieve the most recent successful deployment:

```javascript
octopusdeploy-list_deployments({
  spaceName: "<space-name>",
  projects: ["<project-id>"],
  environments: ["<environment-id>"],
  taskState: "Success",
  take: 1
})
```

Extract the release ID from the deployment.

### Step 5: Get Release Details

Fetch complete release information including build metadata:

```javascript
octopusdeploy-get_release_by_id({
  spaceName: "<space-name>",
  releaseId: "<release-id>"
})
```

The release object should contain build information with Git commit SHAs.

### Step 6: Fetch Git Commit Details

For each commit SHA in the release build information:

```javascript
github-mcp-server-get_commit({
  owner: "<repo-owner>",
  repo: "<repo-name>",
  sha: "<commit-sha>",
  include_diff: true
})
```

This retrieves:
- Commit message
- Author name and email
- Commit date
- Files changed
- Diff statistics

### Step 7: Generate Release Notes

Format the collected information into markdown:

```markdown
# Release Notes - Octopus Copilot Function

**Environment:** Production
**Release Date:** <date>
**Release Version:** <version>

## Changes

### Commits

- **<commit-message>** - *<author>* (<date>)
  - Files changed: <count>
  - +<additions> -<deletions>

[Repeat for each commit]

## Details

[Include additional context, categorization, etc.]
```

## Current Status

⚠️ **Blocked**: Cannot proceed with actual release notes generation due to:
- Octopus Deploy server URL not configured (getting "Invalid URL" error)
- Problem statement incomplete - space name cut off at "in the sp..."

## Next Steps

To complete this task:

1. **Configure Octopus Deploy Access**
   - Set server URL environment variable
   - Provide API key/credentials
   - Test connection with `octopusdeploy-list_spaces()`

2. **Provide Complete Information**
   - Full space name (currently incomplete)
   - Verify project name: "Octopus Copilot Function"
   - Verify environment name: "Production"

3. **Execute Workflow**
   - Run the step-by-step process outlined above
   - Generate markdown release notes
   - Save to `RELEASE_NOTES.md`

## Example Output

See `RELEASE_NOTES.md` for an example template of the expected output format.

## Tools Used

- **Octopus Deploy MCP Server Tools:**
  - `octopusdeploy-list_spaces`
  - `octopusdeploy-list_projects`
  - `octopusdeploy-list_environments`
  - `octopusdeploy-list_deployments`
  - `octopusdeploy-get_release_by_id`

- **GitHub MCP Server Tools:**
  - `github-mcp-server-get_commit`

## Troubleshooting

### "Invalid URL" Error

This indicates the Octopus Deploy server URL is not configured. Check:
- Environment variables for Octopus server URL
- MCP server configuration
- API credentials

### Missing Space Name

The problem statement appears to be cut off. Request clarification on the complete space name.
