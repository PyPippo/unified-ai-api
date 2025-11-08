'''
Comprehensive unit tests for api_ai package functionality.

Tests cover:
- Advanced APIConnectionManager scenarios
- Integration with actual AI providers (when configured)
- Error handling and edge cases
- Configuration management
'''

import pytest
import os
from unittest.mock import patch, Mock


class TestAPIConnectionManagerAdvanced:
    '''Advanced test suite for APIConnectionManager.'''

    def test_package_exports_all_expected_classes(self):
        '''Test that all expected classes are properly exported.'''
        from unified_ai_api import APIConnectionManager, BaseAPIClient, OpenAICompatibleClient

        assert APIConnectionManager is not None
        assert BaseAPIClient is not None
        assert OpenAICompatibleClient is not None

        # Check that they are the right types
        assert callable(APIConnectionManager)
        assert hasattr(BaseAPIClient, '__abstractmethods__')  # Should be abstract
        assert callable(OpenAICompatibleClient)

    def test_api_connection_manager_full_workflow(self):
        '''Test complete workflow with APIConnectionManager.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Test provider discovery
        providers = manager.get_available_providers()
        assert len(providers) > 0

        # Test getting configs for first provider
        first_provider = providers[0]
        configs = manager.get_provider_configs(first_provider)
        assert len(configs) > 0

        # Test getting supported APIs
        apis = manager.get_supported_api(first_provider, 0)
        assert len(apis) > 0

        # Test connection configuration (may fail if no API key)
        if 'openai' in apis:
            manager.configure_api(first_provider, 0, 'openai')
            # Should be able to validate configuration
            result = manager.validate_configuration()
            assert isinstance(result, bool)

    def test_connection_state_management(self):
        '''Test that connection state is properly managed.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Initially not connected - returns empty strings
        params = manager.get_connection_params()
        assert isinstance(params, dict)
        assert params.get('provider') == ''

        # After successful configuration (if possible)
        try:
            manager.configure_api('OPENROUTER', 0, 'openai')
            success = manager.validate_configuration()
            if success:
                params = manager.get_connection_params()
                assert params.get('provider') != ''
                assert 'model_name' in params
        except (ValueError, FileNotFoundError, KeyError):
            # Expected when no API key is available
            pass

    def test_multiple_connections(self):
        '''Test creating multiple connections in sequence.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Configure first connection
        try:
            manager.configure_api('OPENROUTER', 0, 'openai')
            result1 = manager.validate_configuration()
            assert isinstance(result1, bool)
        except (ValueError, FileNotFoundError, KeyError):
            result1 = False

        # Configure second connection (should replace first)
        try:
            manager.configure_api('HUGGINGFACE', 0, 'openai')
            result2 = manager.validate_configuration()
            assert isinstance(result2, bool)

            # If second succeeded, params should reflect HUGGINGFACE
            if result2:
                params = manager.get_connection_params()
                assert params != {}
        except (ValueError, FileNotFoundError, KeyError):
            result2 = False

    def test_interactive_setup_functionality(self):
        '''Test that interactive_setup method exists and is callable.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Method should exist
        assert hasattr(manager, 'interactive_setup')
        assert callable(manager.interactive_setup)

    def test_start_chat_loop_functionality(self):
        '''Test that start_chat_loop method exists and raises error when not connected.'''
        from unified_ai_api import APIConnectionManager
        from unified_ai_api.compatible_client_api import InvalidParameterError

        manager = APIConnectionManager()

        # Method should exist
        assert hasattr(manager, 'start_chat_loop')
        assert callable(manager.start_chat_loop)

        # Should raise InvalidParameterError when no connection configured
        with pytest.raises(InvalidParameterError):
            manager.start_chat_loop()


