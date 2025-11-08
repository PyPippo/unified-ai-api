#!/usr/bin/env python3
"""
Advanced Usage Example - Comprehensive Feature Demonstration

This example demonstrates all advanced features of the Unified AI API package including:
- Interactive setup with full provider discovery
- Direct programmatic configuration
- Automated batch processing
- Enhanced error handling and recovery
- Multi-session management

To run: python examples/advanced_usage.py [1-4]
"""

import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from unified_ai_api.types import ApiSupportedContent
from unified_ai_api import APIConnectionManager


def example_interactive() -> None:
    """Example 1: Interactive setup with full provider discovery."""
    print('=== Example 1: Interactive Setup ===')

    api_manager = APIConnectionManager()

    if api_manager.interactive_setup():
        params = api_manager.get_connection_params()
        print(f'✅ Connection configured:')
        print(f'  Provider: {params["provider"]}')
        print(f'  Model: {params["model_name"]}')
        print(f'  API Type: {params["api_type"]}')
        print('Starting interactive chat...\n')
        api_manager.start_chat_loop()
    else:
        print('❌ Error configuring connection')


def example_programmatic() -> None:
    """Example 2: Programmatic configuration and automation."""
    print('=== Example 2: Programmatic Configuration ===')

    api_manager = APIConnectionManager()

    # Discover available providers
    providers = api_manager.get_available_providers()
    print(f'Available providers: {providers}')

    # Use first available provider programmatically
    if providers:
        provider = providers[0]
        print(f'Using provider: {provider}')

        # Get configurations for this provider
        configs = api_manager.get_provider_configs(provider)
        print(f'Available configs: {len(configs)}')

        if configs:
            # Display first config info
            first_config = configs[0]
            print(f'First config: {first_config.get("model_name", "Unknown")}')

            # Get supported APIs
            apis = api_manager.get_supported_api(provider, 0)
            print(f'Supported APIs: {apis}')

            # Setup connection with OpenAI-compatible API if available
            if 'openai' in apis:
                api_manager.configure_api(provider, 0, 'openai')

                if api_manager.validate_configuration():
                    print('✅ Connection setup successful')

                    # Create client and run automated session
                    with api_manager.create_chatclient(
                        session_id='auto_session'
                    ) as client:
                        # Automated Q&A session
                        qa_pairs = [
                            'What is artificial intelligence?',
                            'How does machine learning work?',
                            'What are the benefits of Python programming?',
                            'Explain the concept of neural networks.',
                            'What is the difference between AI and machine learning?',
                        ]

                        print('\n🤖 Starting automated Q&A session:')
                        successful_responses = 0

                        for i, question in enumerate(qa_pairs, 1):
                            print(f'\n📝 Question {i}: {question}')
                            answer = client.send_message(question)
                            if answer:
                                # Show first 200 characters of response
                                short_answer = (
                                    answer[:200] + '...'
                                    if len(answer) > 200
                                    else answer
                                )
                                print(f'🤖 Answer: {short_answer}')
                                successful_responses += 1
                            else:
                                print('❌ No response received')

                            # Show conversation statistics
                            print(
                                f'   💬 Conversation length: {len(client._chat_history)} messages'
                            )

                        print(f'\n📊 Session Statistics:')
                        print(f'  Questions asked: {len(qa_pairs)}')
                        print(f'  Successful responses: {successful_responses}')
                        print(
                            f'  Success rate: {(successful_responses/len(qa_pairs)*100):.1f}%'
                        )
                else:
                    print('❌ Configuration validation failed')
            else:
                print('⚠️  OpenAI-compatible API not available for this provider')


def example_multi_session() -> None:
    """Example 3: Multi-session management and parallel conversations."""
    print('=== Example 3: Multi-Session Management ===')

    api_manager = APIConnectionManager()

    try:
        # Configure connection
        providers = api_manager.get_available_providers()
        if not providers:
            print('❌ No providers available')
            return

        provider = providers[0]
        configs = api_manager.get_provider_configs(provider)
        apis = api_manager.get_supported_api(provider, 0)
        api_type = 'openai' if 'openai' in apis else apis[0]

        api_manager.configure_api(provider, 0, api_type)

        if not api_manager.validate_configuration():
            print('❌ Configuration validation failed')
            return

        print(f'✅ Configured with {provider} using {api_type}')

        # Create multiple chat sessions
        sessions = []
        session_topics = [
            ('science_chat', 'You are a science expert. Focus on scientific topics.'),
            ('coding_chat', 'You are a programming expert. Focus on coding questions.'),
            ('general_chat', 'You are a helpful general assistant.'),
        ]

        print('\n🔄 Creating multiple chat sessions...')

        for session_id, initial_prompt in session_topics:
            try:
                client = api_manager.create_chatclient(session_id=session_id)

                # Send initial prompt to set context
                client.send_message(initial_prompt)
                sessions.append((session_id, client))
                print(f'✅ Created session: {session_id}')

            except Exception as e:
                print(f'❌ Failed to create session {session_id}: {e}')

        # Test each session with appropriate questions
        test_questions = {
            'science_chat': 'Explain the theory of relativity',
            'coding_chat': 'Write a Python function to sort a list',
            'general_chat': 'What is the weather like today?',
        }

        print(f'\n💬 Testing {len(sessions)} parallel sessions...')

        for session_id, client in sessions:
            question = test_questions.get(session_id, 'Hello')
            print(f'\n📝 Session "{session_id}": {question}')

            try:
                response = client.send_message(question)
                if response:
                    display_response = (
                        response[:150] + '...' if len(response) > 150 else response
                    )
                    print(f'🤖 Response: {display_response}')
                else:
                    print('❌ No response')
            except Exception as e:
                print(f'❌ Error: {e}')

        # Clean up all sessions
        print(f'\n🧹 Cleaning up {len(sessions)} sessions...')
        for session_id, client in sessions:
            client.close()

        api_manager.close_all_clients()
        print('✅ All sessions closed successfully')

    except Exception as e:
        print(f'❌ Multi-session example failed: {e}')


