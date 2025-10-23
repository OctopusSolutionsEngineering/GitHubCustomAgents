# Release Notes Generator - Usage Examples

## Quick Start

### 1. Using the Demo Script (No Octopus Access Required)

```bash
node generate-release-notes.js "Default" "Octopus Copilot Function" "Production"
```

This will generate a template and show the workflow steps.

### 2. With Octopus Deploy Access (When Configured)

First, ensure Octopus Deploy is configured:
- Server URL is set
- API key is available
- MCP tools can connect

Then run:

```bash
# Try with Default space
./generate-release-notes.js "Default" "Octopus Copilot Function" "Production"

# Or with a specific space name
./generate-release-notes.js "Production-Space" "Octopus Copilot Function" "Production"
```

## Manual Workflow Using MCP Tools

If you prefer to run the workflow manually or integrate it into another system, here's the step-by-step process:

### Step 1: List Spaces

```javascript
// Using octopusdeploy-list_spaces MCP tool
const spaces = await octopusdeploy_list_spaces({ take: 100 });
console.log('Available spaces:', spaces);

// Find your space by name
const targetSpace = spaces.find(s => s.Name === "Default");
```

### Step 2: List Projects

```javascript
// Using octopusdeploy-list_projects MCP tool
const projects = await octopusdeploy_list_projects({
  spaceName: "Default",
  partialName: "Octopus Copilot Function"
});

const project = projects[0];
console.log('Project ID:', project.Id);
```

### Step 3: List Environments

```javascript
// Using octopusdeploy-list_environments MCP tool
const environments = await octopusdeploy_list_environments({
  spaceName: "Default",
  partialName: "Production"
});

const environment = environments[0];
console.log('Environment ID:', environment.Id);
```

### Step 4: Get Latest Deployment

```javascript
// Using octopusdeploy-list_deployments MCP tool
const deployments = await octopusdeploy_list_deployments({
  spaceName: "Default",
  projects: [project.Id],
  environments: [environment.Id],
  taskState: "Success",
  take: 1
});

const latestDeployment = deployments[0];
console.log('Release ID:', latestDeployment.ReleaseId);
```

### Step 5: Get Release Details

```javascript
// Using octopusdeploy-get_release_by_id MCP tool
const release = await octopusdeploy_get_release_by_id({
  spaceName: "Default",
  releaseId: latestDeployment.ReleaseId
});

console.log('Build Information:', release.BuildInformation);
// BuildInformation contains an array of commits
```

### Step 6: Fetch GitHub Commit Details

```javascript
// For each commit in the release build information
for (const buildInfo of release.BuildInformation) {
  for (const commit of buildInfo.Commits) {
    // Using github-mcp-server-get_commit MCP tool
    const commitDetails = await github_get_commit({
      owner: buildInfo.VcsRoot.split('/')[0],  // Extract from VCS root
      repo: buildInfo.VcsRoot.split('/')[1],
      sha: commit.Id,
      include_diff: true
    });
    
    console.log('Commit:', {
      sha: commitDetails.sha,
      message: commitDetails.commit.message,
      author: commitDetails.commit.author.name,
      date: commitDetails.commit.author.date,
      filesChanged: commitDetails.files.length,
      additions: commitDetails.stats.additions,
      deletions: commitDetails.stats.deletions
    });
  }
}
```

### Step 7: Format Release Notes

```javascript
// Generate markdown
let markdown = `# Release Notes - ${project.Name}\n\n`;
markdown += `**Environment:** ${environment.Name}\n`;
markdown += `**Release:** ${release.Version}\n`;
markdown += `**Deployed:** ${latestDeployment.Created}\n\n`;
markdown += `## Changes\n\n`;

// Add each commit
for (const commit of commits) {
  markdown += `### ${commit.message.split('\n')[0]}\n\n`;
  markdown += `- **Author:** ${commit.author}\n`;
  markdown += `- **Date:** ${commit.date}\n`;
  markdown += `- **Files:** ${commit.filesChanged} changed (+${commit.additions} -${commit.deletions})\n`;
  markdown += `\n${commit.message}\n\n`;
}

// Save to file
fs.writeFileSync('RELEASE_NOTES.md', markdown);
```

## Current Limitations

⚠️ **Octopus Deploy Server Not Configured**
- All MCP tool calls return "Invalid URL" error
- Server URL and API credentials needed

⚠️ **Incomplete Problem Statement**
- Space name appears to be cut off: "in the sp..."
- Cannot determine which space to use

## Troubleshooting

### Error: "Invalid URL"

This means the Octopus Deploy server is not configured. Check:

1. Environment variables:
   - `OCTOPUS_SERVER_URL`
   - `OCTOPUS_API_KEY`

2. MCP server configuration file

3. Network connectivity to Octopus server

### Missing Space Name

If you see "in the sp..." in the problem statement:

1. Ask for the complete space name
2. Try common names: "Default", "Production", etc.
3. List all spaces and select the appropriate one

### No Build Information

If the release doesn't have build information:

1. Ensure Octopus is configured to capture build information
2. Check that the release was created with Git commits
3. Verify VCS integration is set up correctly

## Integration Examples

### CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
- name: Generate Release Notes
  run: |
    node generate-release-notes.js "${{ env.SPACE_NAME }}" "Octopus Copilot Function" "Production"
    cat RELEASE_NOTES.md
```

### Automated Notifications

```bash
# Generate and send via email/Slack
node generate-release-notes.js "Default" "Octopus Copilot Function" "Production"
# Send RELEASE_NOTES.md to stakeholders
```

## Further Reading

- See `OCTOPUS_RELEASE_NOTES_GUIDE.md` for detailed workflow explanation
- See `RELEASE_NOTES.md` for example output format
- See `README.md` for project overview
