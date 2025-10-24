# Octopus Release Notes Custom Agent

This GitHub custom agent generates release notes from a deployment in Octopus Deploy. It combines the high-level release notes
from Octopus Deploy with the details of the Git commits from GitHub to produce a comprehensive set of release notes in markdown format.

This is the MCP definition:

```json
{ 
  "mcpServers": {
    "octopusdeploy": {
        "type": "local",
        "command": "npx",
        "args": [
            "-y", 
            "@octopusdeploy/mcp-server"
        ],
        "env": {
            "OCTOPUS_SERVER_URL": "COPILOT_MCP_OCTOPUS_SERVER_URL",
            "OCTOPUS_API_KEY": "COPILOT_MCP_OCTOPUS_API_KEY"
        },
        "tools": [
            "get_account",
            "get_branches",
            "get_certificate",
            "get_current_user",
            "get_deployment_process",
            "get_deployment_target",
            "get_kubernetes_live_status",
            "get_missing_tenant_variables",
            "get_release_by_id",
            "get_task_by_id",
            "get_task_details",
            "get_task_raw",
            "get_tenant_by_id",
            "get_tenant_variables",
            "get_variables",
            "list_accounts",
            "list_certificates",
            "list_deployments",
            "list_deployment_targets",
            "list_environments",
            "list_projects",
            "list_releases",
            "list_releases_for_project",
            "list_spaces",
            "list_tenants"
        ]
    }
  } 
}
```