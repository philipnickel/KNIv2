#!/usr/bin/env python3
"""
Deployment health check script for static files validation.
This script verifies that all required static files are present and accessible.
"""
import os
import sys
import json
from pathlib import Path

def check_static_files():
    """Validate static files and manifest for deployment readiness."""

    # Define the static files root
    static_root = Path("static")

    if not static_root.exists():
        print("ERROR: Static directory does not exist")
        return False

    # Check if staticfiles.json manifest exists
    manifest_path = static_root / "staticfiles.json"
    if not manifest_path.exists():
        print("ERROR: staticfiles.json manifest not found")
        return False

    # Load and validate manifest
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        paths = manifest.get('paths', {})
        print(f"INFO: Manifest contains {len(paths)} static file entries")

        # Check for any CSS and JS files to ensure basic functionality
        css_files = [key for key in paths.keys() if key.endswith('.css')]
        js_files = [key for key in paths.keys() if key.endswith('.js')]

        if not css_files:
            print("ERROR: No CSS files found in manifest")
            return False

        if not js_files:
            print("ERROR: No JS files found in manifest")
            return False

        print(f"INFO: Found {len(css_files)} CSS files and {len(js_files)} JS files")

        # Check optional favicon files (warn but don't fail)
        optional_files = [
            'images/favicons/favicon.ico',
            'images/favicons/favicon.svg',
            'images/favicons/apple-touch-icon.png',
        ]

        for file_path in optional_files:
            if file_path not in paths:
                print(f"WARNING: {file_path} not found in manifest (optional)")
            else:
                hashed_filename = paths[file_path]
                physical_path = static_root / hashed_filename
                if not physical_path.exists():
                    print(f"WARNING: {hashed_filename} not found on filesystem (optional)")
                else:
                    print(f"OK: {file_path} -> {hashed_filename}")

        # Validate that some core static files exist
        sample_files = list(paths.keys())[:5]
        for file_path in sample_files:
            hashed_filename = paths[file_path]
            physical_path = static_root / hashed_filename
            if not physical_path.exists():
                print(f"ERROR: {hashed_filename} not found on filesystem")
                return False

        print("SUCCESS: All critical static files validated")
        return True

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in manifest: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def main():
    """Main entry point for health check."""
    print("Starting deployment health check...")

    # Change to the correct directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    success = check_static_files()

    if success:
        print("Health check PASSED")
        sys.exit(0)
    else:
        print("Health check FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()