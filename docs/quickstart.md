# Quick Start Guide

Get up and running with the Unified AI API Connection in just a few minutes.

## 1. Installation

```bash
pip install -e .
```

## 2. Configure API Keys

Choose one method:

### Option A: Environment Variables (Recommended)

```bash
export OPENROUTER_API_KEY="your-key-here"
```

### Option B: Configuration File

```bash
# Copy template and edit
cp src/unified_ai_api/config/secret.json.template src/unified_ai_api/config/secret.json
# Edit secret.json with your API keys
```

## 3. Quick Examples

### Interactive Setup (Easiest)

```python
from unified_ai_api import APIConnectionManager

manager = APIConnectionManager()

# Interactive configuration wizard
if manager.interactive_setup():
    # Start chatting immediately
    manager.start_chat_loop()
```

### Programmatic Setup

```python
from unified_ai_api import APIConnectionManager

# Create and configure manager
manager = APIConnectionManager()
manager.configure_api(
    provider='OPENROUTER',  # or 'OPENAI', 'HUGGINGFACE'
    config_index=0,
    api_type='openai'
)

# Create chat client
with manager.create_chatclient() as client:
    response = client.send_message("Hello! How are you?")
    print(response)
```

### Command Line Usage

```bash
# Run basic example
python examples/basic_usage.py

# Run specific advanced example
python examples/advanced_usage.py 2
```

## 4. Understanding the Workflow

1. **Create Manager**: `APIConnectionManager()` - Central control hub
2. **Configure Connection**: Choose provider, model, and API type
3. **Create Client**: Get a chat client for conversations
4. **Send Messages**: Exchange messages with the AI
5. **Clean Up**: Close clients when done

## 5. Provider Overview

| Provider | API Types | Models Available |
|----------|-----------|------------------|
| OpenRouter | `openai` | Multiple models via OpenRouter |
| OpenAI | `openai` | GPT-3.5, GPT-4, etc. |
| HuggingFace | `requests` | Various open-source models |

## 6. Common Patterns

### Single Conversation

```python
manager = APIConnectionManager()
manager.configure_api('OPENROUTER', 0, 'openai')

with manager.create_chatclient() as client:
    response = client.send_message("Explain Python in one sentence")
    print(response)
```

### Multiple Questions

```python
manager = APIConnectionManager()
manager.configure_api('OPENROUTER', 0, 'openai')

with manager.create_chatclient() as client:
    questions = [
        "What is machine learning?",
        "How does neural networks work?",
        "What is the future of AI?"
    ]
    
    for question in questions:
        response = client.send_message(question)
        print(f"Q: {question}")
        print(f"A: {response}\n")
```

### Error Handling

```python
try:
    manager = APIConnectionManager()
    manager.configure_api('OPENROUTER', 0, 'openai')
    
    with manager.create_chatclient() as client:
        response = client.send_message("Hello!")
        if response:
            print(response)
        else:
            print("No response received")
            
except Exception as e:
    print(f"Error: {e}")
```

## 7. Next Steps

- **[Basic Usage Guide](user_guide/basic_usage.md)** - Learn core concepts
- **[Configuration Guide](user_guide/configuration.md)** - Advanced setup options
- **[Examples](examples.md)** - More comprehensive examples
- **[API Reference](api_reference/)** - Detailed method documentation

## 8. Troubleshooting Quick Fixes

### "No providers found"

Check that `src/unified_ai_api/config/providers.json` exists.

### "No valid API key"

Verify your API key configuration:

```python
import os
print("OpenRouter key:", os.environ.get('OPENROUTER_API_KEY'))
```

### "Import error"

Ensure package is installed:

```bash
pip list | grep unified-ai-api
```

### "Connection failed"

Test your API key directly:

```python
from unified_ai_api import APIConnectionManager
manager = APIConnectionManager()
providers = manager.get_available_providers()
print("Available:", providers)
```

---

*Ready to dive deeper? Check out the [user guide](user_guide/) for comprehensive documentation.*