def example_error_handling():
    """Example 4: Comprehensive error handling and recovery."""
    print('=== Example 4: Error Handling & Recovery ===')

    api_manager = APIConnectionManager()

    # Test 1: Access without configuration
    print('🧪 Test 1: Accessing connection without setup')
    try:
        if not api_manager.validate_configuration():
            print('✅ Correctly detected missing configuration')
        else:
            print('❌ Should have detected missing configuration')
    except Exception as e:
        print(f'❌ Unexpected error: {e}')

    # Test 2: Invalid provider configuration
    print('\n🧪 Test 2: Invalid provider configuration')
    try:
        # This should fail gracefully
        api_manager.configure_api('NONEXISTENT_PROVIDER', 0, 'openai')
        print('❌ Should have failed with invalid provider')
    except Exception as e:
        print(f'✅ Correctly caught error: {type(e).__name__}')

    # Test 3: Invalid config index
    print('\n🧪 Test 3: Invalid configuration index')
    try:
        providers = api_manager.get_available_providers()
        if providers:
            api_manager.configure_api(providers[0], 999, 'openai')  # Invalid index
            print('❌ Should have failed with invalid config index')
    except Exception as e:
        print(f'✅ Correctly caught error: {type(e).__name__}')

    # Test 4: API client creation without configuration
    print('\n🧪 Test 4: Client creation without configuration')
    try:
        fresh_manager = APIConnectionManager()
        client = fresh_manager.create_chatclient()
        print('❌ Should have failed without configuration')
    except Exception as e:
        print(f'✅ Correctly caught error: {type(e).__name__}')

    # Test 5: Recovery and successful operation
    print('\n🧪 Test 5: Recovery and successful operation')
    try:
        recovery_manager = APIConnectionManager()
        providers = recovery_manager.get_available_providers()

        if providers:
            provider = providers[0]
            configs = recovery_manager.get_provider_configs(provider)
            apis = recovery_manager.get_supported_api(provider, 0)

            if apis:
                api_type = apis[0]
                recovery_manager.configure_api(provider, 0, api_type)

                if recovery_manager.validate_configuration():
                    print('✅ Successfully recovered and configured')

                    # Test a simple operation
                    with recovery_manager.create_chatclient() as client:
                        if client.get_connection_status():
                            print('✅ Client created and connected successfully')
                        else:
                            print('⚠️  Client created but not connected')
                else:
                    print('❌ Configuration validation failed during recovery')

    except Exception as e:
        print(f'❌ Recovery failed: {e}')

    print('\n📊 Error handling tests completed')


def show_menu():
    """Display the example menu."""
    print('🤖 Unified AI API - Advanced Examples')
    print('=' * 45)
    print('1. Interactive setup and chat')
    print('2. Programmatic configuration and automation')
    print('3. Multi-session management')
    print('4. Error handling demonstration')
    print('\nUsage:')
    print('  python examples/advanced_usage.py [1-4]')
    print('  or just run: python examples/advanced_usage.py')
    print('\nFeatures showcased:')
    print('- ✅ Comprehensive error handling')
    print('- ✅ Multi-provider support')
    print('- ✅ Session management')
    print('- ✅ Automated workflows')
    print('- ✅ Type-safe configuration')


if __name__ == '__main__':
    examples = {
        '1': example_interactive,
        '2': example_programmatic,
        '3': example_multi_session,
        '4': example_error_handling,
    }

    if len(sys.argv) > 1 and sys.argv[1] in examples:
        # Run specific example
        examples[sys.argv[1]]()
    else:
        # Show menu and run default example
        show_menu()
        print('\nRunning programmatic configuration example by default...\n')
        example_programmatic()
