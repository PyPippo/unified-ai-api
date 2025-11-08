from typing import Literal, TypeAlias, TypedDict, get_args
from sys import version_info

from .api_types import ApiSupported, ApiEndpoints, UrlType


__all__ = [
    # provider name
    'ProviderName',
    'PROVIDER_NAMES',
    # provider config params
    'ProvidersConfigParams',
    'ProvidersConfigList',
    'ProvidersFile',
    # provider attributes = config attributes + secret api key
    'ProviderAttributes',
    'PROVIDER_ATTRIBUTES',
]


# Dynamic ProviderName type generation based on providers.json
def _get_provider_names_from_config() -> list[str]:
    """
    Extract provider names from providers.json configuration file.

    This function dynamically reads the providers.json file and extracts
    the top-level keys (provider names) to generate the ProviderName type.

    Returns:
        List of provider names from configuration

    Note:
        This approach allows adding new providers by simply updating providers.json
        without needing to modify the ProviderName type definition.
    """
    try:
        # Import here to avoid circular imports during module initialization
        from .._utils.config_loaders import load_providers_file

        providers_file = load_providers_file()
        return list(providers_file.keys())
    except Exception:
        # Fallback to hardcoded values if config loading fails
        # This ensures the module can still be imported during development
        return ['HUGGINGFACE', 'OPENAI', 'OPENROUTER']


# Static fallback for import compatibility and older Python versions
ProviderName: TypeAlias = Literal['HUGGINGFACE', 'OPENAI', 'OPENROUTER']

# Python 3.11+ enhancement with dynamic values
if version_info >= (3, 11):
    try:
        # Generate provider names from configuration
        _DYNAMIC_PROVIDER_NAMES = _get_provider_names_from_config()
        # This DOES work and is equivalent to the static version
        ProviderName = Literal[*_DYNAMIC_PROVIDER_NAMES]  # type: ignore
    except (TypeError, SyntaxError):
        # Keep static fallback if anything goes wrong
        pass

# Concrete instance derived from the configuration - single source of truth
PROVIDER_NAMES: list[str] = list(get_args(ProviderName))


# Runtime validation function (required by project specification memory)
def is_valid_provider_name(provider_name: str) -> bool:
    """
    Validate if a provider name exists in the current configuration.

    Args:
        provider_name: Provider name to validate

    Returns:
        True if provider exists in providers.json, False otherwise

    Note:
        This function provides runtime validation as required by the
        Provider Name Validation specification memory.
    """
    return provider_name in PROVIDER_NAMES



# Type for the provider configuration parameters
class ProvidersConfigParams(TypedDict, total=False):
    config_name: str
    '''Configuration name usually a sub-string of model name'''
    model_url: UrlType
    '''Link to the model page'''
    model_name: str
    '''Official name of the model'''
    init_config_msg: str
    '''A unique identifier for the provider's api key'''
    api_supported: ApiSupported
    '''A list of supported APIs'''
    api_endpoints: ApiEndpoints
    '''A dictionary of endpoints for the provider's api'''


ProvidersConfigList: TypeAlias = list[ProvidersConfigParams]

# Type alias for the complete providers.json file structure
# Maps provider names (e.g., "OPENROUTER", "HUGGINGFACE") to lists of their configurations
ProvidersFile: TypeAlias = dict[ProviderName, ProvidersConfigList]


# Type for all the attributes of a provider config
ProviderAttributes: TypeAlias = Literal[
    'config_name',
    'model_url',
    'model_name',
    'init_config_msg',
    'api_supported',
    'api_endpoints',
]

# Concrete instance derived from the type - single source of truth
PROVIDER_ATTRIBUTES: list[ProviderAttributes] = list(get_args(ProviderAttributes))
