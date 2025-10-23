# Octopus Deploy Release Notes Generator

This repository contains tools and documentation for generating release notes from Octopus Deploy deployments.

## Purpose

Generate comprehensive release notes by:
1. Retrieving deployment information from Octopus Deploy
2. Fetching commit details from GitHub
3. Formatting everything into readable markdown documentation

## Files

- **OCTOPUS_RELEASE_NOTES_GUIDE.md** - Complete guide on how to generate release notes
- **RELEASE_NOTES.md** - Template/example of the generated release notes
- **generate-release-notes.js** - Script demonstrating the workflow (Node.js)

## Current Status

⚠️ **Incomplete Task** - Unable to complete due to:

1. **Octopus Deploy Server Not Configured**
   - MCP tools return "Invalid URL" error
   - Server URL and API credentials needed

2. **Incomplete Problem Statement**
   - Requirement: "Generate the release notes for the latest release of project 'Octopus Copilot Function' in the environment 'Production' in the sp..."
   - Space name cut off at "in the sp..."
   - Need complete space name to proceed

## Next Steps

To complete this task:

1. Configure Octopus Deploy server access
   - Set server URL
   - Provide API key/credentials

2. Provide complete space name
   - Current: "in the sp..." (incomplete)
   - Example: "Default", "Production", etc.

3. Execute the workflow as documented in OCTOPUS_RELEASE_NOTES_GUIDE.md

## How It Works

When properly configured, the release notes generator will:

1. Connect to Octopus Deploy server
2. List spaces and find the specified space
3. Find the "Octopus Copilot Function" project
4. Find the "Production" environment
5. Get the latest successful deployment
6. Retrieve release details with build information
7. For each Git commit in the release:
   - Fetch commit details from GitHub
   - Extract message, author, date, files changed
   - Collect diff statistics
8. Generate formatted markdown release notes
9. Save to RELEASE_NOTES.md

## Documentation

See **OCTOPUS_RELEASE_NOTES_GUIDE.md** for detailed instructions.

## Requirements

- Octopus Deploy server access (URL + API key)
- GitHub repository access (for commit details)
- Node.js (for running the generator script)
- Complete project details:
  - Space name
  - Project name: "Octopus Copilot Function"
  - Environment name: "Production"
