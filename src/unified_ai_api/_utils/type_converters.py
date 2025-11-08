'''
Data extraction and filtering utilities for typed configuration structures.

This module provides functions to extract and filter already-typed configuration data.
Configuration loading and type validation is handled by config_loaders.py.
'''

from ..types import (
    ProvidersConfigParams,
    ProvidersConfigList,
    ProvidersFile,
    ApiSupportedContent,
    PROVIDER_ATTRIBUTES,
    ApiSupported,
    ApiEndpoints,
)

__all__ = [
    'filter_providers_by_api_type',
    'extract_supported_apis',
    'validate_provider_config_fields',
]


def filter_providers_by_api_type(
    providers: ProvidersFile, api_type: ApiSupportedContent
) -> ProvidersFile:
    '''
    Filter providers that support a specific API type.

    Args:
        providers: Typed provider configurations
        api_type: API type to filter by (e.g., 'openai', 'requests', 'huggingface_hub')

    Returns:
        Filtered providers that support the specified API type
    '''
    filtered: ProvidersFile = {}

    for provider_name, configs in providers.items():
        matching_configs: ProvidersConfigList = [
            config for config in configs if api_type in config['api_supported']
        ]
        if matching_configs:
            filtered[provider_name] = matching_configs

    return filtered


def extract_supported_apis(providers: ProvidersFile) -> set[ApiSupportedContent]:
    '''
    Extract all unique API types supported across all providers.

    Args:
        providers: Typed provider configurations

    Returns:
        Set of all supported API types
    '''
    supported_apis: set[ApiSupportedContent] = set()

    for configs in providers.values():
        for config in configs:
            supported_apis.update(config['api_supported'])

    return supported_apis


def validate_provider_config_fields(config: ProvidersConfigParams) -> bool:
    '''
    Validate that a provider configuration has all required fields.
    Works with already-typed configuration data.

    Args:
        config: Typed configuration to validate

    Returns:
        True if all required fields are present and non-empty
    '''
    # Use the constant derived from the type - single source of truth
    for field in PROVIDER_ATTRIBUTES:
        if field not in config:
            return False

        # Check for non-empty values
        value: str | ApiSupported | ApiEndpoints = config[field]
        if isinstance(value, str) and not value.strip():
            return False
        elif isinstance(value, (list, dict)) and not value:
            return False

    return True
