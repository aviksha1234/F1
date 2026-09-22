"""Main entry point for F1 Pit Stop Master."""
import sys
import os

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    """Launches F1 Pit Stop Master."""
    print("=======================================================")
    print(" 🏎️  F1 PIT STOP MASTER — 'EVERY SECOND COUNTS.'")
    print("=======================================================")
    print("Initializing engine and motorsport simulation...")

    try:
        from game.game import Game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame session ended by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected exception occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
