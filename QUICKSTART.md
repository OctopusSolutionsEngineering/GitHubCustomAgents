# Quick Start Guide - Release Notes Generator

This guide will help you quickly generate release notes for your Octopus Deploy deployments.

## 1️⃣ Prerequisites Check

Before you begin, make sure you have:
- ✅ Python 3.6 or higher installed
- ✅ Access to your Octopus Deploy instance
- ✅ An Octopus Deploy API key
- ✅ The name of your GitHub repository

## 2️⃣ Configure Environment Variables

### Option A: Using a .env file (Recommended)

1. Copy the template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and fill in your values:
   ```bash
   OCTOPUS_SERVER_URL=https://your-instance.octopus.app
   OCTOPUS_API_KEY=API-XXXXXXXXXXXXXXXXXXXXXXXXXX
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx  # Optional
   ```

3. Load the environment variables:
   ```bash
   source .env  # On Linux/Mac
   # or
   set -a; source .env; set +a  # Alternative for Linux/Mac
   ```

### Option B: Export variables directly

```bash
export OCTOPUS_SERVER_URL="https://your-instance.octopus.app"
export OCTOPUS_API_KEY="API-XXXXXXXXXXXXXXXXXXXXXXXXXX"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"  # Optional
```

## 3️⃣ Generate Release Notes

### Option A: Using the Shell Script (Easiest)

```bash
./generate-release-notes.sh \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo"
```

The shell script provides:
- ✅ Automatic environment variable loading
- ✅ Colored output for better readability
- ✅ Input validation
- ✅ Preview of generated notes

### Option B: Using Python Directly

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo"
```

Replace:
- `"Octopus Copilot Function"` with your project name
- `"Production"` with your environment name
- `"Octopus Copilot"` with your space name
- `"owner/repo"` with your GitHub repository (e.g., `microsoft/vscode`)

## 4️⃣ View the Results

The release notes will be saved to `RELEASE_NOTES.md` by default. You can specify a different output file:

```bash
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo" \
    --output "releases/v1.0.0-notes.md"
```

## 🎯 Example for "Octopus Copilot Function" Project

If you want to generate release notes for the specific project mentioned in this repository:

```bash
# 1. Set your credentials
export OCTOPUS_SERVER_URL="https://your-instance.octopus.app"
export OCTOPUS_API_KEY="API-XXXXXXXXXXXXXXXXXXXXXXXXXX"

# 2. Run the generator (using shell script - recommended)
./generate-release-notes.sh \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "your-org/your-repo"

# OR run using Python directly
python3 generate_release_notes.py \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "your-org/your-repo"

# 3. View the results
cat RELEASE_NOTES.md
```

## 🔍 Troubleshooting

### Error: "OCTOPUS_SERVER_URL environment variable not set"
- Make sure you've exported the environment variable
- Check for typos in the variable name
- Try running `echo $OCTOPUS_SERVER_URL` to verify it's set

### Error: "Space 'XXX' not found"
- Verify the space name is exact (case-sensitive)
- Log in to Octopus Deploy and check the space name in the UI
- Ensure your API key has access to the space

### Error: "No deployments found"
- Verify that at least one deployment exists for the project/environment combination
- Check in Octopus Deploy UI under Project → Deployments

## 📚 Need More Help?

See the full [README.md](README.md) for:
- Detailed setup instructions
- Configuration options
- CI/CD integration examples
- Complete troubleshooting guide
