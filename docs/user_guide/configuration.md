# Configuration Guide

Comprehensive guide for configuring the Unified AI API Connection package with different providers, API keys, and customization options.

## Configuration Overview

The package uses a layered configuration approach:

1. **Provider Configuration** (`providers.json`) - Defines available providers and their capabilities
2. **API Key Configuration** (Environment variables or `secret.json`) - Stores authentication credentials  
3. **Runtime Configuration** (Code) - Dynamic settings and client customization

## API Key Configuration

### Method 1: Environment Variables (Recommended)

Environment variables are the most secure method for production environments.

```bash
# OpenRouter
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# OpenAI
export OPENAI_API_KEY="sk-your-openai-key-here"

# HuggingFace
export HUGGINGFACE_API_KEY="hf_your-token-here"

# Custom providers
export CUSTOM_PROVIDER_API_KEY="your-custom-key"
```

**Windows:**

```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-key-here
set OPENAI_API_KEY=sk-your-openai-key-here
```

**PowerShell:**

```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"
$env:OPENAI_API_KEY="sk-your-openai-key-here"
```

### Method 2: Configuration File (Development)

For development environments, you can use a `secret.json` file:

```bash
# Copy the template
cp src/unified_ai_api/config/secret.json.template src/unified_ai_api/config/secret.json
```

Edit `secret.json`:

```json
{
  "OPENROUTER": {
    "0": {
      "secret_api_key": "sk-or-v1-your-key-here"
    }
  },
  "OPENAI": {
    "0": {
      "secret_api_key": "sk-your-openai-key-here"
    }
  },
  "HUGGINGFACE": {
    "0": {
      "secret_api_key": "hf_your-token-here"
    }
  }
}
```

**Important**: `secret.json` is git-ignored for security. Never commit API keys to version control.

### Method 3: Programmatic Configuration

```python
import os

# Set at runtime
os.environ['OPENROUTER_API_KEY'] = 'your-key-here'

# Then use normally
from unified_ai_api import APIConnectionManager
manager = APIConnectionManager()
```

## Provider Configuration

### Understanding providers.json

The `providers.json` file defines available providers, their models, and supported features:

```json
{
  "OPENROUTER": [
    {
      "config_name": "openrouter_default",
      "model_url": "https://openrouter.ai/models",
      "model_name": "openai/gpt-3.5-turbo",
      "init_config_msg": "You are a helpful AI assistant.",
      "api_supported": ["openai"],
      "api_endpoints": {
        "openai": "https://openrouter.ai/api/v1"
      }
    }
  ],
  "OPENAI": [
    {
      "config_name": "openai_gpt35",
      "model_url": "https://platform.openai.com/docs/models",
      "model_name": "gpt-3.5-turbo",
      "init_config_msg": "You are a helpful assistant.",
      "api_supported": ["openai"],
      "api_endpoints": {
        "openai": "https://api.openai.com/v1"
      }
    }
  ]
}
```

### Adding Custom Providers

To add a new provider, edit `providers.json`:

```json
{
  "CUSTOM_PROVIDER": [
    {
      "config_name": "custom_model",
      "model_url": "https://your-provider.com/models",
      "model_name": "your-model-name",
      "init_config_msg": "Custom system prompt",
      "api_supported": ["openai", "requests"],
      "api_endpoints": {
        "openai": "https://your-provider.com/v1",
        "requests": "https://your-provider.com/api"
      }
    }
  ]
}
```

### Multiple Configurations per Provider

You can define multiple configurations for the same provider:

```json
{
  "OPENAI": [
    {
      "config_name": "gpt35_turbo",
      "model_name": "gpt-3.5-turbo",
      "init_config_msg": "You are a helpful assistant."
    },
    {
      "config_name": "gpt4",
      "model_name": "gpt-4",
      "init_config_msg": "You are an expert AI assistant."
    }
  ]
}
```

Access different configurations using the `config_index`:

```python
# Use first configuration (index 0)
manager.configure_api('OPENAI', 0, 'openai')  # gpt-3.5-turbo

# Use second configuration (index 1)  
manager.configure_api('OPENAI', 1, 'openai')  # gpt-4
```

## Runtime Configuration

### Discovery and Validation

```python
from unified_ai_api import APIConnectionManager

manager = APIConnectionManager()

# Discover available providers
providers = manager.get_available_providers()
print("Available providers:", providers)

# Check configurations for a provider
configs = manager.get_provider_configs('OPENROUTER')
for i, config in enumerate(configs):
    print(f"Config {i}: {config['model_name']}")

# Check supported API types
apis = manager.get_supported_api('OPENROUTER', 0)
print("Supported APIs:", apis)
```

### Configuration Validation

```python
# Configure connection
manager.configure_api('OPENROUTER', 0, 'openai')

# Validate before using
if manager.validate_configuration():
    print("✅ Configuration is valid")
    # Safe to create clients
else:
    print("❌ Configuration incomplete")
    # Check API keys and provider settings
```

### Builder Pattern Configuration

```python
# Method chaining
client = (APIConnectionManager()
         .configure_api('OPENROUTER', 0, 'openai')
         .create_chatclient())

# Use client...
client.close()
```

## Advanced Configuration

### Custom Timeouts

