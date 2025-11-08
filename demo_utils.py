'''
Example demonstrating the refactored _utils functionality.

This shows how to use the configuration loaders and data extraction utilities.
Configuration loading now handles type validation internally, while
data extraction utilities work with already-typed structures.
'''

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from unified_ai_api._utils import (
    load_providers_file,
    filter_providers_by_api_type,
    extract_supported_apis,
    validate_provider_config_fields,
)
from unified_ai_api.types import ProvidersConfigParams


def demonstrate_utils():
    '''Demonstrate the refactored utilities functionality.'''
    print('=== Configuration Loading and Data Extraction Demo ===')

    try:
        # Load typed configuration (validation happens internally)
        print('1. Loading typed providers configuration...')
        providers_config = load_providers_file()
        print(f'   ✅ Loaded {len(providers_config)} providers')

        # Get first provider's first config (already typed)
        provider_name = list(providers_config.keys())[0]
        first_config = providers_config[provider_name][0]
        print(f'   📄 Example provider: {provider_name}')
        print(f'   📄 Config keys: {list(first_config.keys())}')

        # Validate configuration structure (works with typed data)
        print('\n2. Validating configuration fields...')
        is_valid = validate_provider_config_fields(first_config)
        print(f'   ✅ Configuration valid: {is_valid}')

        # Demonstrate data extraction utilities
        print('\n3. Data extraction examples...')

        # Extract all supported APIs
        supported_apis = extract_supported_apis(providers_config)
        print(f'   🔧 All supported APIs: {supported_apis}')

        # Filter by API type
        if 'openai' in supported_apis:
            openai_providers = filter_providers_by_api_type(providers_config, 'openai')
            print(f'   🔍 OpenAI-compatible providers: {list(openai_providers.keys())}')

        # Show typed config details
        print('\n4. Typed configuration details...')
        typed_config: ProvidersConfigParams = first_config
        print(f'   📋 Model: {typed_config["model_name"]}')
        print(f'   🔗 URL: {typed_config["model_url"]}')
        print(f'   📁 Config Name: {typed_config["config_name"]}')
        print(f'   📡 Supported APIs: {typed_config["api_supported"]}')

        print('\n✅ All refactored utilities working correctly!')

    except Exception as e:
        print(f'❌ Error: {e}')
        return False

    return True


if __name__ == '__main__':
    demonstrate_utils()
