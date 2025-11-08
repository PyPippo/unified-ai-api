#!/usr/bin/env python3
"""
REST API Example - Generic REST API Integration

This example demonstrates how to use the package with generic REST APIs
that might not follow the OpenAI-compatible format. It shows the flexibility
of the unified interface.

Features demonstrated:
- REST API client configuration
- Timeout configuration
- Error handling for network issues
- Custom request/response handling

To run: python examples/rest_api_example.py
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from unified_ai_api import APIConnectionManager


def main() -> None:
    """Demonstrate REST API usage with custom configuration."""
    print('🌐 Unified AI API - REST API Example')
    print('=' * 45)

    # Initialize manager
    manager = APIConnectionManager()

    try:
        # Check available providers for REST-compatible ones
        providers = manager.get_available_providers()
        print(f'Available providers: {providers}')

        # Look for HuggingFace or other REST-compatible provider
        rest_provider = None
        for provider in providers:
            try:
                configs = manager.get_provider_configs(provider)
                if configs:
                    supported_apis = manager.get_supported_api(provider, 0)
                    if 'requests' in supported_apis or 'rest' in supported_apis:
                        rest_provider = provider
                        print(f'Found REST-compatible provider: {provider}')
                        break
            except Exception:
                continue

        if not rest_provider:
            print('⚠️  No REST-compatible providers found in configuration.')
            print('Falling back to OpenAI-compatible provider for demonstration...')
            rest_provider = providers[0] if providers else 'OPENROUTER'

        # Configure the REST connection
        print(f'Configuring connection to {rest_provider}...')

        # Get supported API types for this provider
        supported_apis = manager.get_supported_api(rest_provider, 0)
        print(f'Supported APIs: {supported_apis}')

        # Choose the best API type
        api_type = 'requests' if 'requests' in supported_apis else supported_apis[0]

        manager.configure_api(provider=rest_provider, config_index=0, api_type=api_type)

        print(f'✅ Configured with API type: {api_type}')

        # Create client with custom timeout configuration
        print('Creating REST client with custom timeouts...')
        with manager.create_chatclient(session_id='rest_example') as client:

            # Configure timeouts if the client supports it
            try:
                if hasattr(client.compatible_client, 'configure_rest_timeouts'):
                    client.compatible_client.configure_rest_timeouts(
                        connect_timeout=15.0,  # 15 second connection timeout
                        read_timeout=45.0,  # 45 second read timeout
                    )
                    print('✅ Custom timeouts configured (15s connect, 45s read)')
            except Exception as e:
                print(f'⚠️  Timeout configuration not available: {e}')

            print(f'Connected to: {client.get_model_name()}')
            print(
                'Status:',
                '🟢 Connected' if client.get_connection_status() else '🔴 Disconnected',
            )

            # Test messages with various complexities
            test_scenarios = [
                {'name': 'Simple Query', 'message': 'What is machine learning?'},
                {
                    'name': 'Technical Question',
                    'message': 'Explain the difference between supervised and unsupervised learning with examples.',
                },
                {
                    'name': 'Code Request',
                    'message': 'Write a simple Python function to calculate the factorial of a number.',
                },
            ]

            print('\n🚀 Testing REST API with different scenarios...\n')

            for i, scenario in enumerate(test_scenarios, 1):
                print(f'📝 Scenario {i}: {scenario["name"]}')
                print(f'👤 Query: {scenario["message"]}')

                try:
                    response = client.send_message(scenario['message'])
                    if response:
                        # Show response length and first part
                        response_length = len(response)
                        display_response = (
                            response[:250] + '...' if len(response) > 250 else response
                        )
                        print(
                            f'🤖 Response ({response_length} chars): {display_response}'
                        )
                        print('✅ Success')
                    else:
                        print('❌ No response received')
                except Exception as e:
                    print(f'❌ Error: {e}')

                print('-' * 50)

            # Demonstrate connection info
            print('\n📊 Connection Information:')
            connection_params = client.get_connection_params()
            for key, value in connection_params.items():
                print(f'  {key}: {value}')

        print('\n✅ REST API example completed successfully!')

    except Exception as e:
        print(f'❌ Error: {e}')
        print('\n🔧 Troubleshooting:')
        print('1. Check your API key configuration')
        print('2. Verify network connectivity')
        print('3. Ensure the provider supports REST API calls')
        print('4. Check if the API endpoint is accessible')
        print('5. Review rate limits and quotas')


if __name__ == '__main__':
    main()