```python
manager = APIConnectionManager()
manager.configure_api('OPENROUTER', 0, 'openai')

with manager.create_chatclient() as client:
    # Configure timeouts for REST clients
    if hasattr(client.compatible_client, 'configure_rest_timeouts'):
        client.compatible_client.configure_rest_timeouts(
            connect_timeout=10.0,  # 10 second connection timeout
            read_timeout=30.0      # 30 second read timeout
        )
```

### Custom System Messages

Modify the initial system message in `providers.json`:

```json
{
  "config_name": "specialized_assistant",
  "model_name": "gpt-3.5-turbo",
  "init_config_msg": "You are a specialized Python programming assistant. Always provide code examples and explain best practices."
}
```

Or programmatically after client creation:

```python
with manager.create_chatclient() as client:
    # Clear default history and set custom message
    client.clear_chat_history()
    client.send_message("You are a specialized data science assistant.")
```

## Configuration Best Practices

### 1. Environment-Specific Configuration

```python
import os

# Development
if os.environ.get('ENVIRONMENT') == 'development':
    # Use local configuration or test keys
    provider = 'TEST_PROVIDER'
else:
    # Production
    provider = 'OPENROUTER'

manager.configure_api(provider, 0, 'openai')
```

### 2. Configuration Validation

```python
def setup_ai_connection(provider, config_index, api_type):
    """Setup AI connection with validation."""
    manager = APIConnectionManager()
    
    try:
        # Check if provider exists
        available_providers = manager.get_available_providers()
        if provider not in available_providers:
            raise ValueError(f"Provider {provider} not available")
        
        # Check if config index is valid
        configs = manager.get_provider_configs(provider)
        if config_index >= len(configs):
            raise ValueError(f"Config index {config_index} out of range")
        
        # Check if API type is supported
        supported_apis = manager.get_supported_api(provider, config_index)
        if api_type not in supported_apis:
            raise ValueError(f"API type {api_type} not supported")
        
        # Configure
        manager.configure_api(provider, config_index, api_type)
        
        # Final validation
        if not manager.validate_configuration():
            raise ValueError("Configuration validation failed")
        
        return manager
        
    except Exception as e:
        print(f"Configuration error: {e}")
        return None
```

### 3. Dynamic Provider Selection

```python
def choose_best_provider():
    """Automatically choose the best available provider."""
    manager = APIConnectionManager()
    providers = manager.get_available_providers()
    
    # Priority order
    preferred_providers = ['OPENAI', 'OPENROUTER', 'HUGGINGFACE']
    
    for provider in preferred_providers:
        if provider in providers:
            try:
                configs = manager.get_provider_configs(provider)
                if configs:
                    apis = manager.get_supported_api(provider, 0)
                    if 'openai' in apis:
                        manager.configure_api(provider, 0, 'openai')
                        if manager.validate_configuration():
                            print(f"✅ Selected provider: {provider}")
                            return manager
            except Exception:
                continue
    
    raise ValueError("No suitable provider found")
```

## Configuration Files Reference

### providers.json Structure

```json
{
  "PROVIDER_NAME": [
    {
      "config_name": "human_readable_name",
      "model_url": "documentation_url",
      "model_name": "actual_model_identifier",
      "init_config_msg": "system_prompt",
      "api_supported": ["openai", "requests"],
      "api_endpoints": {
        "openai": "openai_compatible_endpoint",
        "requests": "generic_rest_endpoint"
      }
    }
  ]
}
```

### secret.json Structure

```json
{
  "PROVIDER_NAME": {
    "config_index": {
      "secret_api_key": "your_api_key_here"
    }
  }
}
```

## Troubleshooting Configuration

### Common Issues

1. **"No providers found"**
   - Check `src/unified_ai_api/config/providers.json` exists
   - Verify JSON syntax is valid

2. **"No valid API key found"**
   - Check environment variables: `echo $OPENROUTER_API_KEY`
   - Verify `secret.json` format and location
   - Ensure API key format is correct

3. **"Configuration validation failed"**
   - Run discovery methods to check availability
   - Verify provider name matches exactly (case-sensitive)
   - Check config_index is within range

4. **"API type not supported"**
   - Use `get_supported_api()` to check available types
   - Verify API type spelling (usually 'openai' or 'requests')

### Debug Configuration

```python
def debug_configuration():
    """Debug configuration issues."""
    manager = APIConnectionManager()
    
    print("=== Configuration Debug ===")
    
    # Check providers
    try:
        providers = manager.get_available_providers()
        print(f"✅ Available providers: {providers}")
    except Exception as e:
        print(f"❌ Provider loading failed: {e}")
        return
    
    # Check each provider
    for provider in providers:
        print(f"\n--- {provider} ---")
        try:
            configs = manager.get_provider_configs(provider)
            print(f"  Configurations: {len(configs)}")
            
            for i, config in enumerate(configs):
                print(f"  Config {i}: {config.get('model_name', 'Unknown')}")
                
                apis = manager.get_supported_api(provider, i)
                print(f"    APIs: {apis}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Check API keys
    print(f"\n=== API Keys ===")
    import os
    key_vars = ['OPENROUTER_API_KEY', 'OPENAI_API_KEY', 'HUGGINGFACE_API_KEY']
    for var in key_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:10]}...")
        else:
            print(f"❌ {var}: Not set")

# Run debug
debug_configuration()
```

---

*For examples of different configuration patterns, see the [examples directory](../../examples/).*
