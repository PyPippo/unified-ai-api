"""Compatible API client module for unified AI API connections.

This module provides a unified interface for connecting to various AI API providers
through a common abstraction layer. It includes base classes, a dispatcher system,
and concrete implementations for different API types.

Classes:
    BaseAPIClient: Abstract base class defining the API client interface
    CompatibleClientDispatcher: Registry and factory for API client implementations
    CompatibleClient: Factory proxy for creating API clients
    OpenAICompatibleClient: Implementation for OpenAI-compatible APIs
    RestAPICompatibleClient: Implementation for generic REST APIs

Exceptions:
    APIClientError: Base exception for API client errors
    UnsupportedAPITypeError: Raised when an unsupported API type is requested
    InvalidParameterError: Raised when invalid parameters are provided
    ResponseConversionError: Raised when response conversion or parsing fails
"""

from .types.api_types import ApiSupported, EndPointUrl
from .types import (
    ApiSupportedContent,
    ProviderName,
    UrlType,
    ApiEndpoints,
    ChatMessage,
    ChatCompletionResponse,
)
from typing import Callable, Self
from abc import ABC, abstractmethod
from typing_extensions import override


class APIClientError(Exception):
    """Base exception for API client errors."""

    pass


class UnsupportedAPITypeError(APIClientError):
    """Raised when an unsupported API type is requested."""

    pass


class InvalidParameterError(APIClientError):
    """Raised when invalid parameters are provided."""

    pass


class ResponseConversionError(APIClientError):
    """Raised when response conversion or parsing fails."""

    pass


class BaseAPIClient(ABC):
    """Abstract base class for all API client implementations.

    This class defines the required interface that all API client implementations
    must follow. It ensures consistent initialization parameters and method
    signatures across different API providers.

    All subclasses must implement the initialization with the same parameters
    (base_url, api_key, model_name) and provide both chat completion and model
    name retrieval functionality. The base class provides parameter validation
    and a default no-op cleanup method.

    Key Features:
        - Consistent interface across all API providers
        - Built-in parameter validation
        - Resource cleanup support
        - Type safety with abstract method enforcement
    """

    @abstractmethod
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        """Initialize the API client with required parameters.

        Args:
            base_url: The base URL for the API endpoint (must be non-empty)
            api_key: Authentication key for the API (must be non-empty)
            model_name: Name of the model to use for requests (must be non-empty)

        Raises:
            InvalidParameterError: If any parameter is empty or None
        """
        # All implementations should validate parameters
        if not base_url or not base_url.strip():
            raise InvalidParameterError("base_url must be provided and non-empty")
        if not api_key or not api_key.strip():
            raise InvalidParameterError("api_key must be provided and non-empty")
        if not model_name or not model_name.strip():
            raise InvalidParameterError("model_name must be provided and non-empty")

    @abstractmethod
    def chat_completion(self, messages: list[ChatMessage]) -> ChatCompletionResponse:
        """Send chat completion request and return response.

        Args:
            messages: List of chat messages to send to the API

        Returns:
            ChatCompletionResponse: The API response containing generated content

        Raises:
            Exception: If the API request fails or returns an error
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name being used by this client.

        Returns:
            str: The name of the model configured for this client
        """
        pass

    def close(self) -> None:
        """Cleanup resources. Default implementation does nothing."""
        pass  # Default: no cleanup needed, Fallback to no-op


