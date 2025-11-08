# Unified AI API Connection

Welcome to the comprehensive documentation for the Unified AI API Connection package.

## Overview

The Unified AI API Connection is a Python package that provides a clean, type-safe, and extensible interface for interacting with multiple AI service providers through a single unified API.

## Quick Navigation

### Getting Started

- [Installation](installation.md) - Setup and installation guide
- [Quick Start](quickstart.md) - Get up and running in minutes

### User Guide

- [Basic Usage](user_guide/basic_usage.md) - Essential concepts and workflows
- [Configuration](user_guide/configuration.md) - Provider and API configuration
- [API Types](user_guide/api_types.md) - Understanding different API types
- [Error Handling](user_guide/error_handling.md) - Troubleshooting and error recovery

### API Reference

- [Compatible Client](api_reference/compatible_client.md) - Core client interface
- [Dispatcher](api_reference/dispatcher.md) - Client registration and factory
- [Types](api_reference/types.md) - Type definitions and data structures

### Additional Resources

- [Examples](examples.md) - Practical usage examples
- [Contributing](contributing.md) - How to contribute to the project
- [Changelog](changelog.md) - Version history and changes

## Key Features

- **Multi-Provider Support**: OpenAI, HuggingFace, OpenRouter, and more
- **Type Safety**: Full type annotations and Pydantic validation
- **Unified Interface**: Consistent API across all providers
- **Flexible Configuration**: Environment variables, config files, or programmatic setup
- **Interactive Setup**: Built-in wizards for easy configuration
- **Session Management**: Multiple concurrent connections and chat sessions
- **Error Handling**: Comprehensive error handling and recovery

## Quick Example

```python
from unified_ai_api import APIConnectionManager

# Interactive setup
manager = APIConnectionManager()
if manager.interactive_setup():
    manager.start_chat_loop()

# Or programmatic setup
manager = APIConnectionManager()
manager.configure_api('OPENAI', 0, 'openai')
with manager.create_chatclient() as client:
    response = client.send_message("Hello!")
    print(response)
```

## Support

- Check the [troubleshooting guide](user_guide/error_handling.md) for common issues
- Review [examples](examples.md) for practical usage patterns
- See [API reference](api_reference/) for detailed method documentation

---

*For the most up-to-date examples, see the [examples directory](../examples/) in the repository.*
