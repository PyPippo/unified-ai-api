'''
Authentication key management for api_ai package.

This module handles secure loading of API keys from configuration files
with environment variable fallbacks for production deployment.
API keys are stored in secret.json and referenced by providers.json.
'''

from .providers_config_handlers import ProvidersConfigHandler
from .types import (
    SecretsConfig,
    ProviderName,
)
from ._utils.config_loaders import load_secrets_config


def get_secret_api_key(
    provider: ProviderName, config_name: str | None = None, config_index: int = 0
) -> str:
    '''
    Retrieve API key for a specific provider with environment variable fallback.

    Args:
        provider: Provider name (e.g., 'OPENROUTER', 'HUGGINGFACE')

    Returns:
        API key string

    Raises:
        ValueError: If provider not found or API key not configured
        FileNotFoundError: If configuration files are missing
        KeyError: If API key reference is invalid

    '''

    if config_name is None:
        # use config_index value if provided, otherwise default to 0
        return _get_api_key_from_config_index(provider, config_index=config_index)
    else:
        return _get_api_key_from_config_name(provider, config_name)


def _get_api_key_from_config_index(
    provider: ProviderName, config_index: int = 0
) -> str:
    '''
    Get API key from configuration files (original implementation).
    '''

    # Get the raw API key reference and validate it's a valid ApiKeyType
    api_key_ref: str = ProvidersConfigHandler.get_provider_config_attribute(
        provider=provider, attribute='config_name', config_index=config_index
    )

    secret_file_conf: SecretsConfig = load_secrets_config()

    return secret_file_conf[api_key_ref]


def _get_api_key_from_config_name(provider: ProviderName, config_name: str) -> str:
    '''
    Get API key from configuration files (original implementation).
    '''

    secret_file_conf: SecretsConfig = load_secrets_config()
    if config_name in secret_file_conf:
        return secret_file_conf[config_name]
    else:
        raise ValueError(
            f'No API key found for {provider} with config name {config_name}'
        )
