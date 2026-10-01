#!/bin/bash

# GitHub Repository Setup Script for MuJoCo Robotic Arm Project

echo "================================================"
echo "  MuJoCo Robotic Arm - GitHub Setup Script"
echo "================================================"
echo

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo
    echo "Please install it from: https://cli.github.com/"
    echo
    echo "Installation commands:"
    echo "  macOS:   brew install gh"
    echo "  Linux:   See https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo "  Windows: See https://github.com/cli/cli#windows"
    exit 1
fi

echo "✓ GitHub CLI is installed"
echo

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "⚠️  You are not logged into GitHub"
    echo
    echo "Please authenticate with GitHub CLI:"
    echo "  gh auth login"
    echo
    echo "Then run this script again."
    exit 1
fi

echo "✓ GitHub CLI is authenticated"
echo

# Repository details
REPO_NAME="mujoco-robotic-arm"
DESCRIPTION="MuJoCo robotic arm simulation with gripper functionality for object manipulation"

echo "Repository Details:"
echo "  Name:        $REPO_NAME"
echo "  Description: $DESCRIPTION"
echo "  Visibility:  Public"
echo

read -p "Do you want to create this repository? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Repository creation cancelled."
    exit 0
fi

# Create repository
echo
echo "Creating GitHub repository..."
if gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin --push; then
    echo
    echo "================================================"
    echo "✓ Repository created successfully!"
    echo "================================================"
    echo
    echo "Repository URL:"
    gh repo view --web --json url -q .url
    echo
    echo "Next steps:"
    echo "  1. Visit your repository on GitHub"
    echo "  2. Follow the README for installation instructions"
    echo "  3. Start simulating with: python robotic_arm_sim.py"
    echo
else
    echo
    echo "❌ Failed to create repository."
    echo
    echo "You can create it manually:"
    echo "  1. Visit https://github.com/new"
    echo "  2. Create a repository named: $REPO_NAME"
    echo "  3. Then run:"
    echo "     git remote add origin git@github.com:YOUR_USERNAME/$REPO_NAME.git"
    echo "     git branch -M main"
    echo "     git push -u origin main"
    exit 1
fi
