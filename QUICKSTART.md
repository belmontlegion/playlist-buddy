# Quick Start Guide

## Running the Application

### Option 1: Using Python directly
```bash
python -m src.main
```

### Option 2: Using the run script
```bash
python run.py
```

## First Time Setup

When you first run the application:

1. **The application will launch** with the main window
2. **Click "Connect" or File → Connect to Plex...**
3. **Enter your Plex credentials:**
   - Server URL (e.g., `http://192.168.1.100:32400`)
   - Auth Token (see below for how to get this)
4. **Optionally add Tautulli and TMDB:**
   - Switch to Tautulli tab and enter URL + API key
   - Switch to TMDB tab and enter API key
5. **Click "Test Connection"** to verify
6. **Click "Save & Connect"**

## Getting Your Plex Token

### Method 1: Via XML
1. Open your Plex Web App
2. Navigate to any media item
3. Click the three dots (...) → "Get Info"
4. In the URL, look for `X-Plex-Token=XXXXX`

### Method 2: Via Account
1. Go to https://www.plex.tv/
2. Sign in to your account
3. Click your profile picture → Account
4. At the bottom, you'll see your token

### Method 3: Using Plex Web Inspector
1. Open Plex Web App
2. Press F12 to open Developer Tools
3. Go to the Network tab
4. Refresh the page
5. Look for any request and check the `X-Plex-Token` header

## Getting Your Tautulli API Key

1. Open Tautulli web interface
2. Go to **Settings** (gear icon)
3. Click **Web Interface** in the left sidebar
4. Scroll to the **API** section
5. Click **Show API Key**
6. Copy the key

## Getting Your TMDB API Key

1. Create a free account at https://www.themoviedb.org/
2. Go to **Settings** → **API**
3. Click **Request an API Key**
4. Choose **Developer**
5. Fill out the required form
6. Copy your **API Key (v3 auth)**

## Using the Application

### Browsing Your Library

1. **Select a library** from the dropdown at the top
2. **Shows will load** in the tree view
3. **Click the arrow** next to a show to expand seasons
4. **Click the arrow** next to a season to expand episodes

### Selecting Episodes

- **Click the checkbox** next to any show/season/episode
- **Checking a show** selects all seasons and episodes
- **Checking a season** selects all episodes in that season
- **Partial checks** (gray checkboxes) indicate some children are selected

### Keyboard Shortcuts

- `Ctrl+O` - Open connection dialog
- `F5` - Refresh current library
- `Ctrl+N` - New playlist (coming soon)
- `Ctrl+Q` - Quit application

## Troubleshooting

### "Could not connect to Plex server"
- Check that your Plex server URL is correct
- Verify the token hasn't expired
- Ensure the server is running and accessible
- Try accessing the URL in your browser

### "Import PyQt6 could not be resolved"
```bash
pip install PyQt6
```

### Application won't start
```bash
# Reinstall all dependencies
pip install -r requirements.txt
```

### Credentials not saving
- Check that `~/.playlist_buddy/` directory exists
- Verify you have write permissions
- On Windows: `C:\Users\YourName\.playlist_buddy\`
- On macOS/Linux: `~/.playlist_buddy/`

## Development Mode

To run in development with debugging:

```bash
# Enable Python warnings
python -Wd -m src.main

# Or with the run script
python -Wd run.py
```

## Next Steps

Once connected and browsing your library, you'll be able to:

- [x] Browse all your TV shows
- [x] Expand shows to view seasons
- [x] Expand seasons to view episodes
- [x] Select episodes using checkboxes
- [ ] Create static playlists (coming soon)
- [ ] Filter by watch state (coming soon)
- [ ] Use templates (coming soon)
- [ ] Create smart playlists (coming soon)

Check the [GitHub Issues](https://github.com/belmontlegion/playlist-buddy/issues) for current development status.