class TestConfigurationSystem:
    '''Test suite for configuration system functionality.'''

    def test_providers_config_handler_integration(self):
        '''Test ProvidersConfigHandler class methods.'''
        from unified_ai_api.providers_config_handlers import ProvidersConfigHandler

        # Test available_providers
        providers = ProvidersConfigHandler.available_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0

        # Test available_provider_configs
        configs = ProvidersConfigHandler.available_provider_configs(providers[0])
        assert isinstance(configs, list)
        assert len(configs) > 0

        # Test get_provider_api_supported
        apis = ProvidersConfigHandler.get_provider_api_supported(providers[0], 0)
        assert isinstance(apis, list)
        assert len(apis) > 0

    def test_auth_keys_integration(self):
        '''Test auth_keys module integration.'''
        from unified_ai_api.auth_keys import get_secret_api_key

        # Should be callable without crashing
        try:
            key = get_secret_api_key('OPENROUTER')
            assert isinstance(key, str)
        except (ValueError, FileNotFoundError, KeyError):
            # Expected when no config is available
            pass

    def test_types_system(self):
        '''Test that type system is properly structured.'''
        from unified_ai_api.types import ApiSupportedContent, ProviderName

        # Types should be importable
        assert ApiSupportedContent is not None
        assert ProviderName is not None


class TestErrorHandlingAdvanced:
    '''Advanced error handling tests.'''

    def test_robust_error_handling(self):
        '''Test robust error handling across various scenarios.'''
        from unified_ai_api import APIConnectionManager
        from unified_ai_api.compatible_client_api import InvalidParameterError

        manager = APIConnectionManager()

        # Test with out-of-range config index - should raise InvalidParameterError
        with pytest.raises(InvalidParameterError):
            manager.configure_api('OPENROUTER', 999, 'openai')

        # Should still be able to get params after failed configuration attempt
        params = manager.get_connection_params()
        assert isinstance(params, dict)

    def test_concurrent_operations(self):
        '''Test that manager handles rapid sequential operations.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Rapid sequential calls should not break
        for i in range(5):
            providers = manager.get_available_providers()
            assert isinstance(providers, list)

            params = manager.get_connection_params()
            assert isinstance(params, dict)


class TestClientImplementations:
    '''Test suite for client implementations.'''

    def test_base_api_client_is_abstract(self):
        '''Test that BaseAPIClient cannot be instantiated directly.'''
        from unified_ai_api import BaseAPIClient

        # Should be abstract and not instantiable
        with pytest.raises(TypeError):
            BaseAPIClient()

    def test_openai_compatible_client_instantiation(self):
        '''Test that OpenAICompatibleClient can be instantiated with proper parameters.'''
        from unified_ai_api import OpenAICompatibleClient

        # Should be instantiable with proper parameters
        client = OpenAICompatibleClient(
            base_url="https://api.test.com", api_key="test-key", model_name="test-model"
        )

        assert client is not None
        assert hasattr(client, 'chat_completion')
        assert hasattr(client, 'get_model_name')
        assert client.get_model_name() == "test-model"


# Integration tests
def test_end_to_end_workflow():
    '''Test complete end-to-end workflow.'''
    from unified_ai_api import APIConnectionManager

    manager = APIConnectionManager()

    # Step 1: Discover providers
    providers = manager.get_available_providers()
    assert len(providers) > 0

    # Step 2: Get configurations for a provider
    configs = manager.get_provider_configs(providers[0])
    assert len(configs) > 0

    # Step 3: Check supported APIs
    apis = manager.get_supported_api(providers[0], 0)
    assert len(apis) > 0

    # Step 4: Attempt configuration (may fail without API key)
    if 'openai' in apis:
        try:
            manager.configure_api(providers[0], 0, 'openai')
            result = manager.validate_configuration()
            # Just check it returns a boolean
            assert isinstance(result, bool)
        except (ValueError, FileNotFoundError, KeyError):
            # Expected when no API key is available
            pass

    # Step 5: Check final state
    params = manager.get_connection_params()
    assert isinstance(params, dict)


if __name__ == '__main__':
    # Run tests if called directly
    pytest.main([__file__, '-v'])
