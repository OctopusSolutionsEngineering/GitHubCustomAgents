# Generate Release Notes for Octopus Deploy

This document describes how to generate release notes for an Octopus Deploy release.

## Process

The release notes generation process follows these steps:

1. **Query Octopus Deploy Space**
   - Find the space by name (e.g., "Octopus Copilot")

2. **Get Project and Environment**
   - Retrieve the project details (e.g., "Octopus Copilot Function")
   - Get the environment details (e.g., "Production")

3. **Find Latest Deployment**
   - Query for the most recent successful deployment
   - Filter by project and environment

4. **Extract Release Information**
   - Get the release details using the release ID from the deployment
   - Extract build information and Git commit details

5. **Gather Commit Details**
   - For each commit in the release build information:
     - Commit SHA
     - Commit message
     - Author information (if available)
     - Commit URL

6. **Generate Release Notes**
   - Create a markdown document with:
     - Version and deployment information
     - Overview of changes
     - List of commits with links
     - Build information
     - Package versions

## Example Output

The generated release notes include:
- Release version and date
- Git commits included in the release
- Links to commits in GitHub
- Build and deployment metadata
- Package versions deployed

## Tools Used

- **Octopus Deploy MCP Tools**: For querying deployment information
- **GitHub MCP Tools**: For retrieving commit details (when accessible)
- **Markdown**: For formatting the release notes

## Generated File

The release notes are saved as `release_notes.md` in the repository root.
