#!/bin/bash
#
# Release Notes Generator Wrapper Script
# 
# This script provides a convenient way to generate release notes
# for Octopus Deploy deployments.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored messages
print_info() {
    echo -e "${GREEN}ℹ${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Default values
PROJECT="Octopus Copilot Function"
ENVIRONMENT="Production"
SPACE="Octopus Copilot"
GITHUB_REPO="${GITHUB_REPOSITORY:-}"
OUTPUT="RELEASE_NOTES.md"

# Parse command line arguments (check for --help first)
for arg in "$@"; do
    if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Generate release notes for Octopus Deploy deployments"
        echo ""
        echo "Options:"
        echo "  --project PROJECT          Octopus project name (default: 'Octopus Copilot Function')"
        echo "  --environment ENV          Octopus environment name (default: 'Production')"
        echo "  --space SPACE              Octopus space name (default: 'Octopus Copilot')"
        echo "  --github-repo OWNER/REPO   GitHub repository"
        echo "  --output FILE              Output file (default: RELEASE_NOTES.md)"
        echo "  -h, --help                 Show this help message"
        echo ""
        echo "Environment variables:"
        echo "  OCTOPUS_SERVER_URL         Octopus Deploy server URL (required)"
        echo "  OCTOPUS_API_KEY            Octopus Deploy API key (required)"
        echo "  GITHUB_TOKEN               GitHub personal access token (optional)"
        echo "  GITHUB_REPOSITORY          GitHub repository owner/repo (optional)"
        echo ""
        exit 0
    fi
done

# Check Python installation
if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_info "Using Python $PYTHON_VERSION"

# Load environment variables from .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    print_info "Loading environment variables from .env"
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
else
    print_warning "No .env file found. Looking for environment variables..."
fi

# Check required environment variables
if [ -z "$OCTOPUS_SERVER_URL" ]; then
    print_error "OCTOPUS_SERVER_URL environment variable is not set"
    echo ""
    echo "Please either:"
    echo "  1. Create a .env file (see .env.template)"
    echo "  2. Export OCTOPUS_SERVER_URL environment variable"
    echo ""
    exit 1
fi

if [ -z "$OCTOPUS_API_KEY" ]; then
    print_error "OCTOPUS_API_KEY environment variable is not set"
    echo ""
    echo "Please either:"
    echo "  1. Create a .env file (see .env.template)"
    echo "  2. Export OCTOPUS_API_KEY environment variable"
    echo ""
    exit 1
fi

print_success "Octopus Deploy credentials configured"

# Now parse the rest of the arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT="$2"
            shift 2
            ;;
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --space)
            SPACE="$2"
            shift 2
            ;;
        --github-repo)
            GITHUB_REPO="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Build command arguments
ARGS=(
    "--project" "$PROJECT"
    "--environment" "$ENVIRONMENT"
    "--space" "$SPACE"
    "--output" "$OUTPUT"
)

if [ -n "$GITHUB_REPO" ]; then
    ARGS+=("--github-repo" "$GITHUB_REPO")
fi

# Print configuration
echo ""
print_info "Configuration:"
echo "  Project:     $PROJECT"
echo "  Environment: $ENVIRONMENT"
echo "  Space:       $SPACE"
echo "  Output:      $OUTPUT"
if [ -n "$GITHUB_REPO" ]; then
    echo "  GitHub Repo: $GITHUB_REPO"
fi
echo ""

# Run the Python script
print_info "Generating release notes..."
echo ""

if python3 "$SCRIPT_DIR/generate_release_notes.py" "${ARGS[@]}"; then
    echo ""
    print_success "Release notes generated successfully!"
    echo ""
    print_info "Output saved to: $OUTPUT"
    
    if [ -f "$OUTPUT" ]; then
        echo ""
        print_info "Preview:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        head -n 20 "$OUTPUT"
        if [ $(wc -l < "$OUTPUT") -gt 20 ]; then
            echo "..."
            echo "(showing first 20 lines, see $OUTPUT for full content)"
        fi
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
else
    echo ""
    print_error "Failed to generate release notes"
    exit 1
fi
