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

        # Check critical Wagtail admin files that are essential for functionality
        critical_files = [
            'wagtailadmin/css/core.css',  # Wagtail admin styling
            'wagtailadmin/js/core.js',    # Wagtail admin functionality
            'admin/css/base.css',         # Django admin styling
            'admin/js/core.js',           # Django admin functionality
        ]

        missing_critical = []
        for file_path in critical_files:
            found = False
            # Check for exact match or hashed version
            for manifest_key in paths.keys():
                if manifest_key == file_path or manifest_key.startswith(file_path.replace('.css', '.').replace('.js', '.')):
                    hashed_filename = paths[manifest_key]
                    physical_path = static_root / hashed_filename
                    if physical_path.exists():
                        print(f"OK: {file_path} found as {manifest_key} -> {hashed_filename}")
                        found = True
                        break

            if not found:
                missing_critical.append(file_path)
                print(f"ERROR: Critical file {file_path} not found")

        if missing_critical:
            print(f"ERROR: {len(missing_critical)} critical files missing")
            return False

        # Validate basic file counts
        css_files = [key for key in paths.keys() if key.endswith('.css')]
        js_files = [key for key in paths.keys() if key.endswith('.js')]

        if len(css_files) < 5:
            print(f"WARNING: Only {len(css_files)} CSS files found, expected more")

        if len(js_files) < 10:
            print(f"WARNING: Only {len(js_files)} JS files found, expected more")

        print(f"INFO: Found {len(css_files)} CSS files and {len(js_files)} JS files total")

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