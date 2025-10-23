# Octopus Deploy Release Notes Generator

This repository contains scripts to generate release notes for Octopus Deploy releases.

## Overview

The scripts in this repository can fetch release information from Octopus Deploy and generate formatted release notes in markdown format based on Git commit information included in the releases.

## Files

- **`generate_release_notes.py`**: Core script that takes release data (as JSON) and generates markdown-formatted release notes
- **`fetch_and_generate_release_notes.py`**: Standalone script that includes sample data and can be run independently
- **`RELEASE_NOTES.md`**: Example output showing release notes for the latest release

## Usage

### Using the Core Script

To generate release notes from release data:

```bash
python3 generate_release_notes.py <path-to-release-data.json>
```

Or pipe data via stdin:

```bash
cat release_data.json | python3 generate_release_notes.py
```

### Using the Standalone Script

Run the comprehensive script that includes sample data:

```bash
python3 fetch_and_generate_release_notes.py
```

## Example Output

The scripts generate release notes in the following format:

```markdown
# Release Notes - Version 0.1.2942+7bc3c67.3022.1

**Released:** 2025-10-19 20:38:50 UTC

## Package: OctopusCopilot v0.1.2942
**Build Number:** 3022
**Branch:** main
**Build URL:** [...]
**Repository:** https://github.com/OctopusSolutionsEngineering/OctopusCopilot

### Changes (1 commit)
- [7bc3c67](...) - Updated context

## Additional Notes from Octopus Deploy
...
```

## Release Information

The latest release notes have been generated for:
- **Space**: Octopus Copilot
- **Project**: Octopus Copilot Function
- **Environment**: Production
- **Version**: 0.1.2942+7bc3c67.3022.1
- **Released**: 2025-10-19 20:38:50 UTC

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the complete release notes.
