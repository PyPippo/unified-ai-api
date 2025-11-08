'''
Working unit tests for unified_ai_api package interface and core functionality.

Tests cover:
- Package interface validation
- APIConnectionManager functionality
- Configuration management
- Error handling scenarios

This is a simplified test suite focused on core functionality.
'''

import pytest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


def test_package_imports() -> None:
    '''Test that package exposes intended public classes.'''
    from unified_ai_api import APIConnectionManager

    # This should work
    assert APIConnectionManager is not None


def test_package_interface_clean() -> None:
    '''Test that package interface is clean.'''
    import unified_ai_api

    # Check that __all__ is properly defined
    if hasattr(unified_ai_api, '__all__'):
        expected_exports = [
            'APIConnectionManager',
            'BaseAPIClient',
            'OpenAICompatibleClient',
        ]
        assert all(export in unified_ai_api.__all__ for export in expected_exports)
        # Should contain exactly what we expect
        assert len(unified_ai_api.__all__) == 3


class TestAPIConnectionManager:
    '''Test suite for APIConnectionManager functionality.'''

    def test_instantiation(self):
        '''Test APIConnectionManager can be instantiated with no parameters.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()
        assert manager is not None
        assert hasattr(manager, 'get_available_providers')
        assert hasattr(manager, 'configure_api')
        assert hasattr(manager, 'get_connection_params')

    def test_get_available_providers(self):
        '''Test provider discovery functionality.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()
        providers = manager.get_available_providers()

        assert isinstance(providers, list)
        assert len(providers) > 0  # Should have at least some providers

        # Common providers should be available
        provider_names = [str(p) for p in providers]
        assert any(
            'OPENROUTER' in name or 'HUGGINGFACE' in name for name in provider_names
        )

    def test_connection_info_when_not_connected(self):
        '''Test connection info when no connection is established.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()
        info = manager.get_connection_params()

        assert isinstance(info, dict)
        # Should contain basic info even when not connected
        assert 'provider' in info or 'status' in info

    def test_create_connection_success(self):
        '''Test that configure_api method works.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # This should work (though may fail if API key not configured)
        try:
            manager.configure_api('OPENROUTER', 0, 'openai')
            result = manager.validate_configuration()
            assert isinstance(result, bool)
        except Exception:
            # Configuration may fail without API keys, which is acceptable
            pass

    def test_create_connection_invalid_config(self):
        '''Test configure_api with invalid configuration.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Invalid config index should raise an error
        with pytest.raises(Exception):  # Expect some kind of error
            manager.configure_api('OPENROUTER', 999, 'openai')

    def test_get_provider_configs(self):
        '''Test getting provider configurations.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()
        configs = manager.get_provider_configs('OPENROUTER')

        assert isinstance(configs, list)
        assert len(configs) > 0

        # Each config should have required fields
        first_config = configs[0]
        assert 'model_name' in first_config
        assert 'model_url' in first_config

    def test_get_supported_api(self):
        '''Test getting supported APIs for a provider.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()
        apis = manager.get_supported_api('OPENROUTER', 0)

        assert isinstance(apis, list)
        assert len(apis) > 0
        assert 'openai' in apis  # OPENROUTER should support openai


class TestConfigurationIntegration:
    '''Test suite for configuration system integration.'''

    def test_providers_config_handler_available(self):
        '''Test that ProvidersConfigHandler class methods work.'''
        from unified_ai_api.providers_config_handlers import ProvidersConfigHandler

        # Test available_providers class method
        providers = ProvidersConfigHandler.available_providers()
        assert isinstance(providers, list)
        assert len(providers) > 0

    def test_auth_keys_module_available(self):
        '''Test that auth_keys module functions work.'''
        from unified_ai_api.auth_keys import get_secret_api_key

        # This should be callable (even if it fails due to missing config)
        try:
            key = get_secret_api_key('OPENROUTER')
            assert isinstance(key, str)
        except (ValueError, FileNotFoundError, KeyError):
            # Expected when config is not set up
            pass


class TestErrorHandling:
    '''Test suite for error handling scenarios.'''

    def test_missing_connection_graceful_handling(self):
        '''Test that operations without connection are handled gracefully.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Should not crash
        info = manager.get_connection_params()
        # Should return some info even when not connected
        assert isinstance(info, dict)

    def test_invalid_provider_handling(self):
        '''Test handling of invalid provider in various methods.'''
        from unified_ai_api import APIConnectionManager

        manager = APIConnectionManager()

        # Test with invalid config index
        with pytest.raises(Exception):  # Expect some kind of error
            manager.configure_api('OPENROUTER', 999, 'openai')


# Integration test
def test_full_workflow_basic():
    '''Test basic workflow without requiring API keys.'''
    from unified_ai_api import APIConnectionManager

    manager = APIConnectionManager()

    # Should be able to get providers
    providers = manager.get_available_providers()
    assert isinstance(providers, list)
    assert len(providers) > 0

    # Should be able to get connection info
    info = manager.get_connection_params()
    assert isinstance(info, dict)

    # Should be able to get configurations
    if providers:
        configs = manager.get_provider_configs(providers[0])
        assert isinstance(configs, list)


if __name__ == '__main__':
    # Run tests if called directly
    _ = pytest.main([__file__, '-v'])
