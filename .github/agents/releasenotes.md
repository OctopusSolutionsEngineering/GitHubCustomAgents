---
name: octopus-release-notes-with-mcp
description: Generate release notes for a release in Octopus Deploy
mcp-servers:
  octopus:
    type: local
    command: npx
    args: ["-y", "@octopusdeploy/mcp-server", "--api-key", ${{ secrets.OCTOPUS_API_KEY }}, "--server-url", ${{ secrets.OCTOPUS_SERVER_URL }}],
    transport: stdio
---