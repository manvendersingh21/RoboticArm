# GitHub Repository Setup Guide

This guide will help you create a GitHub repository for this MuJoCo robotic arm project and push the code.

## Prerequisites

You need the GitHub CLI (`gh`) installed and authenticated.

### 1. Check if GitHub CLI is installed

```bash
gh --version
```

If not installed, follow the installation instructions at: https://cli.github.com/

**Quick install commands:**
- **macOS**: `brew install gh`
- **Ubuntu/Debian**: `sudo apt install gh`
- **Windows**: Download from https://cli.github.com/

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate with your GitHub account.

## Option A: Automated Setup (Recommended)

Run the provided setup script:

```bash
./setup_github.sh
```

This will:
1. Verify GitHub CLI is installed and authenticated
2. Create a new public repository named `mujoco-robotic-arm`
3. Push all code to GitHub
4. Provide you with the repository URL

## Option B: Manual Setup

If you prefer to create the repository manually or need more control:

### 1. Create Repository via GitHub CLI

```bash
gh repo create mujoco-robotic-arm \
  --public \
  --description "MuJoCo robotic arm simulation with gripper functionality for object manipulation" \
  --source=. \
  --remote=origin \
  --push
```

### 2. Or Create Repository on GitHub.com

1. Visit https://github.com/new
2. Repository name: `mujoco-robotic-arm`
3. Description: "MuJoCo robotic arm simulation with gripper functionality for object manipulation"
4. Choose: Public
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

Then push your local repository:

```bash
# Rename branch to main (optional but recommended)
git branch -M main

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/mujoco-robotic-arm.git

# Push code
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Verify Repository

After creation, verify your repository:

```bash
gh repo view --web
```

This will open your repository in a web browser.

## Update README

After creating the repository, update the README.md file to replace:

```markdown
git clone https://github.com/YOUR_USERNAME/mujoco-robotic-arm.git
```

with your actual GitHub username:

```markdown
git clone https://github.com/yourusername/mujoco-robotic-arm.git
```

Then commit and push the change:

```bash
git add README.md
git commit -m "Update repository URL in README"
git push
```

## Common Issues

### Issue: "gh: command not found"

**Solution**: Install GitHub CLI following the instructions at https://cli.github.com/

### Issue: "You are not logged into any GitHub hosts"

**Solution**: Run `gh auth login` and follow the authentication prompts.

### Issue: "Repository already exists"

**Solution**: 
- Choose a different repository name, or
- Delete the existing repository on GitHub and try again, or
- Push to the existing repository:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/mujoco-robotic-arm.git
  git push -u origin main
  ```

### Issue: Authentication failed

**Solution**: 
- Regenerate your GitHub token
- Run `gh auth logout` followed by `gh auth login`
- Ensure your token has the necessary permissions (repo scope)

## Next Steps

Once your repository is created and pushed:

1. **Add Topics**: Visit your repository settings and add topics like:
   - `mujoco`
   - `robotics`
   - `simulation`
   - `python`
   - `inverse-kinematics`
   - `robotic-arm`

2. **Add a Description**: Ensure your repository has a clear description

3. **Enable Issues**: If you want to track bugs and feature requests

4. **Add Collaborators**: If working with a team

5. **Set up GitHub Pages** (optional): To host documentation

6. **Add CI/CD** (optional): Set up GitHub Actions for testing

## Support

If you encounter any issues, please:
1. Check the GitHub CLI documentation: https://cli.github.com/manual/
2. Review GitHub's repository creation guide: https://docs.github.com/en/repositories/creating-and-managing-repositories
3. Open an issue in the repository after it's created

---

**Happy coding! 🤖**
