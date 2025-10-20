# GitHub Custom Agents

This repository contains custom agents and tools for GitHub Copilot and Octopus Deploy integration.

## Release Notes Generator

This project includes a comprehensive release notes generator that integrates with Octopus Deploy and GitHub to create detailed, professional release notes.

### Features

- **Octopus Deploy Integration**: Fetches release information from Octopus Deploy
- **GitHub Commit Analysis**: Retrieves detailed commit information including messages, authors, dates, and diffs
- **Smart Categorization**: Automatically categorizes commits into Features, Bug Fixes, Improvements, and Other
- **Filtering**: Skips irrelevant commits like merge commits and trivial changes
- **Markdown Output**: Generates well-formatted markdown documentation
- **Contributors List**: Automatically identifies and lists all contributors

### Quick Start

1. **Set up environment variables** (for production use with Octopus):
   ```bash
   export OCTOPUS_SERVER="https://your-server.octopus.app"
   export OCTOPUS_API_KEY="API-XXXXXXXXXX"
   ```

2. **Run the generator**:
   ```bash
   python3 generate_release_notes.py > RELEASE_NOTES.md
   ```

3. **Demo mode** (without Octopus credentials):
   ```bash
   python3 generate_release_notes.py
   ```

### Documentation

- [Release Notes Guide](RELEASE_NOTES_GUIDE.md) - Detailed documentation on usage and customization
- [Example Release Notes](RELEASE_NOTES.md) - Sample output generated from this repository

### Requirements

- Python 3.6+
- Git
- Access to Octopus Deploy (for production use)
- Access to GitHub repository

### Configuration

The generator can be configured through environment variables:

- `OCTOPUS_SERVER` - Your Octopus Deploy server URL
- `OCTOPUS_API_KEY` - Your Octopus Deploy API key
- Additional configuration available in the script

### Custom Agents

This repository also contains custom agent definitions in `.github/agents/`:

- `releasenotes.md` - Agent for generating release notes using Octopus Deploy MCP server

### License

See repository license for details.
