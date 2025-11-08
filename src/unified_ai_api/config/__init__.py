'''
Configuration package for api_ai.

This package contains all configuration files and related utilities:
- defaults.json: Default configuration values
- providers.json: Provider configurations
- secret.json: API keys and secrets (created from template)

This package is internal to api_ai and should not be imported directly by users.
'''

from pathlib import Path

# Configuration file paths
_CONFIG_DIR = Path(__file__).parent
DEFAULTS_FILE_PATH = _CONFIG_DIR / 'defaults.json'
PROVIDER_FILE_PATH = _CONFIG_DIR / 'providers.json'
SECRET_FILE_PATH = _CONFIG_DIR / 'secret.json'

__all__ = [
    'DEFAULTS_FILE_PATH',
    'PROVIDER_FILE_PATH',
    'SECRET_FILE_PATH',
]
