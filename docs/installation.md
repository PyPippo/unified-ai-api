# Installation Guide

This guide covers the installation and initial setup of the Unified AI API Connection package.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for development installation)

## Installation Methods

### 1. From Source (Recommended for Development)

```bash
# Clone the repository
git clone <repository-url>
cd "Unified AI API connection"

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 2. From PyPI (Coming Soon)

```bash
# Once published to PyPI
pip install unified-ai-api
```

## Verify Installation

```python
from unified_ai_api import APIConnectionManager

# Create manager instance
manager = APIConnectionManager()
print("✅ Installation successful!")

# Check available providers
providers = manager.get_available_providers()
print(f"Available providers: {providers}")
```

## Configuration Setup

### 1. API Keys Configuration

Choose one of the following methods:

#### Method A: Environment Variables (Recommended for Production)

```bash
# For OpenRouter
export OPENROUTER_API_KEY="your-openrouter-key-here"

# For OpenAI
export OPENAI_API_KEY="your-openai-key-here"

# For HuggingFace
export HUGGINGFACE_API_KEY="your-huggingface-key-here"
```

#### Method B: Configuration File (Development)

```bash
# Copy the template
cp src/unified_ai_api/config/secret.json.template src/unified_ai_api/config/secret.json

# Edit the file with your API keys
# Note: secret.json is git-ignored for security
```

### 2. Provider Configuration

The providers configuration is already included in the package at:
`src/unified_ai_api/config/providers.json`

This file defines available providers, their models, and supported API types.

## Quick Test

Run a quick test to ensure everything is working:

```bash
# Basic usage example
python examples/basic_usage.py

# Or test programmatically
python -c "
from unified_ai_api import APIConnectionManager
manager = APIConnectionManager()
print('Available providers:', manager.get_available_providers())
"
```

## Troubleshooting

### Common Issues

#### 1. Import Error

```
ModuleNotFoundError: No module named 'unified_ai_api'
```

**Solution**: Ensure you installed the package with `pip install -e .`

#### 2. No Providers Found

```
❌ No providers found in configuration.
```

**Solution**: Check that `src/unified_ai_api/config/providers.json` exists

#### 3. Missing API Keys

```
❌ No valid API key found for provider 'OPENAI'
```

**Solution**: Configure your API keys using environment variables or secret.json

#### 4. Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Solution**: Use virtual environment or `--user` flag: `pip install --user -e .`

### Virtual Environment Setup

For a clean installation:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate

# Install package
pip install -e .
```

## Development Dependencies

For development work, install additional dependencies:

```bash
pip install -e ".[dev]"
```

This includes:

- pytest (testing framework)
- pytest-cov (coverage reporting)
- Additional development tools

## CLI Access

After installation, you can use the command-line interface:

```bash
# If main entry point is configured
unified-ai-api

# Or run as module
python -m unified_ai_api
```

## Next Steps

1. [Quick Start Guide](quickstart.md) - Get up and running in minutes
2. [Basic Usage](user_guide/basic_usage.md) - Learn essential concepts
3. [Examples](examples.md) - See practical usage examples

---

*Need help? Check the [error handling guide](user_guide/error_handling.md) or review the [examples](../examples/).*
