# Basic Usage Guide

This guide covers the fundamental concepts and basic usage patterns of the Unified AI API Connection package.

## Core Concepts

### APIConnectionManager

The central hub for managing AI provider connections. It handles configuration, client creation, and resource management.

### ChatClient

Individual chat session instances that maintain conversation history and handle message exchange with AI providers.

### Providers

AI service providers (OpenAI, OpenRouter, HuggingFace) that offer different models and capabilities.

### API Types

Different interface standards (openai, requests) that define how to communicate with providers.

## Basic Workflow

1. **Create Manager** → 2. **Configure Connection** → 3. **Create Client** → 4. **Chat** → 5. **Clean Up**

## Usage Patterns

### Pattern 1: Interactive Setup

Best for: First-time users, exploration, prototyping

```python
from unified_ai_api import APIConnectionManager

manager = APIConnectionManager()

# Interactive wizard guides you through setup
if manager.interactive_setup():
    # Automatic chat loop
    manager.start_chat_loop()
```

### Pattern 2: Direct Configuration

Best for: Production code, automation, known configurations

```python
from unified_ai_api import APIConnectionManager

manager = APIConnectionManager()

# Direct configuration
manager.configure_api(
    provider='OPENROUTER',
    config_index=0,
    api_type='openai'
)

# Create and use client
with manager.create_chatclient() as client:
    response = client.send_message("Hello, AI!")
    print(response)
```

### Pattern 3: Discovery and Selection

Best for: Dynamic applications, user choice

```python
manager = APIConnectionManager()

# Discover available options
providers = manager.get_available_providers()
print("Available providers:", providers)

# Get configurations for a provider
configs = manager.get_provider_configs('OPENROUTER')
print(f"Configurations: {len(configs)}")

# Get supported API types
apis = manager.get_supported_api('OPENROUTER', 0)
print("Supported APIs:", apis)

# Configure based on discovery
manager.configure_api('OPENROUTER', 0, apis[0])
```

## Managing Conversations

### Single Message

```python
with manager.create_chatclient() as client:
    response = client.send_message("What is Python?")
    print(response)
```

### Conversation Flow

```python
with manager.create_chatclient() as client:
    # Messages are automatically added to history
    response1 = client.send_message("Hello!")
    response2 = client.send_message("Can you remember what I just said?")
    
    # Check conversation length
    print(f"Messages in history: {len(client._chat_history)}")
```

### Clear History

```python
with manager.create_chatclient() as client:
    client.send_message("First conversation")
    
    # Start fresh
    client.clear_chat_history()
    
    client.send_message("New conversation")  # AI won't remember previous
```

## Session Management

### Named Sessions

```python
# Create clients with specific session IDs
client1 = manager.create_chatclient(session_id="science_chat")
client2 = manager.create_chatclient(session_id="coding_chat")

# Use them independently
client1.send_message("Explain quantum physics")
client2.send_message("Write a Python function")

# Clean up
client1.close()
client2.close()
```

### Multiple Sessions

```python
# Manager tracks all active clients
clients = []
for i in range(3):
    client = manager.create_chatclient(session_id=f"session_{i}")
    clients.append(client)

# Use all clients...

# Clean up all at once
manager.close_all_clients()
```

## Connection Information

### Check Configuration

```python
# Before creating clients
if manager.validate_configuration():
    print("✅ Ready to create clients")
else:
    print("❌ Configuration incomplete")
```

### Get Connection Details

```python
# Manager level
params = manager.get_connection_params()
print(f"Provider: {params['provider']}")
print(f"Model: {params['model_name']}")

# Client level
with manager.create_chatclient() as client:
    print(f"Model: {client.get_model_name()}")
    print(f"Connected: {client.get_connection_status()}")
    
    details = client.get_connection_params()
    print(f"Endpoint: {details['endpoint_url']}")
```

## Resource Management

### Context Managers (Recommended)

```python
# Automatic cleanup
with manager.create_chatclient() as client:
    # Use client...
    pass  # Client is automatically closed
```

### Manual Management

```python
# Manual cleanup
client = manager.create_chatclient()
try:
    # Use client...
    pass
finally:
    client.close()  # Always clean up
```

### Bulk Cleanup

```python
# Create multiple clients
client1 = manager.create_chatclient()
client2 = manager.create_chatclient()

# Clean up all at once
manager.close_all_clients()
```

## Best Practices

### 1. Always Use Context Managers

```python
# ✅ Good
with manager.create_chatclient() as client:
    response = client.send_message("Hello")

# ❌ Avoid (unless you handle cleanup manually)
client = manager.create_chatclient()
response = client.send_message("Hello")
# Missing cleanup!
```

### 2. Validate Configuration

```python
# ✅ Good
manager.configure_api('OPENROUTER', 0, 'openai')
if manager.validate_configuration():
    with manager.create_chatclient() as client:
        # Use client...
        pass
```

### 3. Handle Errors Gracefully

```python
# ✅ Good
try:
    with manager.create_chatclient() as client:
        response = client.send_message("Hello")
        if response:
            print(response)
        else:
            print("No response received")
except Exception as e:
    print(f"Error: {e}")
```

### 4. Use Meaningful Session IDs

```python
# ✅ Good
client = manager.create_chatclient(session_id="user_support_chat")

# ❌ Less clear
client = manager.create_chatclient(session_id="session_1")
```

## Common Patterns Summary

| Use Case | Pattern | Example |
|----------|---------|---------|
| First time | Interactive | `manager.interactive_setup()` |
| Production | Direct config | `manager.configure_api(...)` |
| Single Q&A | Context manager | `with manager.create_chatclient():` |
| Long conversation | Named session | `session_id="main_chat"` |
| Multiple topics | Multiple clients | Different session IDs |
| Exploration | Discovery | `get_available_providers()` |

## Next Steps

- [Configuration Guide](configuration.md) - Advanced configuration options
- [API Types](api_types.md) - Understanding different API interfaces
- [Error Handling](error_handling.md) - Robust error handling patterns

---

*For working examples, see the [examples directory](../../examples/).*
