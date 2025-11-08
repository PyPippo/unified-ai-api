"""
Entry point for running unified_ai_api as a module: python -m unified_ai_api
"""

import sys
from typing import Optional

def main() -> Optional[int]:
    """Main entry point for the unified-ai-api CLI."""
    try:
        # Import here to avoid circular imports
        from unified_ai_api.api_connection import APIConnectionManager
        
        print('🤖 Unified AI API Connection Manager')
        print('=' * 40)
        print('Welcome! This will guide you through setting up your AI connection.\n')
        
        # Initialize the API connection manager
        api_manager = APIConnectionManager()
        
        # Start interactive setup
        if api_manager.interactive_setup():
            print('\n🚀 Starting chat session...')
            api_manager.start_chat_loop()
        else:
            print('\n❌ Setup failed. Please check your configuration and try again.')
            return 1
            
        return 0
        
    except KeyboardInterrupt:
        print('\n\n✅ Thanks for using Unified AI API! Goodbye!')
        return 0
    except Exception as e:
        print(f'\n❌ Error: {e}')
        print('\n🔧 Troubleshooting:')
        print('1. Check your API key configuration')
        print('2. Verify configuration files in src/unified_ai_api/config/')
        print('3. Make sure dependencies are installed')
        return 1

if __name__ == '__main__':
    sys.exit(main() or 0)