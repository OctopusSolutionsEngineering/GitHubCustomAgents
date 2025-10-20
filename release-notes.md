# Release Notes

## Project: Octopus Copilot Function
**Environment:** Production  
**Space:** Octopus Copilot  
**Generated:** 2025-10-20

---

## ⚠️ Unable to Generate Complete Release Notes

### Issue
The release notes could not be automatically generated because access to Octopus Deploy is not available in the current environment.

### What Was Attempted
1. ✓ Located the custom agent configuration for Octopus Deploy integration
2. ✓ Verified the agent expects `OCTOPUS_API_KEY` and `OCTOPUS_SERVER_URL` secrets
3. ✗ Environment variables for Octopus Deploy credentials are not set
4. ✗ Octopus Deploy MCP server is not accessible without credentials

### Required Setup
To generate release notes automatically, one of the following must be configured:

1. **GitHub Secrets (Recommended)**
   - Add `OCTOPUS_API_KEY` secret with your Octopus Deploy API key
   - Add `OCTOPUS_SERVER_URL` secret with your Octopus Deploy server URL
   - These will be automatically injected into the custom agent

2. **Manual Approach**
   - Provide the list of Git commits from the Octopus release
   - The agent can then fetch commit details from GitHub and generate notes

### Next Steps
Please configure the required Octopus Deploy credentials as GitHub secrets and re-run this task.

---

## Template: Expected Release Notes Format

When properly configured, this file would contain:

### Features
- Feature descriptions from commit messages
- Author attribution
- Commit dates

### Bug Fixes
- Bug fix descriptions
- Related issue numbers
- Author attribution

### Infrastructure Changes
- Deployment configuration updates
- Build process improvements

### Other Changes
- Documentation updates
- Refactoring
- Minor improvements

---

*This document was created by the GitHub Copilot Agent*  
*For more information about configuring Octopus Deploy integration, see `.github/agents/releasenotes.md`*
