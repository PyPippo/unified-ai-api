# Types API Reference

This document provides the complete API reference for type definitions used throughout the Unified AI API connection library.

## Type Definitions

### Core Types

#### ProviderName

```python
ProviderName = Literal[...]
```

Defines the supported API provider names.

#### APIType

Enumeration of supported API types.

#### ModelInfo

Data structure containing model information.

#### ConnectionConfig

Configuration structure for API connections.

### Configuration Types

#### OpenAIConfig

Configuration specific to OpenAI-compatible APIs.

#### RESTConfig

Configuration for generic REST API connections.

#### AuthConfig

Authentication configuration structure.

### Response Types

#### APIResponse

Standard response structure from API calls.

#### ModelList

Structure for model listing responses.

#### ErrorResponse

Structure for error responses.

### Callback Types

#### MessageCallback

Type definition for message handling callbacks.

#### ErrorCallback

Type definition for error handling callbacks.

#### ProgressCallback

Type definition for progress tracking callbacks.

### Utility Types

#### ConnectionParams

Parameters for establishing connections.

#### RequestOptions

Options for customizing API requests.

#### ValidationResult

Result structure for parameter validation.

## Type Guards

Functions for runtime type checking and validation.

### is_valid_provider()

Validates provider name format.

### is_valid_config()

Validates configuration structure.

### is_api_response()

Validates API response format.

## Usage Examples

```python
# Type usage examples will be added here
```

---

*This documentation is under development. More detailed content will be added in future versions.*
