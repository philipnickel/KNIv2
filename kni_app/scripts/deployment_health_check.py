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

        # Check critical files
        critical_files = [
            'images/favicons/favicon.ico',
            'images/favicons/favicon.svg',
            'images/favicons/apple-touch-icon.png',
        ]

        missing_files = []
        for file_path in critical_files:
            if file_path not in paths:
                missing_files.append(file_path)
                print(f"WARNING: {file_path} not found in manifest")
            else:
                hashed_filename = paths[file_path]
                physical_path = static_root / hashed_filename
                if not physical_path.exists():
                    missing_files.append(file_path)
                    print(f"ERROR: {hashed_filename} not found on filesystem")
                else:
                    print(f"OK: {file_path} -> {hashed_filename}")

        if missing_files:
            print(f"ERROR: {len(missing_files)} critical files missing")
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