#!/usr/bin/env python3
"""
The Signal Cartographer: Echoes from the Void
Entry point for the game
"""

import sys
import os
import traceback

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.game_core import SignalCartographer
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print("Please ensure all required files are present.")
    sys.exit(1)

def main():
    """Main entry point for The Signal Cartographer"""
    try:
        print("=" * 60)
        print("  THE SIGNAL CARTOGRAPHER: ECHOES FROM THE VOID")
        print("=" * 60)
        print("Initializing AetherTap terminal interface...")
        print("Press Ctrl+C to exit at any time.")
        print()
        
        game = SignalCartographer()
        game.run()
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Signal lost... AetherTap shutting down.")
        print("Thank you for exploring the void.")
        print("=" * 60)
    except Exception as e:
        print(f"\nCritical system error: {e}")
        print("=" * 60)
        print("DEBUG INFORMATION:")
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
