"""Tautulli API client for user watch statistics and insights."""

from typing import Optional, List, Dict, Any
import requests


class TautulliClient:
    """Client for interacting with Tautulli API."""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize Tautulli client.
        
        Args:
            base_url: Tautulli server URL (e.g., http://localhost:8181)
            api_key: Tautulli API key
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self._session = requests.Session()
    
    def _make_request(self, cmd: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to Tautulli API.
        
        Args:
            cmd: API command
            params: Optional query parameters
            
        Returns:
            JSON response data
        """
        url = f"{self.base_url}/api/v2"
        request_params = {
            'apikey': self.api_key,
            'cmd': cmd,
        }
        if params:
            request_params.update(params)
        
        try:
            response = self._session.get(url, params=request_params)
            response.raise_for_status()
            data = response.json()
            if data.get('response', {}).get('result') == 'success':
                return data.get('response', {}).get('data', {})
            else:
                print(f"Tautulli API error: {data.get('response', {}).get('message')}")
                return {}
        except Exception as e:
            print(f"Failed to make Tautulli request: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to Tautulli.
        
        Returns:
            True if connection successful, False otherwise
        """
        result = self._make_request('arnold')
        return bool(result)
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Get all Plex users tracked by Tautulli.
        
        Returns:
            List of user dictionaries
        """
        return self._make_request('get_users') or []
    
    def get_user_watch_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Get watch statistics for a specific user.
        
        Args:
            user_id: Plex user ID
            
        Returns:
            Dictionary of watch statistics
        """
        return self._make_request('get_user_watch_time_stats', {'user_id': user_id})
    
    def get_history(
        self,
        user_id: Optional[int] = None,
        rating_key: Optional[int] = None,
        start: int = 0,
        length: int = 25
    ) -> Dict[str, Any]:
        """
        Get watch history.
        
        Args:
            user_id: Optional user ID to filter by
            rating_key: Optional Plex rating key to filter by
            start: Starting index for pagination
            length: Number of results to return
            
        Returns:
            Dictionary with history data and pagination info
        """
        params = {'start': start, 'length': length}
        if user_id:
            params['user_id'] = user_id
        if rating_key:
            params['rating_key'] = rating_key
        
        return self._make_request('get_history', params)
    
    def get_metadata(self, rating_key: int) -> Dict[str, Any]:
        """
        Get metadata for a specific item.
        
        Args:
            rating_key: Plex rating key
            
        Returns:
            Metadata dictionary
        """
        return self._make_request('get_metadata', {'rating_key': rating_key})
    
    def get_recently_watched(
        self,
        user_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recently watched items.
        
        Args:
            user_id: Optional user ID to filter by
            limit: Maximum number of items to return
            
        Returns:
            List of recently watched items
        """
        params = {'count': limit}
        if user_id:
            params['user_id'] = user_id
        
        result = self._make_request('get_recently_added', params)
        return result.get('recently_added', []) if result else []
    
    def get_watch_state(self, rating_key: int, user_id: int) -> Dict[str, Any]:
        """
        Get watch state for a specific item and user.
        
        Args:
            rating_key: Plex rating key
            user_id: Plex user ID
            
        Returns:
            Dictionary with watch state info (watched, in_progress, etc.)
        """
        history = self.get_history(user_id=user_id, rating_key=rating_key, length=1)
        if history and history.get('data'):
            last_watch = history['data'][0]
            return {
                'watched': last_watch.get('watched_status') == 1,
                'in_progress': last_watch.get('watched_status') == 0.5,
                'last_watched': last_watch.get('date'),
                'play_count': last_watch.get('play_count', 0),
            }
        return {
            'watched': False,
            'in_progress': False,
            'last_watched': None,
            'play_count': 0,
        }
