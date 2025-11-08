"""Unified API connection management for multiple AI providers.

This module provides the core classes for managing connections to various AI API providers
through a unified interface. It implements the factory pattern with secure instantiation
controls and comprehensive error handling.

Classes:
    _ChatClientToken: Private token for secure ChatClient instantiation
    ChatClient: Individual chat session with conversation management
    APIConnectionManager: Main interface for provider configuration and client creation

Exceptions:
    All methods may raise APIClientError, InvalidParameterError, UnsupportedAPITypeError,
    or ResponseConversionError from the compatible_client_api module.

Usage:
    Basic setup:
        manager = APIConnectionManager()
        manager.configure_api('OPENAI', 0, 'openai')
        client = manager.create_chatclient()
        response = client.send_message("Hello!")

    Interactive setup:
        manager = APIConnectionManager()
        if manager.interactive_setup():
            manager.start_chat_loop()
"""

import secrets
from typing import Any

from .types import (
    ApiSupportedContent,
    ApiSupported,
    ProviderName,
    ProviderAttributes,
    ProvidersConfigParams,
    ProvidersConfigList,
    UrlType,
    ChatMessage,
    ChatCompletionResponse,
)
from .types.providers_types import is_valid_provider_name
from .compatible_client_api import (
    CompatibleClient,
    APIClientError,
    InvalidParameterError,
    UnsupportedAPITypeError,
    ResponseConversionError,
)
from .providers_config_handlers import ProvidersConfigHandler
from .auth_keys import get_secret_api_key


class _ChatClientToken:
    """Private security token to control ChatClient instantiation.

    This token ensures that ChatClient instances can only be created through
    the APIConnectionManager factory method, preventing direct instantiation
    and maintaining proper initialization flow.

    Attributes:
        _token (str): Cryptographically secure random token
    """

    def __init__(self) -> None:
        """Initialize a new security token."""
        self._token = secrets.token_hex(16)


