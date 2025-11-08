# Playlist Buddy

[![GitHub issues](https://img.shields.io/github/issues/belmontlegion/playlist-buddy)](https://github.com/belmontlegion/playlist-buddy/issues)
[![GitHub stars](https://img.shields.io/github/stars/belmontlegion/playlist-buddy)](https://github.com/belmontlegion/playlist-buddy/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust desktop GUI tool for creating and managing Plex playlists using Tautulli insights and the Plex API.

## 🎯 Overview

Playlist Buddy makes it easy to curate the perfect viewing experience by combining the power of Plex, Tautulli user statistics, and TMDB metadata. Browse your entire library in an intuitive tree view, filter by watch states, and create both static and smart playlists with just a few clicks.

## ✨ Features

- **User-Centric Insights**: Leverage Tautulli for play counts, watch states, recency, and ratings
- **Intuitive Tree View**: Browse shows, seasons, and episodes with tri-state checkboxes
- **Smart Playlists**: Create rule-based playlists that auto-refresh (coming soon)
- **Static Playlists**: Build custom playlists with full control
- **Advanced Filtering**: Search and filter by unwatched status, duration, genre, year, quality, and more
- **TMDB Enrichment**: Enhanced artwork and metadata integration
- **Safe Operations**: Dry-run previews before committing changes
- **Performance**: Optimized for large libraries with virtualized lists and local caching
- **Secure**: All API credentials encrypted at rest

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Plex Media Server with API access
- Tautulli installation (for user statistics)
- TMDB API key (optional, for enhanced artwork)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/belmontlegion/playlist-buddy.git
   cd playlist-buddy
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (CMD)
   .\venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m src.main
   ```

### First-Time Setup

1. **Connect to Plex**
   - File → Connect to Plex...
   - Enter your Plex server URL (e.g., `http://localhost:32400`)
   - Enter your Plex authentication token ([How to find](DEVELOPMENT.md#plex-token))

2. **Connect to Tautulli** (optional but recommended)
   - Edit → Preferences...
   - Enter Tautulli URL (e.g., `http://localhost:8181`)
   - Enter Tautulli API key ([How to find](DEVELOPMENT.md#tautulli-api-key))

3. **Add TMDB API Key** (optional)
   - Get a free key at [themoviedb.org](https://www.themoviedb.org/)
   - Add in Edit → Preferences...

## 📋 Current Status

**Development Phase**: MVP (Minimum Viable Product)

This project is in active development. Core API clients and architecture are complete. Currently implementing the GUI components and playlist creation features.

See [Issue #1](https://github.com/belmontlegion/playlist-buddy/issues/1) for MVP progress tracking.

### Completed ✅
- Project structure and architecture
- API clients (Plex, Tautulli, TMDB)
- Secure credential storage
- Image caching system
- Basic GUI framework
- Data models
- **Library tree view with tri-state selection**
- **Connection dialog for easy setup**
- **Playlist builder panel with runtime meter**
- **Deduplication and ordering**

### In Progress 🚧
- User-aware filtering (watch states from Tautulli)
- Dry-run preview improvements
- Episode metadata display

### Planned 📅
- Templates (Catch-Up Tonight, Season Sampler, etc.)
- Smart playlists with rule builder
- Export/import functionality
- Advanced search and filtering

See the complete [roadmap](tautulli_powered_playlist_builder_high_level_vision.md) for details.

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

- Report bugs via [Issues](https://github.com/belmontlegion/playlist-buddy/issues)
- Suggest features using the Feature Request template
- Submit pull requests for bug fixes or features

## 📖 Documentation

- [Development Guide](DEVELOPMENT.md) - Setup and development workflow
- [Vision Document](tautulli_powered_playlist_builder_high_level_vision.md) - Complete feature roadmap
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Scott McKay** ([@belmontlegion](https://github.com/belmontlegion))

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Uses [PlexAPI](https://github.com/pkkid/python-plexapi) for Plex integration
- Powered by [TMDB](https://www.themoviedb.org/) for metadata enrichment

---

⭐ If you find this project useful, please consider giving it a star!
