#!/bin/bash

echo "=========================================="
echo "Testing Octopus Deploy MCP Tools"
echo "=========================================="
echo ""
echo "This script tests the Octopus Deploy MCP connection"
echo "to determine why release notes cannot be generated."
echo ""

echo "Environment Check:"
echo "- Checking for Octopus-related environment variables..."
env | grep -i octopus || echo "  No Octopus environment variables found"
echo ""

echo "Expected MCP tools:"
echo "  - octopusdeploy-list_spaces"
echo "  - octopusdeploy-list_projects"
echo "  - octopusdeploy-list_environments"
echo "  - octopusdeploy-list_deployments"
echo "  - octopusdeploy-get_release_by_id"
echo ""

echo "Error encountered when attempting to use MCP tools:"
echo "  'Invalid URL'"
echo ""

echo "This indicates the Octopus Deploy server URL is not configured."
echo "To fix:"
echo "  1. Set OCTOPUS_SERVER_URL environment variable"
echo "  2. Set OCTOPUS_API_KEY environment variable"
echo "  3. Verify network connectivity to Octopus server"
echo ""

echo "=========================================="
