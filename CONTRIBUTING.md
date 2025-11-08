# Contributing to Playlist Buddy

Thank you for your interest in contributing to Playlist Buddy! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project and community

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/belmontlegion/playlist-buddy/issues)
2. Use the Bug Report template
3. Include detailed steps to reproduce
4. Add relevant logs and screenshots
5. Specify your environment (OS, Python version, Plex version, etc.)

### Suggesting Features

1. Check the [roadmap](tautulli_powered_playlist_builder_high_level_vision.md) first
2. Search existing feature requests
3. Use the Feature Request template
4. Explain the use case and benefits
5. Consider implementation complexity

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/playlist-buddy.git
   cd playlist-buddy
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Write clear, documented code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   black src/ tests/
   flake8 src/ tests/
   
   # Type checking
   mypy src/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Test:` for test additions/changes
   - `Refactor:` for code refactoring

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the [original repository](https://github.com/belmontlegion/playlist-buddy)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template
   - Link related issues

### Code Style Guidelines

- **Python**: Follow PEP 8
- **Line length**: 100 characters (configured in Black)
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use type hints where practical
- **Imports**: Group stdlib, third-party, and local imports

Example:
```python
"""Module description."""

from typing import Optional, List
from pathlib import Path

from PyQt6.QtWidgets import QWidget

from src.models.media import MediaNode


class MyClass:
    """Class description.
    
    Attributes:
        attribute_name: Description of attribute
    """
    
    def my_method(self, param: str) -> Optional[int]:
        """
        Method description.
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
        """
        pass
```

### Testing Guidelines

- Write unit tests for new functionality
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use meaningful test names: `test_<what>_<condition>_<expected>`

Example:
```python
def test_playlist_creation_with_valid_episodes_succeeds():
    """Test that playlist is created successfully with valid episodes."""
    # Arrange
    client = PlexClient(url, token)
    episodes = [episode1, episode2]
    
    # Act
    playlist = client.create_playlist("Test", episodes)
    
    # Assert
    assert playlist is not None
    assert playlist.title == "Test"
```

### Documentation

- Update README.md for user-facing changes
- Update DEVELOPMENT.md for developer-facing changes
- Add docstrings to all public functions/classes
- Update CHANGELOG.md

## Development Workflow

1. **MVP Phase** (Current): Core functionality
   - Library browsing
   - Static playlists
   - Basic filtering

2. **Beta Phase**: Enhanced features
   - Templates
   - Search improvements
   - Export/import

3. **v1.0**: Full feature set
   - Smart playlists
   - Multi-user support
   - Advanced options

See the [roadmap](tautulli_powered_playlist_builder_high_level_vision.md) for details.

## Questions?

- Open a [Discussion](https://github.com/belmontlegion/playlist-buddy/discussions)
- Comment on related issues
- Check the [DEVELOPMENT.md](DEVELOPMENT.md) guide

Thank you for contributing! 🎉
