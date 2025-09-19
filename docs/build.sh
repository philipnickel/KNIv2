#!/bin/bash

# Build script for KNIv2 documentation with MkDocs
# This script builds the documentation locally for testing

set -e

echo "🔨 Building KNIv2 documentation with MkDocs..."

# Check if we're in the right directory
if [ ! -f "../mkdocs.yml" ]; then
    echo "❌ Error: Please run this script from the docs/ directory"
    exit 1
fi

# Install dependencies if not already installed
if ! command -v mkdocs &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r ../requirements.txt
fi

# Build documentation
echo "📚 Building documentation..."
cd ..
mkdocs build

echo "✅ Documentation build complete!"
echo "📖 Open site/index.html in your browser to view the documentation"
echo "🚀 Or run 'mkdocs serve' to start a live development server"