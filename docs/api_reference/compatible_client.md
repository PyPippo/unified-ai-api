# CompatibleClient API Reference

This document provides the complete API reference for the `CompatibleClient` class.

## Class: CompatibleClient

The `CompatibleClient` class provides a unified interface for interacting with different AI API providers.

### Constructor

```python
CompatibleClient(api_type, base_url, api_key, model_name)
```

#### Parameters

- `api_type` (str): The type of API (e.g., "openai", "rest")
- `base_url` (str): Base URL for the API endpoint
- `api_key` (str): Authentication key for the API
- `model_name` (str): Name of the model to use

### Methods

#### send_message()

Sends a message to the AI model and returns the response.

#### get_available_models()

Retrieves a list of available models for the current API.

#### configure_parameters()

Configures model parameters like temperature, max_tokens, etc.

#### close()

Properly closes the connection and cleans up resources.

### Properties

#### is_connected

Returns the connection status.

#### current_model

Returns the currently selected model.

#### api_info

Returns information about the current API configuration.

### Usage Examples

```python
# Basic usage examples will be added here
```

### Error Handling

List of exceptions that can be raised by this class and when they occur.

---

*This documentation is under development. More detailed content will be added in future versions.*
