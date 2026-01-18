#!/usr/bin/env python
"""
Build script for Network Monitor plugin
Run this to create a .egg file for distribution
"""

import subprocess
import sys
import os

def build_plugin():
    """Build the plugin egg file"""
    print("Building Network Monitor plugin...")
    result = subprocess.run([sys.executable, "setup.py", "bdist_egg"], cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("\n✓ Plugin built successfully!")
        print("The .egg file is in the 'dist' directory")
        print("\nTo install:")
        print("  Copy the .egg file to your Deluge plugins directory")
        print("  Windows: %APPDATA%\\Deluge\\plugins\\")
        return True
    else:
        print("\n✗ Build failed. Check errors above.")
        return False

if __name__ == "__main__":
    success = build_plugin()
    sys.exit(0 if success else 1)
