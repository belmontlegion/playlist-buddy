# Development Guide

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/belmontlegion/playlist-buddy.git
   cd playlist-buddy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python -m src.main
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_credential_store.py
```

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Check code style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Project Structure

```
playlist-buddy/
├── src/
│   ├── api/              # API client modules
│   │   ├── plex_client.py
│   │   ├── tautulli_client.py
│   │   └── tmdb_client.py
│   ├── models/           # Data models
│   │   └── media.py
│   ├── ui/               # User interface
│   │   └── main_window.py
│   ├── utils/            # Utilities
│   │   ├── config.py
│   │   ├── credential_store.py
│   │   └── image_cache.py
│   └── main.py           # Entry point
├── tests/                # Test suite
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project metadata
└── README.md             # Main readme
```

## Configuration

The application stores configuration in `~/.playlist_buddy/`:
- `config.json` - User preferences
- `credentials.enc` - Encrypted API credentials
- `cache/` - Cached images and metadata

## First Run Setup

1. **Launch the application**
2. **Connect to Plex**: File → Connect to Plex...
   - Enter your Plex server URL (e.g., `http://localhost:32400`)
   - Enter your Plex authentication token
3. **Connect to Tautulli** (optional): Edit → Preferences...
   - Enter your Tautulli URL (e.g., `http://localhost:8181`)
   - Enter your Tautulli API key
4. **Add TMDB API Key** (optional for enhanced artwork)
   - Get a free API key from https://www.themoviedb.org/
   - Add it in Edit → Preferences...

## Getting API Credentials

### Plex Token
1. Log into Plex Web App
2. Open any media item
3. Click "Get Info" or "View XML"
4. Look for `X-Plex-Token` in the URL

Or use this XML method:
1. Go to: `http://YOUR_PLEX_IP:32400/library/sections?X-Plex-Token=`
2. Sign in when prompted
3. Copy the token from the URL

### Tautulli API Key
1. Open Tautulli web interface
2. Go to Settings → Web Interface
3. Find "API Key" section
4. Click "Show API Key"

### TMDB API Key
1. Create account at https://www.themoviedb.org/
2. Go to Settings → API
3. Request an API key (choose "Developer")
4. Fill out the form
5. Copy your API key (v3 auth)

## Development Roadmap

See [tautulli_powered_playlist_builder_high_level_vision.md](tautulli_powered_playlist_builder_high_level_vision.md) for the complete roadmap.

### Current Status: MVP Phase

- [x] Project structure
- [x] API client foundations
- [x] Secure credential storage
- [x] Basic UI framework
- [ ] Library browser with tree view
- [ ] Tri-state selection system
- [ ] Playlist builder panel
- [ ] Static playlist creation
- [ ] Dry-run preview

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](LICENSE) file for details
