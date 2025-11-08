"""Quick start script for testing the application."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import main

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Playlist Buddy...")
    print("=" * 60)
    print("\nNote: PyQt6 must be installed for the GUI to work.")
    print("Install with: pip install -r requirements.txt\n")
    print("=" * 60)
    
    main()