class ChatClient:
    """Individual chat session client with conversation management.

    This class provides a secure, session-based interface for conducting
    conversations with AI providers. It maintains chat history, handles
    message formatting, and provides context management.

    Security:
        Can only be instantiated through APIConnectionManager.create_chatclient()
        to ensure proper configuration and resource management.

    Features:
        - Automatic chat history management
        - Message formatting and validation
        - Context manager support for resource cleanup
        - Configurable timeouts and error handling

    Attributes:
        compatible_client (CompatibleClient): Underlying API client

    Usage:
        # Through APIConnectionManager (recommended)
        manager = APIConnectionManager()
        manager.configure_api('OPENAI', 0, 'openai')
        with manager.create_chatclient() as client:
            response = client.send_message("Hello!")
            print(response)
    """

    def __init__(
        self,
        token: _ChatClientToken,
        session_id: str,
        connection_params: dict[str, Any],
        secret_api_key: str,
    ) -> None:
        """Initialize a ChatClient instance.

        Args:
            token: Security token from APIConnectionManager
            session_id: Unique identifier for this chat session
            connection_params: Configuration parameters for the connection
            secret_api_key: API authentication key

        Raises:
            RuntimeError: If not called through APIConnectionManager
            InvalidParameterError: If any parameters are invalid or missing
            APIClientError: If client initialization fails
        """
        # check if called from factory
        if not isinstance(token, _ChatClientToken):
            raise RuntimeError(
                "ChatClient can only be instantiated through APIConnectionManager.create_chatclient()"
            )

        # Validate inputs with proper exception types
        if not connection_params:
            raise InvalidParameterError("Connection parameters cannot be empty")
        if not secret_api_key or not secret_api_key.strip():
            raise InvalidParameterError("Secret API key must be provided and non-empty")
        if not session_id or not session_id.strip():
            raise InvalidParameterError("Session ID must be provided and non-empty")

        # Validate required connection parameters
        required_params = ['api_type', 'endpoint_url', 'model_name', 'init_config_msg']
        missing_params = [
            param for param in required_params if param not in connection_params
        ]
        if missing_params:
            raise InvalidParameterError(
                f"Missing required connection parameters: {missing_params}"
            )

        # Validate parameter values are not empty
        empty_params = [
            param
            for param in required_params
            if not connection_params[param] or not str(connection_params[param]).strip()
        ]
        if empty_params:
            raise InvalidParameterError(
                f"Empty values for required parameters: {empty_params}"
            )

        # Initialize attributes
        self._token = token
        self._session_id = session_id
        self._is_closed = False
        self._secret_api_key: str = secret_api_key
        self._connection_params: dict[str, Any] = connection_params
        self._chat_history: list[ChatMessage] = []

        # Try to initialize CompatibleClient with proper error handling
        try:
            self.compatible_client = CompatibleClient(
                api_type=self._connection_params['api_type'],
                base_url=self._connection_params['endpoint_url'],
                model_name=self._connection_params['model_name'],
                api_key=self._secret_api_key,
            )

            # Configure default timeouts (per project memory: 30s connection, 60s read)
            try:
                self.compatible_client.configure_rest_timeouts(
                    connect_timeout=30.0, read_timeout=60.0
                )
            except Exception:
                # Timeout configuration is optional - don't fail if it doesn't work
                pass
        except (InvalidParameterError, UnsupportedAPITypeError) as e:
            # Re-raise client-specific errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise APIClientError(f"Failed to initialize API client: {e}") from e

    def _create_message_user(self, message: str) -> ChatMessage:
        """Create a user message object from text.

        Args:
            message: Text content for the user message

        Returns:
            ChatMessage: Formatted user message object
        """
        # Create user message
        user_message: ChatMessage = ChatMessage.create_message(
            role='user', content=message
        )

        return user_message

    def _create_message_assistant(self, message: str) -> ChatMessage:
        """Create an assistant message object from text.

        Args:
            message: Text content for the assistant message

        Returns:
            ChatMessage: Formatted assistant message object
        """
        # Create assistant message
        assistant_message: ChatMessage = ChatMessage.create_message(
            role='assistant', content=message
        )

        return assistant_message

    def send_message(self, message: str) -> str | None:
        """Send a message to the AI and get a response.

        This method handles the complete conversation flow: validates input,
        adds the message to chat history, sends it to the AI provider,
        processes the response, and updates the conversation history.

        Args:
            message: The message to send (must be non-empty)

        Returns:
            str | None: The AI response content, or None if an error occurred.
                       None indicates a recoverable error; exceptions indicate
                       configuration or validation issues.

        Raises:
            InvalidParameterError: If message is empty or None
            APIClientError: If no client connection is established

        Note:
            API errors (network issues, rate limits, etc.) return None rather
            than raising exceptions to allow graceful error handling in chat loops.
        """
        # Validate input
        if not message or not message.strip():
            raise InvalidParameterError("Message cannot be empty or None")

        # Check if client is available
        if self.compatible_client is None:
            raise APIClientError('API connection not established')

        try:
            # Create user message
            user_message: ChatMessage = self._create_message_user(message=message)
            # Add to chat history
            self._chat_history.append(user_message)

            # Get response from API
            response: ChatCompletionResponse = self.compatible_client.chat_completion(
                self._chat_history
            )
            response_content = response.get_content()

            # Add assistant response to history (if we want to maintain conversation)
            if response_content:
                assistant_message: ChatMessage = ChatMessage.create_message(
                    role='assistant', content=response_content
                )
                self._chat_history.append(assistant_message)

            return response_content

        except (
            APIClientError,
            InvalidParameterError,
            UnsupportedAPITypeError,
            ResponseConversionError,
        ) as e:
            # Log API-specific errors but don't re-raise, return None to indicate failure
            print(f'API error sending message: {e}')
            return None
        except Exception as e:
            # Log unexpected errors
            print(f'Unexpected error sending message: {e}')
            return None

    def clear_chat_history(self) -> None:
        """Clear conversation history and reset to initial state.

        Removes all previous messages and reinitializes the chat history
        with the configured initial message. This effectively starts
        a fresh conversation while maintaining the same connection.

        Raises:
            APIClientError: If no client connection is established or
                           if required configuration is missing
        """
        if self.compatible_client is None:
            raise APIClientError('No API connection established')

        try:
            init_config_text_msg: str = self._connection_params['init_config_msg']
            if not init_config_text_msg:
                # Use a default message if none configured
                init_config_text_msg = "You are a helpful AI assistant."

            init_config_chat_msg: ChatMessage = self._create_message_user(
                init_config_text_msg
            )
            self._chat_history = [init_config_chat_msg]

        except KeyError as e:
            raise APIClientError(f"Missing configuration parameter: {e}") from e
        except Exception as e:
            raise APIClientError(f"Failed to clear chat history: {e}") from e

    def get_connection_status(self) -> bool:
        """Check if the client has an active connection.

        Returns:
            bool: True if connected and ready for messaging, False otherwise
        """
        return self.compatible_client is not None

    def get_model_name(self) -> str:
        """Get model name.

        Returns:
            str: The configured model name

        Raises:
            APIClientError: If no client connection is established
        """
        if self.compatible_client is None:
            raise APIClientError(
                'No API connection established. Use APIConnectionManager.create_chatclient() first.'
            )
        return self._connection_params['model_name']

    def get_connection_params(self) -> dict[str, Any]:
        """Get connection parameters.

        Returns:
            dict: Copy of connection parameters

        Raises:
            APIClientError: If no client connection is established
        """
        if self.compatible_client is None:
            raise APIClientError(
                'No API connection established. Use APIConnectionManager.create_chatclient() first.'
            )
        return (
            self._connection_params.copy()
        )  # Return copy to prevent external modification

    # close connection Context Manager
    def close(self) -> None:
        """Close the chat client and clean up resources.

        Closes the underlying API client connection, clears chat history
        from memory, and marks the client as closed. Safe to call multiple times.

        Note:
            After calling close(), the client cannot be reused. Create a new
            client through APIConnectionManager if needed.
        """
        if not self._is_closed:
            if self.compatible_client:
                self.compatible_client.close()  # Call compatible client's cleanup
            self._chat_history.clear()  # Clear memory
            print(f"Closing ChatClient session: {self._session_id}")
            self._is_closed = True

    def __enter__(self) -> 'ChatClient':
        """Enter context manager.

        Returns:
            ChatClient: Self for use in with statements
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and clean up resources.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.close()


class APIConnectionManager:
    """Unified API connection manager for multiple AI providers.

    This is the main entry point for the API connection system. It provides
    a builder-pattern interface for configuring connections and creating
    chat clients. Supports both programmatic and interactive setup.

    Features:
        - Multi-provider support (OpenAI, HuggingFace, OpenRouter, etc.)
        - Configuration validation and error handling
        - Session management and resource cleanup
        - Interactive setup wizard
        - Builder pattern for fluent configuration

    Workflow:
        1. Create manager instance
        2. Configure API connection (programmatic or interactive)
        3. Create chat clients as needed
        4. Use clients for conversations
        5. Clean up resources when done

    Usage Examples:
        Programmatic setup:
            manager = APIConnectionManager()
            manager.configure_api('OPENAI', 0, 'openai')
            client = manager.create_chatclient()
            response = client.send_message("Hello!")
            client.close()

        Interactive setup:
            manager = APIConnectionManager()
            if manager.interactive_setup():
                manager.start_chat_loop()  # Interactive chat session

        Builder pattern:
            client = (APIConnectionManager()
                     .configure_api('OPENAI', 0, 'openai')
                     .create_chatclient())
    """

    def __init__(self) -> None:
        """Initialize a new API connection manager.

        Creates an empty manager ready for configuration. No connections
        are established until configure_api() is called.
        """
        self._active_clients: list['ChatClient'] = []
        self._connection_params: dict = {}

    def configure_api(
        self, provider: ProviderName, config_index: int, api_type: ApiSupportedContent
    ) -> 'APIConnectionManager':
        """Configure API connection parameters using builder pattern.

        Validates the provider configuration, loads settings from providers.json,
        retrieves the API key, and prepares the manager for client creation.

        Args:
            provider: Provider name (e.g., 'OPENAI', 'HUGGINGFACE')
            config_index: Configuration index (must be >= 0)
            api_type: API type to use (e.g., 'openai', 'huggingface')

        Returns:
            APIConnectionManager: Self for method chaining

        Raises:
            InvalidParameterError: If parameters are invalid, provider not found,
                                   config index out of range, or API type not supported
            APIClientError: If configuration loading fails or API key not found

        Example:
            manager.configure_api('OPENAI', 0, 'openai')
        """
        # Validate provider name using runtime checking (per specification)
        if not is_valid_provider_name(provider):
            available = ProvidersConfigHandler.available_providers()
            raise InvalidParameterError(
                f"Invalid provider '{provider}'. Available: {available}"
            )

        # Validate config_index
        if config_index < 0:
            raise InvalidParameterError(
                f"Config index must be >= 0, got: {config_index}"
            )

        try:
            # Validate that the config exists and get configuration data
            provider_configs = ProvidersConfigHandler.available_provider_configs(
                provider
            )
            if config_index >= len(provider_configs):
                raise InvalidParameterError(
                    f"Config index {config_index} out of range for provider '{provider}' "
                    f"(max: {len(provider_configs) - 1})"
                )

            # Validate API type is supported
            supported_apis = ProvidersConfigHandler.get_provider_api_supported(
                provider, config_index
            )
            if api_type not in supported_apis:
                raise InvalidParameterError(
                    f"API type '{api_type}' not supported by provider '{provider}' config {config_index}. "
                    f"Supported: {supported_apis}"
                )

            # Get configuration parameters
            self._connection_params.update(
                {
                    'provider': provider,
                    'config_index': config_index,
                    'api_type': api_type,
                    'endpoint_url': ProvidersConfigHandler.get_provider_endpoint(
                        provider, api_type, config_index
                    ),
                    'model_name': ProvidersConfigHandler.get_provider_config_attribute(
                        provider, 'model_name', config_index
                    ),
                    'init_config_msg': ProvidersConfigHandler.get_provider_config_attribute(
                        provider, 'init_config_msg', config_index
                    ),
                }
            )

            # Get secret API key
            self._secret_api_key = get_secret_api_key(
                provider, config_index=config_index
            )

            # Validate that we got a non-empty API key
            if not self._secret_api_key or not self._secret_api_key.strip():
                raise InvalidParameterError(
                    f"No valid API key found for provider '{provider}' config {config_index}. "
                    "Check your environment variables or secrets configuration."
                )

            return self  # Enable method chaining

        except (InvalidParameterError, APIClientError):
            # Re-raise our own exceptions
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise APIClientError(
                f"Failed to configure API for provider '{provider}': {e}"
            ) from e

    def validate_configuration(self) -> bool:
        """Check if the manager has a complete, valid configuration.

        Verifies that all required parameters are present and that the
        API key has been successfully retrieved.

        Returns:
            bool: True if configuration is complete and valid, False otherwise
        """
        required = [
            'provider',
            'config_index',
            'api_type',
            'endpoint_url',
            'model_name',
            'init_config_msg',
        ]
        return all(param in self._connection_params for param in required) and hasattr(
            self, '_secret_api_key'
        )

    def get_connection_params(self) -> dict[str, Any]:
        """Get information about the configured connection.

        Returns:
            dict[str, Any]: Dictionary containing connection parameters
        """
        return {
            'provider': self._connection_params.get('provider', ''),
            'config_index': self._connection_params.get('config_index', ''),
            'api_type': self._connection_params.get('api_type', ''),
            'endpoint_url': self._connection_params.get('endpoint_url', ''),
            'model_name': self._connection_params.get('model_name', ''),
            'init_config_msg': self._connection_params.get('init_config_msg', ''),
        }

    def create_chatclient(self, session_id: str | None = None) -> ChatClient:
        """Create a new ChatClient instance (factory method).

        This is the only way to create ChatClient instances. The factory
        pattern ensures proper initialization and security.

        Args:
            session_id: Optional session identifier. If None, auto-generated
                       based on the number of active clients.

        Returns:
            ChatClient: Configured and ready-to-use chat client instance

        Raises:
            InvalidParameterError: If configuration is incomplete or session_id is empty
            APIClientError: If client creation fails due to initialization errors

        Note:
            The manager tracks all created clients for resource management.
            Use close_all_clients() to clean up all active sessions.
        """
        if not self.validate_configuration():
            missing_config = []
            required = [
                'provider',
                'config_index',
                'api_type',
                'endpoint_url',
                'model_name',
                'init_config_msg',
            ]
            for param in required:
                if param not in self._connection_params:
                    missing_config.append(param)
            if not hasattr(self, '_secret_api_key'):
                missing_config.append('secret_api_key')

            raise InvalidParameterError(
                f"Configuration incomplete. Missing: {missing_config}. "
                "Use configure_api() method first."
            )

        try:
            # Generate session ID if not provided
            if session_id is None:
                session_id = f'session_{len(self._active_clients)}'
            elif not session_id.strip():
                raise InvalidParameterError("Session ID cannot be empty")

            # Create authorization token
            token = _ChatClientToken()

            # Create the client (this will validate parameters and create CompatibleClient)
            client = ChatClient(
                token=token,
                connection_params=self._connection_params.copy(),
                session_id=session_id,
                secret_api_key=self._secret_api_key,
            )

            # Track active clients for cleanup
            self._active_clients.append(client)
            return client

        except (InvalidParameterError, APIClientError, UnsupportedAPITypeError):
            # Re-raise specific API errors
            raise
        except Exception as e:
            # Wrap unexpected errors with context
            raise APIClientError(
                f"Failed to create ChatClient for provider '{self._connection_params.get('provider', 'unknown')}': {e}"
            ) from e

    def close_all_clients(self) -> None:
        """Close and cleanup all active chat clients.

        Calls close() on all clients created by this manager and clears
        the internal tracking list. Safe to call multiple times.
        """
        for client in self._active_clients:
            client.close()
        self._active_clients.clear()

    # Provider configuration helpers - delegate to ProvidersConfigHandler
    def get_available_providers(self) -> list[ProviderName]:
        """Get list of all available AI providers.

        Returns:
            list[ProviderName]: Names of all configured providers from providers.json
        """
        return ProvidersConfigHandler.available_providers()

    def get_provider_configs(self, provider: ProviderName) -> ProvidersConfigList:
        """Get available configurations for a specific provider.

        Args:
            provider: Provider name to query

        Returns:
            ProvidersConfigList: List of configuration dictionaries for the provider

        Raises:
            ValueError: If provider is not found in providers.json
        """
        return ProvidersConfigHandler.available_provider_configs(provider)

    def get_supported_api(
        self, provider: ProviderName, config_index: int
    ) -> ApiSupported:
        """Get supported API types for a provider configuration.

        Args:
            provider: Provider name
            config_index: Configuration index within the provider

        Returns:
            ApiSupported: List of supported API type strings

        Raises:
            ValueError: If provider not found or config_index out of range
        """
        return ProvidersConfigHandler.get_provider_api_supported(
            provider=provider,
            config_index=config_index,
        )

    # Interactive setup and chat methods
    def interactive_setup(self) -> bool:
        """Interactive setup wizard for configuring API connection.

        Guides the user through selecting a provider, configuration, and API type
        using console prompts. Automatically configures the manager based on
        user selections.

        Workflow:
            1. Display available providers
            2. User selects provider
            3. Display configurations for selected provider
            4. User selects configuration
            5. Display supported APIs for selected config
            6. User selects API type
            7. Configure manager with selections

        Returns:
            bool: True if configuration was successful, False if cancelled or failed

        Note:
            This method blocks for user input. Use Ctrl+C to cancel.
        """
        # Get available providers
        providers_list = self.get_available_providers()
        print('\nAvailable providers:')
        for i, provider in enumerate(providers_list):
            print(f'{i}: {provider}')

        try:
            # Get provider choice
            choice = int(input('Choose a provider: '))
            if choice not in range(len(providers_list)):
                print(f'Provider not found: {choice}')
                return False

            provider_chosen: ProviderName = providers_list[choice]
            print(f'Provider chosen: {provider_chosen}\n')

            # Get available configurations
            config_list: ProvidersConfigList = self.get_provider_configs(
                provider_chosen
            )

            print(f'Available configurations for {provider_chosen}:')
            for i, config in enumerate(config_list):
                print(f'{i}: {config['model_name']} - {config['model_url']}')

            choice = int(input('Choose a configuration: '))
            if choice not in range(len(config_list)):
                print(f'Configuration not found: {choice}')
                return False

            config_index_chosen: int = choice
            config_chosen: ProvidersConfigParams = config_list[choice]
            print(
                f'Configuration chosen: {config_chosen['model_name']} - {config_chosen['model_url']}\n'
            )

            # Get supported APIs
            api_list: ApiSupported = self.get_supported_api(
                provider=provider_chosen, config_index=config_index_chosen
            )

            print(f'Supported APIs for {config_chosen['model_name']}:')
            for i, api in enumerate(api_list):
                print(f'{i}: {api}')

            choice = int(input('Choose an API: '))
            if choice not in range(len(api_list)):
                print(f'API not found: {choice}')
                return False

            api_chosen: ApiSupportedContent = api_list[choice]
            print(f'API chosen: {api_chosen}\n')

            # Setup connection using the builder pattern
            self.configure_api(
                provider=provider_chosen,
                config_index=config_index_chosen,
                api_type=api_chosen,
            )
            return self.validate_configuration()

        except (ValueError, KeyboardInterrupt) as e:
            print(f'Error during configuration: {e}')
            return False

    def start_chat_loop(self) -> None:
        """Start an interactive chat session in the terminal.

        Creates a chat client and enters a loop where users can type messages
        and receive AI responses. The loop continues until the user presses Ctrl+C.

        Features:
            - Real-time conversation with the configured AI
            - Automatic client cleanup on exit
            - Graceful handling of Ctrl+C interruption
            - Error reporting for failed responses

        Raises:
            InvalidParameterError: If manager is not properly configured
            APIClientError: If chat client creation or startup fails

        Note:
            Must call configure_api() or interactive_setup() first.
            The chat client is automatically cleaned up when exiting.
        """
        if not self.validate_configuration():
            raise InvalidParameterError(
                'No connection configured. Call configure_api() or interactive_setup() first.'
            )

        try:
            chat_client = self.create_chatclient()
            print(
                f'\nChat started with {self.get_connection_params()['provider']} - {chat_client.get_model_name()}'
            )
            print('Press Ctrl+C to exit\n')

            try:
                while True:
                    user_input = input('You: ')
                    if user_input.strip():
                        response = chat_client.send_message(user_input)
                        if response:
                            print(f'AI: {response}\n')
                        else:
                            print('Error getting response\n')
            except KeyboardInterrupt:
                print('\nGoodbye!\n')
            finally:
                # Clean up the chat client
                chat_client.close()

        except Exception as e:
            raise APIClientError(f"Failed to start chat loop: {e}") from e
