#!/bin/bash

# Fetch the latest tag to help the user know what the next version should be
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
if [ -z "$LATEST_TAG" ]; then
  LATEST_TAG="None (This will be your first release!)"
fi

# Check if version is provided
if [ -z "$1" ]; then
  echo "❌ Error: Please provide a version number."
  echo "📌 The last released version was: $LATEST_TAG"
  echo "👉 Usage: $0 vX.Y.Z (e.g. v1.0.1)"
  exit 1
fi

VERSION=$1

echo "📦 Preparing release for $VERSION..."

# 1. Create the tag
git tag $VERSION
if [ $? -eq 0 ]; then
  echo "✅ Tag $VERSION created locally."
else
  echo "❌ Failed to create tag. Does it already exist?"
  exit 1
fi

# 2. Push the tag to GitHub
echo "🚀 Pushing tag to GitHub to trigger the automated build..."
git push origin $VERSION
if [ $? -eq 0 ]; then
  echo "🎉 Success! The GitHub Action has been triggered."
  echo "⏳ Wait about 2-3 minutes, then check your GitHub Releases page."
else
  echo "❌ Failed to push the tag."
  exit 1
fi
