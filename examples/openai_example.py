#!/usr/bin/env python3
"""
OpenAI Example - Direct OpenAI-compatible API Usage

This example demonstrates how to use the package specifically with
OpenAI-compatible providers like OpenRouter, direct OpenAI API, or
other compatible services.

Features demonstrated:
- Direct configuration without interactive setup
- OpenAI-compatible API usage
- Conversation management
- Error handling for API calls

To run: python examples/openai_example.py
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from unified_ai_api import APIConnectionManager


def main() -> None:
    """Demonstrate OpenAI-compatible API usage."""
    print('🤖 Unified AI API - OpenAI Example')
    print('=' * 40)

    # Initialize manager
    manager = APIConnectionManager()

    try:
        # Configure for OpenAI-compatible API (using OpenRouter as example)
        print('Configuring OpenAI-compatible connection...')
        manager.configure_api(
            provider='OPENROUTER',  # or 'OPENAI' if you have OpenAI keys
            config_index=0,
            api_type='openai',
        )

        # Validate configuration
        if not manager.validate_configuration():
            print('❌ Configuration validation failed.')
            print('Please check your API keys and provider configuration.')
            return

        print('✅ Configuration validated!')

        # Create a chat client
        print('Creating chat client...')
        with manager.create_chatclient(session_id='openai_example') as client:
            print(f'Connected to: {client.get_model_name()}')
            print(
                'Status:',
                '🟢 Connected' if client.get_connection_status() else '🔴 Disconnected',
            )

            # Example conversation
            test_messages = [
                "Hello! Can you introduce yourself?",
                "What are the main features of Python programming?",
                "Explain the difference between lists and tuples in Python.",
            ]

            print('\n🚀 Starting conversation...\n')

            for i, message in enumerate(test_messages, 1):
                print(f'👤 User ({i}): {message}')

                response = client.send_message(message)
                if response:
                    # Truncate long responses for display
                    display_response = (
                        response[:300] + '...' if len(response) > 300 else response
                    )
                    print(f'🤖 AI ({i}): {display_response}')
                else:
                    print(f'🤖 AI ({i}): ❌ No response received')

                print()  # Empty line for readability

            # Demonstrate chat history management
            print('📋 Chat History Management:')
            print(
                'Current conversation length: {} messages'.format(
                    len(client._chat_history)
                )
            )

            # Clear history and start fresh
            print('Clearing chat history...')
            client.clear_chat_history()
            print(
                'History cleared. New conversation length: {} messages'.format(
                    len(client._chat_history)
                )
            )

            # Send one more message to demonstrate fresh start
            final_message = (
                "This is a fresh conversation. Do you remember our previous discussion?"
            )
            print(f'\n👤 User (fresh): {final_message}')

            response = client.send_message(final_message)
            if response:
                display_response = (
                    response[:200] + '...' if len(response) > 200 else response
                )
                print(f'🤖 AI (fresh): {display_response}')

        print('\n✅ Example completed successfully!')
        print('💡 The chat client was automatically closed using context manager.')

    except Exception as e:
        print(f'❌ Error: {e}')
        print('\n🔧 Troubleshooting:')
        print('1. Ensure OPENROUTER_API_KEY environment variable is set')
        print('2. Or configure src/unified_ai_api/config/secret.json')
        print('3. Check that providers.json contains OPENROUTER configuration')
        print('4. Verify your API key has sufficient permissions')


if __name__ == '__main__':
    main()
