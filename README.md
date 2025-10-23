# GitHub Custom Agents

This repository contains custom agents and tools for working with GitHub and Octopus Deploy.

## Octopus Deploy Release Notes Generator

A tool to automatically generate release notes from Octopus Deploy releases by extracting commit information and enriching it with GitHub commit details.

### Features

- Connects to Octopus Deploy API to retrieve the latest release for a specified project, environment, and space
- Extracts commit information from the release's build information
- Fetches detailed commit information from GitHub (including author, date, and diff)
- Generates formatted markdown release notes

### Prerequisites

- Python 3.6+
- Octopus Deploy server URL and API key
- (Optional) GitHub personal access token for enhanced commit details

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Environment Variables

Set the following environment variables:
- `OCTOPUS_URL`: Your Octopus Deploy server URL
- `OCTOPUS_API_KEY`: Your Octopus Deploy API key
- `GITHUB_TOKEN`: (Optional) Your GitHub personal access token

#### Command Line

```bash
python generate_release_notes.py \
  --space "Octopus Copilot" \
  --project "Octopus Copilot Function" \
  --environment "Production"
```

Or with explicit configuration:

```bash
python generate_release_notes.py \
  --space "Octopus Copilot" \
  --project "Octopus Copilot Function" \
  --environment "Production" \
  --octopus-url "https://your-octopus-server.com" \
  --octopus-api-key "API-XXXXXXXXXX" \
  --github-token "ghp_XXXXXXXXXX" \
  --output release_notes.md
```

#### Arguments

- `--space`: Name of the Octopus space (required)
- `--project`: Name of the Octopus project (required)
- `--environment`: Name of the Octopus environment (required)
- `--octopus-url`: Octopus server URL (optional if set via environment variable)
- `--octopus-api-key`: Octopus API key (optional if set via environment variable)
- `--github-token`: GitHub token (optional, enhances commit details)
- `--output`: Output file path (optional, defaults to stdout)

### Example Output

```markdown
# Release Notes: 1.0.5

**Project:** Octopus Copilot Function
**Environment:** Production
**Release Date:** 2025-10-23T10:30:00.000Z

## Changes

- **Add support for multiple deployment targets**
  - Author: John Doe
  - Date: 2025-10-22T14:20:00Z
  - Commit: [a1b2c3d](https://github.com/org/repo/commit/a1b2c3d)

- **Fix authentication issue**
  - Author: Jane Smith
  - Date: 2025-10-21T09:15:00Z
  - Commit: [e4f5g6h](https://github.com/org/repo/commit/e4f5g6h)
```

### License

MIT
