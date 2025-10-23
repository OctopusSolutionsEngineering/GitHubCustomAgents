#!/usr/bin/env python3
"""
Example/Demo of the release notes generator with mock data.

This demonstrates what the output would look like without requiring actual Octopus credentials.
"""

def generate_example_release_notes():
    """Generate example release notes to demonstrate the format."""
    
    release_notes = """# Release Notes: 1.2.3

**Project:** Octopus Copilot Function
**Environment:** Production
**Release Date:** 2025-10-23T10:30:00.000Z

## Changes

- **Implement new deployment strategy for multi-region rollouts**
  - Author: Alice Johnson
  - Date: 2025-10-22T14:20:00Z
  - Commit: [a1b2c3d](https://github.com/mcasperson/OctopusCopilot/commit/a1b2c3d)

- **Fix authentication token refresh logic**
  - Author: Bob Smith
  - Date: 2025-10-21T09:15:00Z
  - Commit: [e4f5g6h](https://github.com/mcasperson/OctopusCopilot/commit/e4f5g6h)

- **Add comprehensive error handling for API calls**
  - Author: Carol Williams
  - Date: 2025-10-20T16:45:00Z
  - Commit: [i7j8k9l](https://github.com/mcasperson/OctopusCopilot/commit/i7j8k9l)

- **Update dependencies to latest stable versions**
  - Author: David Brown
  - Date: 2025-10-19T11:30:00Z
  - Commit: [m1n2o3p](https://github.com/mcasperson/OctopusCopilot/commit/m1n2o3p)

- **Improve logging for deployment tracking**
  - Author: Alice Johnson
  - Date: 2025-10-18T13:00:00Z
  - Commit: [q4r5s6t](https://github.com/mcasperson/OctopusCopilot/commit/q4r5s6t)
"""
    
    return release_notes


if __name__ == '__main__':
    print("Example Release Notes Output")
    print("=" * 60)
    print()
    print(generate_example_release_notes())
    print()
    print("=" * 60)
    print("\nTo generate actual release notes, use:")
    print("  python generate_release_notes.py \\")
    print("    --space 'Octopus Copilot' \\")
    print("    --project 'Octopus Copilot Function' \\")
    print("    --environment 'Production'")
    print("\nMake sure to set OCTOPUS_URL and OCTOPUS_API_KEY environment variables.")
