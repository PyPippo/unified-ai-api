# Examples

This folder contains comprehensive usage examples for the Unified AI API connection library.

## Running Examples

From the project root directory:

```bash
# Basic interactive usage
python examples/basic_usage.py

# OpenAI-compatible API demonstration
python examples/openai_example.py

# Advanced features and multi-session management
python examples/advanced_usage.py

# REST API integration
python examples/rest_api_example.py

# Utility functions demonstration
python examples/demo_utils.py
```

## Example Descriptions

### `basic_usage.py`

- Interactive provider selection
- Simple chat interface
- Basic error handling
- Good starting point for new users

### `openai_example.py`

- Direct OpenAI-compatible API usage
- Programmatic configuration
- Conversation management
- Chat history handling

### `advanced_usage.py`

- Multi-session management
- Automated batch processing
- Comprehensive error handling
- Multiple configuration methods

### `rest_api_example.py`

- Generic REST API integration
- Custom timeout configuration
- Different API scenarios
- Connection parameter demonstration

### `demo_utils.py`

- Configuration loading utilities
- Data extraction functions
- Type validation examples
- Internal API demonstration

## Prerequisites

Make sure you have:

1. API keys configured (see main README.md)
2. Dependencies installed: `pip install -e .`
3. Configuration files set up in `src/unified_ai_api/config/`

## Configuration

Examples will guide you through setup, but you can also:

- Set environment variables: `OPENROUTER_API_KEY`, `HUGGINGFACE_API_KEY`
- Configure `src/unified_ai_api/config/secret.json`

## Getting Help

If examples don't work:

1. Check your API key configuration
2. Verify network connectivity
3. Review the troubleshooting sections in each example
4. See the main project documentation in `docs/`
