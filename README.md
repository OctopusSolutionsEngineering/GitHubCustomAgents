# Release Notes Generator

This tool generates release notes for Octopus Deploy releases by fetching commit information from GitHub.

## Prerequisites

- Python 3.6 or higher
- Access to Octopus Deploy API
- Access to GitHub repository
- Octopus Deploy API key
- (Optional) GitHub personal access token for private repositories

## Setup

### 1. Set Environment Variables

Create a `.env` file or export the following environment variables:

```bash
# Required
export OCTOPUS_SERVER_URL="https://your-instance.octopus.app"
export OCTOPUS_API_KEY="API-XXXXXXXXXXXXXXXXXXXXXXXXXX"

# Optional (for private repositories)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Optional (can be passed as argument instead)
export GITHUB_REPOSITORY="owner/repo"
```

### 2. Create Octopus API Key

1. Log in to your Octopus Deploy instance
2. Go to your profile (top right) → Profile → My API Keys
3. Click "New API Key"
4. Give it a purpose (e.g., "Release Notes Generator")
5. Copy the generated API key
6. Set it as the `OCTOPUS_API_KEY` environment variable

### 3. (Optional) Create GitHub Token

For public repositories, a token is not required. For private repositories or to avoid rate limiting:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Set it as the `GITHUB_TOKEN` environment variable

## Usage

### Basic Usage

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo"
```

### With Custom Output File

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo" \
    --output "releases/v1.0.0-notes.md"
```

### Using Environment Variables

If `GITHUB_REPOSITORY` is set in your environment (e.g., in GitHub Actions):

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot"
```

## How It Works

1. **Connects to Octopus Deploy**: Uses the API to authenticate
2. **Finds the Space**: Locates the specified space by name
3. **Finds the Project**: Locates the project within the space
4. **Finds the Environment**: Locates the target environment
5. **Gets Latest Deployment**: Retrieves the most recent deployment to that environment
6. **Gets Release Details**: Fetches the release information
7. **Gets Build Information**: Retrieves Git commit information from Octopus build information
8. **Fetches Commit Details**: For each commit, fetches full details from GitHub
9. **Generates Release Notes**: Creates a markdown-formatted document with all changes

## Example Output

```markdown
# Release Notes

Generated: 2025-10-20 12:00:00 UTC
Total commits: 5

## Changes

### Add new authentication feature
- **Author**: John Doe
- **Date**: 2025-10-19T14:30:00Z
- **Commit**: abc1234

Implemented OAuth2 authentication for improved security.

### Fix bug in user profile
- **Author**: Jane Smith
- **Date**: 2025-10-19T10:15:00Z
- **Commit**: def5678

Fixed issue where user profiles were not loading correctly.

### Update dependencies
- **Author**: John Doe
- **Date**: 2025-10-18T16:45:00Z
- **Commit**: ghi9012
```

## Troubleshooting

### "Space not found"
- Verify the space name is correct (case-sensitive)
- Ensure your API key has access to the space

### "Project not found"
- Verify the project name is correct (case-sensitive)
- Ensure the project exists in the specified space

### "Environment not found"
- Verify the environment name is correct (case-sensitive)
- Ensure the environment exists in the specified space

### "No deployments found"
- Verify that at least one deployment has been made to the environment
- Check that the project has been deployed to the specified environment

### "No build information found"
- This means no Git commits are associated with the release
- Ensure your CI/CD pipeline is pushing build information to Octopus
- See: https://octopus.com/docs/packaging-applications/build-servers/build-information

## Integration with CI/CD

### GitHub Actions

```yaml
name: Generate Release Notes

on:
  workflow_dispatch:
    inputs:
      project:
        description: 'Octopus Project Name'
        required: true
      environment:
        description: 'Octopus Environment Name'
        required: true
      space:
        description: 'Octopus Space Name'
        required: true

jobs:
  release-notes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate Release Notes
        env:
          OCTOPUS_SERVER_URL: ${{ secrets.OCTOPUS_SERVER_URL }}
          OCTOPUS_API_KEY: ${{ secrets.OCTOPUS_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 generate_release_notes.py \
            --project "${{ github.event.inputs.project }}" \
            --environment "${{ github.event.inputs.environment }}" \
            --space "${{ github.event.inputs.space }}" \
            --github-repo "${{ github.repository }}"
      
      - name: Upload Release Notes
        uses: actions/upload-artifact@v3
        with:
          name: release-notes
          path: RELEASE_NOTES.md
```

## License

This tool is provided as-is for generating release notes from Octopus Deploy deployments.
