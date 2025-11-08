# Playlist Buddy

A robust desktop GUI tool for creating and managing Plex playlists using Tautulli insights and the Plex API.

## Features

- **User-Centric Insights**: Leverage Tautulli for play counts, watch states, recency, and ratings
- **Intuitive Tree View**: Browse shows, seasons, and episodes with tri-state checkboxes
- **Smart Playlists**: Create rule-based playlists that auto-refresh
- **Static Playlists**: Build custom playlists with full control
- **Advanced Filtering**: Search and filter by unwatched status, duration, genre, year, quality, and more
- **TMDB Enrichment**: Enhanced artwork and metadata integration
- **Safe Operations**: Dry-run previews before committing changes
- **Performance**: Optimized for large libraries with virtualized lists and local caching

## Installation

```bash
# Clone the repository
git clone https://github.com/belmontlegion/playlist-buddy.git
cd playlist-buddy

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
```

## Requirements

- Python 3.10+
- Plex Media Server with API access
- Tautulli installation
- TMDB API key (optional, for enhanced artwork)

## Development Status

Currently in active development. See the [roadmap](tautulli_powered_playlist_builder_high_level_vision.md) for planned features.

## License

MIT License - See LICENSE file for details

## Author

Scott McKay (@belmontlegion)
