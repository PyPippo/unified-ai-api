'''unified_ai_api package - Unified API Connection Manager for Multiple AI Providers

This package provides a clean, unified interface for connecting to various AI providers
through different API types in a transparent way.

Main Components:
- APIConnectionManager: The primary class for managing API connections
- BaseAPIClient: Abstract base class for API clients
- OpenAICompatibleClient: Implementation for OpenAI-compatible APIs

Usage:
    from unified_ai_api import APIConnectionManager

    # Interactive setup
    manager = APIConnectionManager()
    if manager.interactive_setup():
        manager.start_chat_loop()

    # Direct configuration
    manager = APIConnectionManager()
    manager.configure_api('OPENROUTER', 0, 'openai')
    with manager.create_chatclient() as client:
        response = client.send_message('Hello!')
        print(response)
'''

# Import the classes we want to expose
from .api_connection import APIConnectionManager
from .compatible_client_api import BaseAPIClient, OpenAICompatibleClient


# Explicitly define what gets exported
__all__ = [
    'APIConnectionManager',
    'BaseAPIClient',
    'OpenAICompatibleClient',
]

# Version information
__version__ = '1.0.0'
__author__ = 'API_AI Team'
__description__ = 'Unified API Connection Manager for Multiple AI Providers'
