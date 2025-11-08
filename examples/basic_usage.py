#!/usr/bin/env python3
"""
Basic Usage Example - Simple Interactive Chat Interface

This example provides a clean, simple entry point to start using the
APIConnectionManager with interactive setup and chat functionality.

Features demonstrated:
- Interactive provider and configuration selection
- Automatic API key detection
- Simple chat loop with error handling
- User-friendly console interface

To run: python examples/basic_usage.py
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from unified_ai_api.api_connection import APIConnectionManager


def main() -> None:
    """Simple interactive chat interface using APIConnectionManager."""
    print('🤖 Unified AI API Connection - Basic Usage')
    print('=' * 50)
    print(
        'Welcome! This will guide you through setting up and using your AI connection.\n'
    )

    try:
        # Initialize the API connection manager
        api_manager = APIConnectionManager()

        # Get available providers to check configuration
        available_providers = api_manager.get_available_providers()

        if not available_providers:
            print('❌ No providers found in configuration.')
            print(
                'Please check that src/unified_ai_api/config/providers.json exists and is properly configured.'
            )
            return

        print('Setting up your AI connection...\n')

        # Interactive setup
        if api_manager.interactive_setup():
            print(f'\n✅ Connected successfully!')
            connection_info = api_manager.get_connection_params()
            print(f'Provider: {connection_info.get("provider", "Unknown")}')
            print(f'Model: {connection_info.get("model_name", "Unknown")}')
            print(f'API Type: {connection_info.get("api_type", "Unknown")}')
            print('\n🚀 Starting chat session...')
            print('💡 Tip: Press Ctrl+C to exit\n')

            # Start the chat loop
            api_manager.start_chat_loop()

        else:
            print('❌ Failed to set up connection.')
            print('\n🔧 Troubleshooting:')
            print('1. Make sure you have API keys configured')
            print(
                '2. Copy: src/unified_ai_api/config/secret.json.template → secret.json'
            )
            print('3. Edit secret.json with your actual API keys')
            print('4. Or set environment variables (e.g., OPENROUTER_API_KEY=your-key)')
            print('\n📚 For more examples and advanced usage:')
            print('   python examples/advanced_usage.py')

    except Exception as e:
        print(f'❌ Error during initialization: {e}')
        print('\n🔧 Common solutions:')
        print(
            '1. Check that all configuration files exist in src/unified_ai_api/config/'
        )
        print('2. Verify your API keys are properly configured')
        print(
            '3. Make sure dependencies are installed: pip install -r requirements.txt'
        )
        print('\n📚 For detailed setup instructions, see: docs/installation.md')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n✅ Thanks for using Unified AI API! Goodbye!')
