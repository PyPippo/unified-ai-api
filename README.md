# Unified AI API Connection Manager

A clean, modular, and secure Python package for interacting with multiple AI service providers through a unified interface.

## Features

- 🔌 **Unified Interface**: Connect to multiple AI providers (OpenRouter, HuggingFace) through a single API
- 🔐 **Secure Authentication**: Environment variable and config file support for API keys
- 🎯 **Type Safe**: Full type annotations and Pydantic validation
- 🔄 **Extensible**: Abstract base class design for easy provider additions
- 💬 **Interactive**: Built-in chat loop and interactive setup
- 📦 **Modular**: Clean separation of concerns with private internal modules

## Installation

### From Source

```bash
git clone <repository-url>
cd unified-ai-api
pip install -e .
```

### From PyPI (when published)

```bash
pip install unified-ai-api
```

## Quick Start

### Basic Usage

```python
from unified_ai_api import APIConnectionManager

# Initialize manager
manager = APIConnectionManager()

# Interactive setup
if manager.interactive_setup():
    # Start chat session
    manager.start_chat_loop()
```

### Programmatic Configuration

```python
from unified_ai_api import APIConnectionManager

manager = APIConnectionManager()

# Configure connection
manager.configure_api('OPENROUTER', 0, 'openai')

# Create and use chat client
with manager.create_chatclient() as client:
    response = client.send_message("Hello!")
    print(response)
```

### Command Line Interface

```bash
# Run interactive setup and chat
unified-ai-api

# Or run examples
python examples/basic_usage.py
python examples/openai_example.py
```

## Configuration

### API Keys

Set up your API keys using one of these methods:

#### 1. Environment Variables (Recommended)

```bash
export OPENROUTER_API_KEY="your-openrouter-key"
export HUGGINGFACE_API_KEY="your-huggingface-token"
```

#### 2. Configuration File

Copy the template and add your API keys:

```bash
cp src/unified_ai_api/config/secret.json.template src/unified_ai_api/config/secret.json
```

Then edit `secret.json` and replace the placeholder values with your actual API keys. The keys are referenced by the `config_name` from `providers.json`:

```json
{
    "gemma-3-4b-it:free": "sk-or-v1-your-actual-openrouter-key",
    "llama-3-1-70b-instruct:fireworks-ai": "hf_your-actual-huggingface-token"
}
```

### Supported Providers

- **OpenRouter**: OpenAI-compatible API access to multiple LLMs
- **HuggingFace**: Access to HuggingFace Hub models
- **Extensible**: Add new providers via the `BaseAPIClient` interface

## Advanced Usage

### Direct Client Usage

```python
from unified_ai_api import OpenAICompatibleClient

client = OpenAICompatibleClient(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-key",
    model_name="meta-llama/llama-3.1-8b-instruct:free"
)

response = client.chat_completion([
    {"role": "user", "content": "Hello!"}
])
```

### Multiple Sessions

```python
manager = APIConnectionManager()
manager.configure_api('OPENROUTER', 0, 'openai')

# Session 1
with manager.create_chatclient(session_id='session1') as client1:
    response1 = client1.send_message("Hello from session 1")

# Session 2  
with manager.create_chatclient(session_id='session2') as client2:
    response2 = client2.send_message("Hello from session 2")
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd unified-ai-api

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/unified_ai_api --cov-report=html
```

### Project Structure

```
src/unified_ai_api/
├── __init__.py              # Public API exports
├── __main__.py             # CLI entry point
├── api_connection.py        # Main APIConnectionManager class
├── auth_keys.py            # API key management
├── compatible_client_api.py # Client implementations
├── providers_config_handlers.py # Provider configuration
├── config/                 # Configuration files
│   ├── defaults.json       # Default configuration
│   ├── providers.json      # Provider definitions
│   └── secret.json.template # Template for API keys
├── types/                  # Type definitions
└── _utils/                 # Internal utilities

examples/                   # Usage examples
├── basic_usage.py          # Simple interactive example
├── openai_example.py       # OpenAI-specific usage
├── advanced_usage.py       # Advanced features demo
└── rest_api_example.py     # REST API usage
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_api_ai.py

# With coverage
pytest --cov=src/unified_ai_api
```

## Examples

The `examples/` folder contains comprehensive usage examples:

- **`basic_usage.py`** - Interactive setup and simple chat
- **`openai_example.py`** - OpenAI-compatible API usage
- **`advanced_usage.py`** - Multi-session management and automation
- **`rest_api_example.py`** - REST API integration
- **`demo_utils.py`** - Utility functions demonstration

```bash
python examples/basic_usage.py
python examples/openai_example.py
python examples/advanced_usage.py
```

## Security

- ✅ Never commit API keys to version control
- ✅ Use environment variables in production
- ✅ `secret.json` is included in `.gitignore`
- ✅ Minimal required permissions for API keys

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Support

- 📚 **Documentation**: See this README and code examples for usage guidance
- 🐛 **Issues**: Report bugs and feature requests on GitHub
- 💬 **Examples**: Check `examples/` folder for comprehensive usage examples
- 🚀 **Quick Start**: Run `python examples/basic_usage.py` or `unified-ai-api` CLI to get started
