'''
Configuration file loading utilities.

This module provides functions for loading and caching configuration files
with proper error handling and type safety.
'''

import json
from typing import cast
from functools import lru_cache

from ..config import DEFAULTS_FILE_PATH, PROVIDER_FILE_PATH, SECRET_FILE_PATH
from ..types import ProvidersFile, SecretsConfig, DefaultsConfig


__all__ = [
    'load_providers_file',
    'load_secrets_config',
    'load_defaults_config',
    'clear_config_cache',
]


@lru_cache(maxsize=1)
def load_providers_file() -> ProvidersFile:
    '''
    Load and cache provider configuration from JSON file.

    Returns:
        Dictionary mapping provider names to lists of their configurations

    Raises:
        ValueError: If file is missing or contains invalid JSON
    '''
    try:
        with open(PROVIDER_FILE_PATH, 'r', encoding='utf-8') as f:
            return cast(ProvidersFile, json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(
            f'Failed to load provider config from {PROVIDER_FILE_PATH}: {e}'
        ) from e


@lru_cache(maxsize=1)
def load_secrets_config() -> SecretsConfig:
    '''
    Load and cache secrets configuration from JSON file.

    Returns:
        Dictionary containing API keys and secrets

    Raises:
        ValueError: If file is missing or contains invalid JSON
    '''
    try:
        with open(SECRET_FILE_PATH, 'r', encoding='utf-8') as f:
            return cast(SecretsConfig, json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(
            f'Failed to load secrets config from {SECRET_FILE_PATH}: {e}'
        ) from e


@lru_cache(maxsize=1)
def load_defaults_config() -> DefaultsConfig:
    '''
    Load and cache default configuration from JSON file.

    Returns:
        Dictionary containing default configuration values

    Raises:
        ValueError: If file is missing or contains invalid JSON
    '''
    try:
        with open(DEFAULTS_FILE_PATH, 'r', encoding='utf-8') as f:
            return cast(DefaultsConfig, json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(
            f'Failed to load defaults config from {DEFAULTS_FILE_PATH}: {e}'
        ) from e


def clear_config_cache() -> None:
    '''
    Clear all configuration caches.

    This is useful for testing or when configuration files are updated
    and you need to reload them.
    '''
    load_providers_file.cache_clear()
    load_secrets_config.cache_clear()
    load_defaults_config.cache_clear()