class CompatibleClientDispatcher:
    """Registry and factory for API client implementations.

    This class maintains a registry of available API client implementations
    and provides a factory method to instantiate the appropriate client
    based on the API type.

    Usage:
        dispatcher = CompatibleClientDispatcher()
        client = dispatcher('openai', 'https://api.openai.com/v1', 'key', 'gpt-4')

    Key attributes:
        _registry: Class-level dictionary mapping API types to client classes
    """

    # Class-level registry to store handlers
    _registry = {}

    def __init__(self) -> None:
        """Initialize dispatcher with access to the class registry."""
        # Instance uses the class registry
        self.registry = self._registry

    @classmethod
    def register(cls, api_key: ApiSupportedContent) -> Callable:
        """Register a new API client implementation.

        This decorator registers a client class for a specific API type.

        Args:
            api_key: The API type identifier to register

        Returns:
            Callable: Decorator function for the client class
        """

        def wrapper(new_cls):
            cls._registry[api_key] = new_cls
            return new_cls

        return wrapper

    def __call__(
        self, key: ApiSupportedContent, base_url: str, api_key: str, model_name: str
    ):
        """Create an instance of the appropriate API client.

        Args:
            key: The API type to create a client for
            base_url: The base URL for the API endpoint
            api_key: Authentication key for the API
            model_name: Name of the model to use

        Returns:
            BaseAPIClient: An instance of the appropriate API client

        Raises:
            UnsupportedAPITypeError: If no handler is registered for the given API type
        """
        if key in self.registry:
            handler_class = self.registry[key]
            # Instantiate the class with the provided parameters
            return handler_class(base_url, api_key, model_name)
        else:
            raise UnsupportedAPITypeError(f"No handler for: {key}")


