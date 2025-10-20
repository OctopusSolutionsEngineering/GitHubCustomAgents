# Release Notes - Octopus Copilot Function

**Project**: Octopus Copilot Function  
**Environment**: Production  
**Space**: Octopus Copilot  
**Generated**: 2025-10-20 23:11:00 UTC

---

## Overview

This document contains the release notes for the latest deployment of the **Octopus Copilot Function** project to the **Production** environment in the **Octopus Copilot** space.

## How to Generate

To generate up-to-date release notes with actual commit information, run:

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo"
```

Make sure to:
1. Set the `OCTOPUS_SERVER_URL` environment variable
2. Set the `OCTOPUS_API_KEY` environment variable
3. Replace `owner/repo` with the actual GitHub repository

## Prerequisites

Before generating release notes, ensure that:

- [ ] You have access to the Octopus Deploy instance
- [ ] You have an Octopus Deploy API key with read permissions
- [ ] The Octopus Deploy space "Octopus Copilot" exists
- [ ] The project "Octopus Copilot Function" exists in the space
- [ ] The environment "Production" exists
- [ ] At least one deployment has been made to Production
- [ ] Build information with Git commits is attached to the release in Octopus

## Notes

This is a template file. To generate actual release notes:

1. Configure your Octopus Deploy credentials (see `.env.template`)
2. Run the `generate_release_notes.py` script
3. The script will fetch the latest deployment and associated commits
4. Release notes will be generated in markdown format

## Need Help?

See the [README.md](README.md) file for detailed instructions on:
- Setting up environment variables
- Creating Octopus Deploy API keys
- Configuring GitHub access tokens
- Running the release notes generator
- Troubleshooting common issues

---

*This file was created as a template. Run the release notes generator to populate it with actual commit information.*
