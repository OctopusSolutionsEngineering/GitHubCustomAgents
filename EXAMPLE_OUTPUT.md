# Example: Release Notes Generation for Octopus Copilot Function

This document demonstrates how the release notes generator works.

## Command

```bash
python3 generate_release_notes.py "Octopus Copilot" "Octopus Copilot Function" "Production"
```

## Execution Flow

### 1. Query Octopus Deploy

The script queries Octopus Deploy using these MCP server tools:

```
📦 Fetching latest deployment for:
   Space: Octopus Copilot
   Project: Octopus Copilot Function
   Environment: Production
```

**MCP Calls Made:**
- `octopusdeploy-list_spaces(partialName="Octopus Copilot")` → Get space ID
- `octopusdeploy-list_projects(spaceName="Octopus Copilot", partialName="Octopus Copilot Function")` → Get project ID
- `octopusdeploy-list_environments(spaceName="Octopus Copilot", partialName="Production")` → Get environment ID
- `octopusdeploy-list_deployments(spaceName="Octopus Copilot", projects=[project_id], environments=[env_id], taskState="Success")` → Get latest deployment
- `octopusdeploy-get_release_by_id(spaceName="Octopus Copilot", releaseId=release_id)` → Get release with build information

### 2. Extract Commit Information

From the release's build information metadata, the script extracts:
- Commit SHAs
- Repository information (owner/repo)

### 3. Query GitHub

For each commit, the script queries GitHub using:

```
🔍 Fetching commit details for abc123def456 in owner/repo
```

**MCP Calls Made:**
- `github-mcp-server-get_commit(owner="owner", repo="repo", sha="abc123def456", include_diff=True)`

This retrieves:
- Commit message
- Author name and email
- Commit date
- File change statistics (additions, deletions)
- Unified diff of changes

### 4. Generate Release Notes

The script filters commits (skipping merges, formatting changes) and generates markdown:

```markdown
# Release Notes - Octopus Copilot Function

**Version:** 1.0.0
**Environment:** Production
**Space:** Octopus Copilot
**Deployed:** 2025-10-23T23:19:58.198008

---

## Changes

### Sample commit message

- **Author:** John Doe
- **Date:** 2025-10-23T23:19:58.198019
- **Commit:** `abc123d`

**Changes:** +10 / -5 lines

---

*Total: 1 commit(s) included, 0 commit(s) skipped*
```

### 5. Save to File

The release notes are saved to `release_notes_1.0.0.md`

## Real-World Example

With actual Octopus Deploy and GitHub data, the output would look like:

```markdown
# Release Notes - Octopus Copilot Function

**Version:** 2.1.5
**Environment:** Production
**Space:** Octopus Copilot
**Deployed:** 2025-10-23T14:30:00.000000

---

## Changes

### Add support for multi-region deployments

- **Author:** Jane Smith
- **Date:** 2025-10-22T10:15:00
- **Commit:** `a1b2c3d`

Implemented multi-region deployment capability with automatic failover.

**Changes:** +245 / -18 lines

### Fix memory leak in connection pool

- **Author:** John Doe
- **Date:** 2025-10-21T16:45:00
- **Commit:** `e4f5g6h`

Resolved issue where database connections were not properly released.

**Changes:** +12 / -8 lines

### Update dependencies to latest versions

- **Author:** Alice Johnson
- **Date:** 2025-10-20T09:00:00
- **Commit:** `i7j8k9l`

**Changes:** +156 / -142 lines

---

*Total: 3 commit(s) included, 2 commit(s) skipped*
```

## Notes

- The script requires valid Octopus Deploy API credentials to access deployment information
- GitHub credentials are needed to fetch commit details
- Commits are filtered to exclude merges and minor changes
- The output is saved to a file named after the release version
