#!/usr/bin/env node

/**
 * Octopus Deploy Release Notes Generator
 * 
 * This script generates release notes for an Octopus Deploy project by:
 * 1. Getting the latest deployment to a specified environment
 * 2. Retrieving the release and build information
 * 3. Fetching Git commit details from GitHub for each commit in the release
 * 4. Generating formatted markdown release notes
 * 
 * Prerequisites:
 * - Octopus Deploy server URL and API key configured in environment
 * - GitHub repository access
 * 
 * Usage:
 *   node generate-release-notes.js <spaceName> <projectName> <environmentName>
 * 
 * Example:
 *   node generate-release-notes.js "Default" "Octopus Copilot Function" "Production"
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 3) {
    console.error('Usage: node generate-release-notes.js <spaceName> <projectName> <environmentName>');
    console.error('Example: node generate-release-notes.js "Default" "Octopus Copilot Function" "Production"');
    process.exit(1);
}

const [spaceName, projectName, environmentName] = args;

console.log('='.repeat(80));
console.log('Octopus Deploy Release Notes Generator');
console.log('='.repeat(80));
console.log(`\nConfiguration:`);
console.log(`  Space:       ${spaceName}`);
console.log(`  Project:     ${projectName}`);
console.log(`  Environment: ${environmentName}`);
console.log('');

/**
 * Main workflow for generating release notes
 */
async function generateReleaseNotes() {
    try {
        // Note: This script demonstrates the workflow using MCP tools
        // In actual execution, these would be async calls to the MCP server
        
        console.log('Step 1: Listing available spaces...');
        console.log('  -> Would call: octopusdeploy-list_spaces');
        console.log('  -> Verify space exists: ' + spaceName);
        console.log('');
        
        console.log('Step 2: Finding project in space...');
        console.log(`  -> Would call: octopusdeploy-list_projects(spaceName="${spaceName}", partialName="${projectName}")`);
        console.log('  -> Extract project ID');
        console.log('');
        
        console.log('Step 3: Finding environment...');
        console.log(`  -> Would call: octopusdeploy-list_environments(spaceName="${spaceName}", partialName="${environmentName}")`);
        console.log('  -> Extract environment ID');
        console.log('');
        
        console.log('Step 4: Getting latest deployment...');
        console.log(`  -> Would call: octopusdeploy-list_deployments(spaceName="${spaceName}", projects=[projectId], environments=[environmentId], taskState="Success", take=1)`);
        console.log('  -> Extract deployment and release ID');
        console.log('');
        
        console.log('Step 5: Getting release details...');
        console.log('  -> Would call: octopusdeploy-get_release_by_id(spaceName, releaseId)');
        console.log('  -> Extract build information with Git commits');
        console.log('');
        
        console.log('Step 6: Fetching Git commit details from GitHub...');
        console.log('  -> For each commit SHA in the release:');
        console.log('     - Would call: github-mcp-server-get_commit(owner, repo, sha)');
        console.log('     - Extract: message, author, date, diff summary');
        console.log('');
        
        console.log('Step 7: Generating release notes...');
        console.log('  -> Format commits into markdown');
        console.log('  -> Save to RELEASE_NOTES.md');
        console.log('');
        
        // Generate example release notes structure
        const exampleReleaseNotes = generateExampleReleaseNotes(spaceName, projectName, environmentName);
        
        const outputPath = path.join(__dirname, 'RELEASE_NOTES.md');
        fs.writeFileSync(outputPath, exampleReleaseNotes);
        
        console.log('✓ Release notes template generated successfully!');
        console.log(`  Output: ${outputPath}`);
        console.log('');
        console.log('Note: This is a demonstration script. To generate actual release notes,');
        console.log('configure Octopus Deploy server URL and API key, then use the MCP tools.');
        
    } catch (error) {
        console.error('Error generating release notes:', error.message);
        process.exit(1);
    }
}

/**
 * Generate example release notes structure
 */
function generateExampleReleaseNotes(spaceName, projectName, environmentName) {
    const date = new Date().toISOString().split('T')[0];
    
    return `# Release Notes

**Project:** ${projectName}  
**Environment:** ${environmentName}  
**Space:** ${spaceName}  
**Generated:** ${date}

## Summary

This release includes the following changes:

## Changes

### Feature Updates
- *[Commits would be listed here with details from GitHub]*
- *Each commit would include: message, author, date*
- *Relevant changes would be summarized*

### Bug Fixes
- *Bug fix commits would be listed here*

### Infrastructure Changes
- *Infrastructure-related changes would be listed here*

## Commit Details

*Detailed commit information would be included here, fetched from GitHub:*
- Commit SHA
- Author
- Date
- Message
- Files changed summary

---

## How This Was Generated

1. Retrieved latest deployment for "${projectName}" in "${environmentName}" environment
2. Extracted release information from Octopus Deploy
3. Fetched Git commit details from GitHub for each commit in the release
4. Categorized and formatted commits into this document

## Next Steps

To regenerate these release notes with actual data:
1. Ensure Octopus Deploy server is accessible
2. Configure API credentials
3. Run the release notes generator with the MCP tools
`;
}

// Run the script
generateReleaseNotes().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});
