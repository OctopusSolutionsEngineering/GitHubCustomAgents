# Quick Reference Card - Release Notes Generator

## 🚀 Quick Start (3 Steps)

### 1. Configure
```bash
export OCTOPUS_SERVER_URL="https://your-instance.octopus.app"
export OCTOPUS_API_KEY="API-XXXXXXXXXX"
```

### 2. Run
```bash
./generate-release-notes.sh \
    --project "Octopus Copilot Function" \
    --environment "Production" \
    --space "Octopus Copilot" \
    --github-repo "owner/repo"
```

### 3. View
```bash
cat RELEASE_NOTES.md
```

## 📋 Common Commands

### Generate for Default Project
```bash
./generate-release-notes.sh --github-repo "owner/repo"
```

### Custom Output File
```bash
./generate-release-notes.sh \
    --github-repo "owner/repo" \
    --output "v1.0.0-notes.md"
```

### Using Python Directly
```bash
python3 generate_release_notes.py \
    --project "My Project" \
    --environment "Production" \
    --space "Default" \
    --github-repo "owner/repo"
```

## 🔧 Configuration

### Create .env File
```bash
cp .env.template .env
# Edit .env with your credentials
```

### Environment Variables
- `OCTOPUS_SERVER_URL` - Your Octopus instance URL (required)
- `OCTOPUS_API_KEY` - Your Octopus API key (required)
- `GITHUB_TOKEN` - GitHub token (optional, for private repos)
- `GITHUB_REPOSITORY` - Default repo in owner/repo format (optional)

## 🆘 Troubleshooting

| Error | Solution |
|-------|----------|
| "OCTOPUS_SERVER_URL not set" | Export the environment variable or create .env file |
| "Space not found" | Check space name is exact (case-sensitive) |
| "No deployments found" | Verify project was deployed to that environment |
| "No build information" | Configure build info in your CI/CD pipeline |

## 📚 Documentation

- **Full Guide**: `README.md`
- **Quick Start**: `QUICKSTART.md`
- **Implementation Details**: `SUMMARY.md`

## 🎯 Default Values

- **Project**: "Octopus Copilot Function"
- **Environment**: "Production"
- **Space**: "Octopus Copilot"
- **Output**: "RELEASE_NOTES.md"

## 💡 Tips

✅ Use the shell script for easier usage and better error messages  
✅ Store credentials in .env file (never commit it!)  
✅ Add .env to .gitignore (already done)  
✅ Use --help to see all options  

## 🔗 Quick Links

- Get Octopus API Key: Profile → My API Keys
- Get GitHub Token: Settings → Developer settings → Personal access tokens
- Octopus Build Info Docs: https://octopus.com/docs/packaging-applications/build-servers/build-information
