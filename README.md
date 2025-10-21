# GitHub Custom Agents

This repository contains custom agent configurations and tools for GitHub Copilot.

## Octopus Deploy Release Notes Generator

### Overview
This repository includes a tool to automatically generate release notes from Octopus Deploy deployments, enriched with detailed commit information from GitHub.

### Files
- `generate_octopus_release_notes.py` - Python script to fetch deployment information and generate release notes
- `release-notes.md` - Generated release notes (or documentation if generation fails)
- `.github/agents/octopus-deploy-release-notes-mcp.md` - MCP server configuration for Octopus Deploy

### Requirements
To use the release notes generator, you need:
- Python 3.6+
- `requests` library (`pip install requests`)
- Access to an Octopus Deploy instance
- GitHub access (uses GitHub API to fetch commit details)

### Configuration
Set the following environment variables:

```bash
export OCTOPUS_SERVER_URL="https://your-octopus-server.com"
export OCTOPUS_API_KEY="API-XXXXXXXXXXXXXXXXXXXXXXXX"
export GITHUB_TOKEN="your-github-token"  # Optional, for higher rate limits
export GITHUB_REPOSITORY="owner/repo"     # Optional, defaults to mcasperson/GitHubCustomAgents
```

### Usage

```bash
# Install dependencies
pip install requests

# Run the script
python3 generate_octopus_release_notes.py
```

The script will:
1. Connect to Octopus Deploy and retrieve the latest deployment to Production
2. Extract commit information from the deployment's build information
3. Fetch detailed commit data from GitHub (message, author, date, files changed)
4. Generate comprehensive markdown-formatted release notes
5. Save the output to `release-notes.md`

### Customization
You can customize the following in the script:
- `SPACE_NAME` - Octopus Deploy space name (default: "Octopus Copilot")
- `PROJECT_NAME` - Octopus Deploy project name (default: "Octopus Copilot Function")
- `ENVIRONMENT_NAME` - Octopus Deploy environment (default: "Production")

### Output Format
The generated release notes include:
- Release version and date
- List of changes with:
  - Commit message
  - Author information
  - Commit date
  - Commit SHA
  - Number of files changed
- Automatic filtering of merge commits and WIP changes

## License
This project is open source and available under standard terms.
