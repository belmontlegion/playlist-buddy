"""Plex API client for library access and playlist management."""

from typing import Optional, List, Dict, Any
from plexapi.server import PlexServer
from plexapi.playlist import Playlist
from plexapi.video import Show, Season, Episode


class PlexClient:
    """Client for interacting with Plex Media Server."""
    
    def __init__(self, base_url: str, token: str):
        """
        Initialize Plex client.
        
        Args:
            base_url: Plex server URL (e.g., http://localhost:32400)
            token: Plex authentication token
        """
        self.base_url = base_url
        self.token = token
        self._server: Optional[PlexServer] = None
    
    def connect(self) -> bool:
        """
        Connect to Plex server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._server = PlexServer(self.base_url, self.token)
            return True
        except Exception as e:
            print(f"Failed to connect to Plex: {e}")
            return False
    
    @property
    def server(self) -> PlexServer:
        """Get the Plex server instance."""
        if not self._server:
            raise RuntimeError("Not connected to Plex server. Call connect() first.")
        return self._server
    
    def get_libraries(self) -> List[Dict[str, Any]]:
        """
        Get all TV show libraries.
        
        Returns:
            List of library dictionaries with id, title, and type
        """
        libraries = []
        for section in self.server.library.sections():
            if section.type == 'show':
                libraries.append({
                    'id': section.key,
                    'title': section.title,
                    'type': section.type,
                })
        return libraries
    
    def get_shows(self, library_id: Optional[str] = None) -> List[Show]:
        """
        Get all shows from a library.
        
        Args:
            library_id: Library section ID. If None, gets shows from all libraries.
            
        Returns:
            List of Show objects
        """
        if library_id:
            section = self.server.library.sectionByID(library_id)
            return section.all()
        else:
            shows = []
            for section in self.server.library.sections():
                if section.type == 'show':
                    shows.extend(section.all())
            return shows
    
    def get_seasons(self, show: Show) -> List[Season]:
        """
        Get all seasons for a show.
        
        Args:
            show: Show object
            
        Returns:
            List of Season objects
        """
        return show.seasons()
    
    def get_episodes(self, season: Season) -> List[Episode]:
        """
        Get all episodes for a season.
        
        Args:
            season: Season object
            
        Returns:
            List of Episode objects
        """
        return season.episodes()
    
    def create_playlist(self, name: str, items: List[Episode]) -> Optional[Playlist]:
        """
        Create a new playlist.
        
        Args:
            name: Playlist name
            items: List of Episode objects to include
            
        Returns:
            Created Playlist object or None on failure
        """
        try:
            return self.server.createPlaylist(name, items=items)
        except Exception as e:
            print(f"Failed to create playlist: {e}")
            return None
    
    def update_playlist(self, playlist: Playlist, items: List[Episode]) -> bool:
        """
        Update an existing playlist with new items.
        
        Args:
            playlist: Playlist object to update
            items: New list of Episode objects
            
        Returns:
            True if successful, False otherwise
        """
        try:
            playlist.removeItems(playlist.items())
            playlist.addItems(items)
            return True
        except Exception as e:
            print(f"Failed to update playlist: {e}")
            return False
    
    def get_playlists(self) -> List[Playlist]:
        """
        Get all playlists on the server.
        
        Returns:
            List of Playlist objects
        """
        return self.server.playlists()
    
    def search(self, query: str, library_id: Optional[str] = None) -> List[Any]:
        """
        Search for content in the library.
        
        Args:
            query: Search query string
            library_id: Optional library ID to limit search scope
            
        Returns:
            List of matching items
        """
        if library_id:
            section = self.server.library.sectionByID(library_id)
            return section.search(query)
        else:
            return self.server.library.search(query)
