#!/usr/bin/env python3
"""
Script to update requirements.txt file automatically.
Usage: python update_requirements.py
"""

import subprocess
import sys
from pathlib import Path


def update_requirements():
    """Update requirements.txt with currently installed packages."""
    try:
        # Get current directory
        current_dir = Path(__file__).parent
        requirements_file = current_dir / 'requirements.txt'
        
        # Create backup of current requirements.txt
        if requirements_file.exists():
            backup_file = current_dir / 'requirements.txt.backup'
            requirements_file.rename(backup_file)
            print(f'Created backup: {backup_file}')
        
        # Generate new requirements.txt
        result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                              capture_output=True, text=True, check=True)
        
        # Write to requirements.txt
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write('# Auto-generated requirements.txt\n')
            f.write('# Generated using: pip freeze\n\n')
            f.write(result.stdout)
        
        print(f'Successfully updated {requirements_file}')
        print('Installed packages:')
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f'Error running pip freeze: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Error updating requirements.txt: {e}')
        sys.exit(1)


if __name__ == '__main__':
    update_requirements()