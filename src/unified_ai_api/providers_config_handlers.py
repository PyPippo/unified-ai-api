from ._utils import load_providers_file
from .types import (
    ProviderAttributes,
    ApiSupportedContent,
    ProvidersFile,
    ProvidersConfigList,
    ProviderName,
    ProvidersConfigParams,
    ApiEndpoints,
    UrlType,
    ApiSupported,
)


class ProvidersConfigHandler:
    """Static handler for provider configuration operations.

    This class provides a namespace for all provider configuration operations,
    making the API more discoverable and maintaining clear separation of concerns.

    Note:
        This class should not be instantiated. All methods are static.

    Usage:
        providers = ProvidersConfigHandler.available_providers()
        config = ProvidersConfigHandler.get_provider_config('OPENROUTER', 0)
        endpoint = ProvidersConfigHandler.get_provider_endpoint('OPENROUTER', 'openai', 0)

        supported_api_list = ProvidersConfigHandler.get_provider_api_supported('OPENROUTER', 0)
        attribute_value_as_str = ProvidersConfigHandler.get_provider_config_attribute(
            'OPENROUTER', 'api_key', config_index=0
        )
    """

    def __init__(self):
        """Prevent instantiation of this utility class."""
        raise TypeError(
            "ProvidersConfigHandler is a utility class and should not be instantiated. "
            "Use its static methods directly."
        )

    @staticmethod
    def available_providers() -> list[ProviderName]:
        """Returns a list of available providers."""
        providers_file: ProvidersFile = load_providers_file()
        return list(providers_file.keys())

    @staticmethod
    def available_provider_configs(provider: ProviderName) -> ProvidersConfigList:
        """Get list of all available provider configurations for a given provider.

        Args:
            provider: Provider name

        Returns:
            List of provider configurations

        Raises:
            ValueError: If provider not found
        """
        providers_file: ProvidersFile = load_providers_file()

        if provider not in providers_file:
            raise ValueError(
                f'Provider "{provider}" not found. Available: {ProvidersConfigHandler.available_providers()}'
            )
        return providers_file[provider]

    @staticmethod
    def get_provider_config(
        provider: ProviderName, config_index: int = 0
    ) -> ProvidersConfigParams:
        """Get provider configuration data by name and index.

        Args:
            provider: Provider name (e.g., 'OPENROUTER', 'HUGGINGFACE')
            config_index: Provider configuration index (default: 0)

        Returns:
            Dictionary containing provider configuration

        Raises:
            ValueError: If provider not found or index out of range
        """
        providers_file: ProvidersFile = load_providers_file()

        if provider not in providers_file:
            raise ValueError(
                f'Provider "{provider}" not found. Available: {ProvidersConfigHandler.available_providers()}'
            )

        provider_configs_list: ProvidersConfigList = providers_file[provider]
        if config_index >= len(provider_configs_list):
            raise ValueError(
                f'Index {config_index} out of range for provider "{provider}" (max: {len(provider_configs_list) - 1})'
            )

        return provider_configs_list[config_index]

    @staticmethod
    def get_provider_config_attribute(
        provider: ProviderName, attribute: ProviderAttributes, config_index: int = 0
    ) -> str:
        """Get specific provider attribute.

        Args:
            provider: Provider name
            attribute: Attribute to retrieve
            config_index: Provider configuration index (default: 0)

        Returns:
            Attribute value as string
        """
        provider_config: ProvidersConfigParams = (
            ProvidersConfigHandler.get_provider_config(provider, config_index)
        )

        if attribute not in provider_config:
            available: list[str] = list(provider_config.keys())
            raise ValueError(
                f'Attribute "{attribute}" not found for provider "{provider}". Available: {available}'
            )

        return str(provider_config[attribute])

    @staticmethod
    def get_provider_api_supported(
        provider: ProviderName, config_index: int = 0
    ) -> ApiSupported:
        """Get supported API types for a provider configuration."""
        provider_config: ProvidersConfigParams = (
            ProvidersConfigHandler.get_provider_config(provider, config_index)
        )
        return provider_config.get('api_supported', [])

    @staticmethod
    def get_provider_endpoint(
        provider: ProviderName,
        endpoint_type: ApiSupportedContent,
        config_index: int = 0,
    ) -> UrlType:
        """Get provider API endpoint by type.

        Args:
            provider: Provider name
            endpoint_type: Type of endpoint to retrieve
            config_index: Provider configuration index (default: 0)

        Returns:
            API endpoint URL
        """
        provider_config: ProvidersConfigParams = (
            ProvidersConfigHandler.get_provider_config(provider, config_index)
        )

        endpoints: ApiEndpoints = provider_config['api_endpoints']
        if endpoint_type not in endpoints:
            available: list[str] = list(endpoints.keys())
            raise ValueError(
                f'Endpoint type "{endpoint_type}" not found for provider "{provider}". Available: {available}'
            )

        return endpoints[endpoint_type]
