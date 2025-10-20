# Release Notes - Task Status

## ❌ Unable to Complete Task

### Task Requirements
Generate release notes for the latest release of:
- **Project**: Octopus Copilot Function
- **Environment**: Production
- **Space**: Octopus Copilot
- **Repository**: mcasperson/GitHubCustomAgents

### ❗ Missing Required Information

To generate release notes from Octopus Deploy, the following information is required but was not provided:

1. **Octopus Deploy Server URL** - The base URL of your Octopus server (e.g., `https://your-instance.octopus.app`)
2. **Octopus API Key** - Authentication credentials to access the Octopus API
3. **Space ID** - The identifier for the "Octopus Copilot" space
4. **Project ID** - The identifier for the "Octopus Copilot Function" project
5. **Environment ID** - The identifier for the "Production" environment

### 🔧 How to Obtain Required Information

#### Get Space, Project, and Environment IDs:
```bash
# List all spaces
curl -H "X-Octopus-ApiKey: YOUR_API_KEY" \
     https://your-instance.octopus.app/api/spaces

# List projects in a space
curl -H "X-Octopus-ApiKey: YOUR_API_KEY" \
     https://your-instance.octopus.app/api/Spaces-{spaceId}/projects

# List environments in a space
curl -H "X-Octopus-ApiKey: YOUR_API_KEY" \
     https://your-instance.octopus.app/api/Spaces-{spaceId}/environments
```

### 📋 What This Tool Would Do (With Proper Access)

1. **Query Octopus Deploy** for the latest release:
   - Find the most recent deployment to Production environment
   - Retrieve the release details including build information
   - Extract Git commit SHAs from the build information

2. **Fetch Git Commit Details** from GitHub:
   - For each commit SHA in the release
   - Retrieve commit message, author, date, and diff
   - Using the GitHub API

3. **Generate Release Notes**:
   - Create a comprehensive markdown document
   - Summarize changes by commit
   - Filter out irrelevant commits (merge commits, version bumps, etc.)
   - Group related changes
   - Highlight important changes

### 💡 Alternative Approaches

#### Option A: Provide Commit Information Manually
If you can provide a list of Git commit SHAs from the Octopus release, I can generate release notes from GitHub directly:

```bash
# Example: Provide commits like this
COMMITS="abc123,def456,ghi789"
```

#### Option B: Use GitHub Releases
Consider using GitHub's release feature instead of or in addition to Octopus Deploy tracking.

---

**Status**: FAILED - Missing Octopus Deploy API credentials and configuration  
**Created**: 2025-10-20 23:48:23 UTC