class CompatibleClient:
    """Factory proxy for creating and managing API clients.

    This class acts as a high-level factory that simplifies client creation
    by handling the dispatcher internally. It provides a clean interface
    for users who want to work with different API types without managing
    the registration system directly.

    The class supports both context manager usage for automatic resource cleanup
    and manual resource management patterns.

    Usage:
        # Basic usage
        client = CompatibleClient('openai', 'https://api.openai.com/v1', 'key', 'gpt-4')
        response = client.chat_completion(messages)

        # Context manager usage (recommended)
        with CompatibleClient('openai', url, key, model) as client:
            response = client.chat_completion(messages)
            response2 = client.chat_completion(more_messages)

        # Manual cleanup
        client = CompatibleClient('openai', url, key, model)
        try:
            response = client.chat_completion(messages)
        finally:
            client.close()  # Manual cleanup

    Key attributes:
        api_type: The type of API being used
        base_url: The API endpoint URL
        api_key: Authentication key for the API
        model_name: Name of the model to use
        dispatcher: The client dispatcher instance
        _client: Lazy-loaded actual API client instance
    """

    def __init__(
        self,
        api_type: ApiSupportedContent,
        base_url: EndPointUrl,
        model_name: str,
        api_key: str,
        dispatcher: CompatibleClientDispatcher | None = None,
    ) -> None:
        """Initialize the factory proxy.

        Args:
            api_type: The type of API to create a client for
            base_url: The base URL for the API endpoint
            model_name: Name of the model to use
            api_key: Authentication key for the API
            dispatcher: Optional custom dispatcher (uses default if None)

        Raises:
            InvalidParameterError: If any parameter is empty or None
        """
        # Validate parameters early
        if not base_url or not base_url.strip():
            raise InvalidParameterError("base_url must be provided and non-empty")
        if not api_key or not api_key.strip():
            raise InvalidParameterError("api_key must be provided and non-empty")
        if not model_name or not model_name.strip():
            raise InvalidParameterError("model_name must be provided and non-empty")

        # Use the provided dispatcher, or fall back to the default
        self.dispatcher = dispatcher or CompatibleClientDispatcher()
        self.api_type = api_type
        self.base_url = base_url
        self.api_key = api_key
        self.model_name: str = model_name
        self._client: BaseAPIClient | None = None
        self._rest_timeout_config: tuple[float, float] | None = None

    @property
    def client(self) -> BaseAPIClient:
        """Get the underlying API client, creating it if necessary.

        Returns:
            BaseAPIClient: The actual API client instance

        Raises:
            UnsupportedAPITypeError: If no handler is registered for the API type
        """
        if self._client is None:
            try:
                self._client = self.dispatcher(
                    self.api_type, self.base_url, self.api_key, self.model_name
                )
                # Apply timeout configuration if stored and applicable
                if self._rest_timeout_config is not None and hasattr(
                    self._client, 'set_timeout'
                ):
                    connect_timeout, read_timeout = self._rest_timeout_config
                    self._client.set_timeout(connect_timeout, read_timeout)
            except KeyError as e:
                raise UnsupportedAPITypeError(
                    f"Unsupported API type: {self.api_type}"
                ) from e
        return self._client

    def chat_completion(self, messages: list[ChatMessage]) -> ChatCompletionResponse:
        """Send chat completion request using the underlying client.

        Args:
            messages: List of chat messages to send to the API

        Returns:
            ChatCompletionResponse: The API response containing generated content

        Raises:
            UnsupportedAPITypeError: If the API type is not supported
            APIClientError: If the API request fails or returns an error
            ResponseConversionError: If response parsing/conversion fails
        """
        return self.client.chat_completion(messages)

    def get_model_name(self) -> str:
        """Get the model name being used.

        Returns:
            str: The name of the model configured for this client
        """
        return self.model_name

    def __enter__(self) -> Self:
        """Enter the context manager.

        Returns:
            Self: The CompatibleClient instance for use in the with statement
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and cleanup resources.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.close()

    def close(self) -> None:
        """Cleanup resources from the underlying API client.

        This method ensures proper cleanup of any resources used by the
        underlying API client implementation, such as HTTP connections.
        It's safe to call multiple times.
        """
        if self._client is not None:
            if hasattr(self._client, 'close'):
                self._client.close()

    def configure_rest_timeouts(
        self, connect_timeout: float, read_timeout: float
    ) -> None:
        """Configure timeouts for REST API clients.

        This method allows configuring timeouts specifically for REST API clients.
        If the underlying client is not a REST API client, this method has no effect.

        Args:
            connect_timeout: Connection timeout in seconds
            read_timeout: Read timeout in seconds

        Raises:
            ValueError: If timeout values are not positive numbers

        Example:
            client = CompatibleClient('requests', 'https://api.example.com', 'key', 'model')
            client.configure_rest_timeouts(10.0, 30.0)
        """
        # Check if we have a REST API client
        if self._client is not None and hasattr(self._client, 'set_timeout'):
            self._client.set_timeout(connect_timeout, read_timeout)
        elif self.api_type == 'requests':
            # If client is not yet created but will be a REST client, store the config
            # This will be applied when the client is created
            self._rest_timeout_config = (connect_timeout, read_timeout)


"""
---------------------------------------------------------------------------
Implementations of classes compatible with various API types 
---------------------------------------------------------------------------
"""
from .types import (
    ChatChoice,
    ChatUsage,
    MessageRole,
)

"""
--------------------------------------------------------------------------
OpenAI API compatible client
--------------------------------------------------------------------------
"""
from openai import OpenAI

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
)


@CompatibleClientDispatcher.register(api_key='openai')
class OpenAICompatibleClient(BaseAPIClient):
    """OpenAI API compatible client implementation.

    This client provides compatibility with OpenAI's chat completion API
    and any APIs that follow the same interface structure. It handles
    message format conversion and response parsing automatically.

    Registration: Registered under 'openai' API type

    Usage:
        client = OpenAICompatibleClient('https://api.openai.com/v1', 'api-key', 'gpt-4')
        response = client.chat_completion(messages)

    Key attributes:
        client: OpenAI client instance for API communication
        model_name: Name of the model to use for requests
    """

    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        """Initialize OpenAI compatible client.

        Args:
            base_url: The base URL for the API endpoint
            api_key: Authentication key for the API
            model_name: Name of the model to use for requests

        Raises:
            InvalidParameterError: If any parameter is empty or None
        """
        # Validate parameters using parent class validation
        super().__init__(base_url, api_key, model_name)

        # initialize client attributes
        self.client: OpenAI = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name: str = model_name
        self.openai_messages: list[ChatCompletionMessageParam] = []

    def _convert_messages(self, messages: list[ChatMessage]) -> None:
        """Convert ChatMessage objects to OpenAI format.

        This method transforms the generic ChatMessage objects into OpenAI's
        specific message parameter types (User, Assistant, System) and stores
        them in the openai_messages attribute for use in API calls.

        Args:
            messages: List of ChatMessage objects to convert
        """
        self.openai_messages = []  # Clear previous message
        for message in messages:
            if message.role == 'user':
                self.openai_messages.append(
                    ChatCompletionUserMessageParam(
                        role='user', content=message.content or ''
                    )
                )
            elif message.role == 'assistant':
                self.openai_messages.append(
                    ChatCompletionAssistantMessageParam(
                        role='assistant', content=message.content or ''
                    )
                )
            elif message.role == 'system':
                self.openai_messages.append(
                    ChatCompletionSystemMessageParam(
                        role='system', content=message.content or ''
                    )
                )

    def _convert_response(
        self, openai_response: ChatCompletion
    ) -> ChatCompletionResponse:
        """Convert OpenAI response to ChatCompletionResponse format.

        This method transforms OpenAI's native ChatCompletion response into
        the unified ChatCompletionResponse format used across all client types.

        Args:
            openai_response: The raw response from OpenAI's API

        Returns:
            ChatCompletionResponse: Unified response format
        """

        choices: list[ChatChoice] = []
        for choice in openai_response.choices:
            message: ChatMessage = ChatMessage(
                role=choice.message.role,
                content=choice.message.content,
                name=getattr(choice.message, 'name', None),
                # tool_calls=getattr(choice.message, 'tool_calls', None),
            )
            choices.append(
                ChatChoice(
                    index=choice.index,
                    message=message,
                    finish_reason=choice.finish_reason,
                )
            )

        usage: ChatUsage | None = None
        if hasattr(openai_response, 'usage') and openai_response.usage:
            usage = ChatUsage(
                prompt_tokens=openai_response.usage.prompt_tokens,
                completion_tokens=openai_response.usage.completion_tokens,
                total_tokens=openai_response.usage.total_tokens,
            )

        return ChatCompletionResponse.create_response(
            id=openai_response.id,
            object=getattr(openai_response, 'object', 'chat.completion'),
            created=openai_response.created,
            model=openai_response.model,
            choices=choices,
            usage=usage,
            system_fingerprint=getattr(openai_response, 'system_fingerprint', None),
        )

    @override
    def chat_completion(self, messages: list[ChatMessage]) -> ChatCompletionResponse:
        """Send chat completion request to OpenAI API.

        Args:
            messages: List of chat messages to send to the API

        Returns:
            ChatCompletionResponse: The API response containing generated content

        Raises:
            Exception: If the OpenAI API request fails
        """
        self._convert_messages(messages)

        openai_response: ChatCompletion = self.client.chat.completions.create(
            model=self.model_name, messages=self.openai_messages
        )
        return self._convert_response(openai_response)

    @override
    def get_model_name(self) -> str:
        """Get the model name being used.

        Returns:
            str: The name of the model configured for this client
        """
        return self.model_name

    @override
    def close(self) -> None:
        """Close the underlying HTTP client."""
        if hasattr(self.client, 'close'):
            self.client.close()
        elif hasattr(self.client, '_client') and hasattr(self.client._client, 'close'):
            # OpenAI client use httpx internal client
            self.client._client.close()


"""
-------------------------------------------------------------------------------
REST API compatible client.
-------------------------------------------------------------------------------
"""

import json
import requests  # type: ignore
from requests.models import Response  # type: ignore # noqa: E501
from typing import Any


@CompatibleClientDispatcher.register(api_key='requests')
class RestAPICompatibleClient(BaseAPIClient):
    """Generic REST API compatible client implementation.

    This client provides compatibility with generic REST APIs that accept
    chat completion requests via HTTP POST. It handles JSON serialization
    and HTTP authentication automatically. Supports configurable connection
    and read timeouts for improved reliability and performance tuning.

    Registration: Registered under 'requests' API type

    Usage:
        # Basic usage with default timeouts (30s connect, 60s read)
        client = RestAPICompatibleClient('https://api.example.com/v1/chat', 'api-key', 'model-name')

        # Runtime timeout adjustment
        client.set_timeout(10.0, 30.0)  # 10s connect, 30s read

        # Alternative: Pythonic property-based timeout setting
        client.timeout = (10.0, 30.0)  # 10s connect, 30s read
        current_timeouts = client.timeout  # Get current timeouts

        response = client.chat_completion(messages)

    Key attributes:
        base_url: The API endpoint URL
        api_key: Authentication key for requests
        model_name: Name of the model to use
        connect_timeout: Connection timeout in seconds
        read_timeout: Read timeout in seconds
    """

    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        """Initialize REST API compatible client with default timeout settings.

        Args:
            base_url: The base URL for the API endpoint
            api_key: Authentication key for the API
            model_name: Name of the model to use for requests

        Raises:
            InvalidParameterError: If any parameter is empty or None

        Note:
            Uses default timeout values (30s connect, 60s read). For custom timeouts,
            use set_timeout() method or the timeout property after initialization.
        """
        # Validate parameters using parent class validation
        super().__init__(base_url, api_key, model_name)

        # initialize client attributes with default timeouts
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.model_name: str = model_name
        self.connect_timeout: float = 30.0  # Default connection timeout
        self.read_timeout: float = 60.0  # Default read timeout
        self.rest_messages: list[dict[str, str | None]] = []
        # Optional, maintain a session for connection pooling
        self._session: requests.Session | None = None

    @property
    def session(self) -> requests.Session:
        """Get or create a requests session for connection pooling.

        Returns:
            requests.Session: Configured session with headers and timeout
        """
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
            )
            # Set configurable timeout (connect, read)
            self._session.timeout = (self.connect_timeout, self.read_timeout)
        return self._session

    def set_timeout(self, connect_timeout: float, read_timeout: float) -> None:
        """Set new timeout values and reset the session if it exists.

        This method allows changing timeout values after client initialization.
        If a session already exists, it will be closed and recreated with new timeout values.

        Args:
            connect_timeout: New connection timeout in seconds
            read_timeout: New read timeout in seconds

        Raises:
            ValueError: If timeout values are not positive numbers
        """
        if connect_timeout <= 0:
            raise ValueError("connect_timeout must be a positive number")
        if read_timeout <= 0:
            raise ValueError("read_timeout must be a positive number")

        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

        # Reset session to apply new timeout values
        if self._session:
            self._session.close()
            self._session = None

    def get_timeout(self) -> tuple[float, float]:
        """Get current timeout values.

        Returns:
            tuple[float, float]: A tuple of (connect_timeout, read_timeout) in seconds
        """
        return (self.connect_timeout, self.read_timeout)

    @property
    def timeout(self) -> tuple[float, float]:
        """Get current timeout values as (connect_timeout, read_timeout).

        Returns:
            tuple[float, float]: A tuple of (connect_timeout, read_timeout) in seconds
        """
        return (self.connect_timeout, self.read_timeout)

    @timeout.setter
    def timeout(self, value: tuple[float, float]) -> None:
        """Set timeout values from (connect_timeout, read_timeout) tuple.

        Args:
            value: A tuple of (connect_timeout, read_timeout) in seconds

        Raises:
            ValueError: If value is not a 2-element tuple or timeout values are not positive
        """
        if len(value) != 2:
            raise ValueError(
                "timeout must be a tuple of (connect_timeout, read_timeout)"
            )
        connect_timeout, read_timeout = value

        # Reuse existing validation logic
        if connect_timeout <= 0:
            raise ValueError("connect_timeout must be a positive number")
        if read_timeout <= 0:
            raise ValueError("read_timeout must be a positive number")

        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

        # Reset session to apply new timeout values
        if self._session:
            self._session.close()
            self._session = None

    def _convert_messages(self, messages: list[ChatMessage]) -> None:
        """Convert ChatMessage objects to dictionary format for REST API.

        This method transforms the generic ChatMessage objects into simple
        dictionaries containing 'role' and 'content' keys, which is the
        standard format expected by most REST APIs.

        Args:
            messages: List of ChatMessage objects to convert
        """
        self.rest_messages = [
            {
                'role': message.role,
                'content': message.content,
            }
            for message in messages
        ]

    def _from_dict(self, data: dict[str, Any]) -> ChatCompletionResponse:
        """
        Create from dictionary (e.g., from REST API JSON response).

        This replaces the deprecated ChatCompletion.parse_obj method.
        """
        return ChatCompletionResponse.model_validate(data)

    def _convert_response(self, rest_response: Response) -> ChatCompletionResponse:
        """Convert REST API response to ChatCompletionResponse format.

        Args:
            rest_response: The HTTP response from the REST API

        Returns:
            ChatCompletionResponse: Parsed response object

        Raises:
            APIClientError: If the API request fails or response is invalid
        """
        # Check for successful response
        if rest_response.status_code == 200:
            try:
                # Parse JSON response
                response_data = rest_response.json()
                # Use our new method instead of deprecated parse_obj
                chat_response: ChatCompletionResponse = self._from_dict(
                    data=response_data
                )
                return chat_response
            except ValueError as e:
                # JSON parsing failed
                raise ResponseConversionError(
                    f'Failed to parse JSON response: {e}. Response text: {rest_response.text[:500]}'
                ) from e
            except Exception as e:
                # ChatCompletionResponse parsing failed
                raise ResponseConversionError(
                    f'Failed to convert response to ChatCompletionResponse: {e}'
                ) from e
        else:
            # Handle error responses with detailed information
            try:
                error_details = rest_response.json()
                error_message = error_details.get('error', {}).get(
                    'message', str(error_details)
                )
            except ValueError:
                # If JSON parsing fails, use raw text
                error_message = rest_response.text[:500]  # Limit error message length

            raise APIClientError(
                f'API request failed with status {rest_response.status_code}: {error_message}'
            )

    @override
    def chat_completion(self, messages: list[ChatMessage]) -> ChatCompletionResponse:
        """Send chat completion request to REST API endpoint.

        Args:
            messages: List of chat messages to send to the API

        Returns:
            ChatCompletionResponse: The API response containing generated content

        Raises:
            APIClientError: If the HTTP request fails or returns an error status
            ResponseConversionError: If JSON parsing or response conversion fails
        """
        self._convert_messages(messages)

        data = {
            'messages': self.rest_messages,
            'model': self.model_name,
        }
        rest_response: Response = self.session.post(
            url=self.base_url,
            data=json.dumps(data),
        )

        assert rest_response is not None
        return self._convert_response(rest_response)

    @override
    def get_model_name(self) -> str:
        """Get the model name being used.

        Returns:
            str: The name of the model configured for this client
        """
        return self.model_name

    @override
    def close(self) -> None:
        """Close the requests session."""
        if self._session:
            self._session.close()
            self._session = None


# class HuggingFaceAPICompatibleClient(BaseAPIClient):

#     @override
#     def chat_completion(self, messages: list[ChatMessage]) -> ChatCompletionResponse:
#         '''Send chat completion request and return response.'''
#         pass

#     @override
#     def get_model_name(self) -> str:
#         '''Get the model name being used.'''
#         pass
