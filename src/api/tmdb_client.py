"""TMDB API client for enhanced metadata and artwork."""

from typing import Optional, List, Dict, Any
import requests
from datetime import datetime, timedelta


class TMDBClient:
    """Client for interacting with The Movie Database (TMDB) API."""
    
    def __init__(self, api_key: str):
        """
        Initialize TMDB client.
        
        Args:
            api_key: TMDB API key
        """
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self._session = requests.Session()
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._cache_ttl = timedelta(hours=24)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to TMDB API with caching.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response data
        """
        # Check cache first
        cache_key = f"{endpoint}:{str(params)}"
        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_ttl:
                return cached_data
        
        url = f"{self.base_url}/{endpoint}"
        request_params = {'api_key': self.api_key}
        if params:
            request_params.update(params)
        
        try:
            response = self._session.get(url, params=request_params)
            response.raise_for_status()
            data = response.json()
            
            # Cache the result
            self._cache[cache_key] = (data, datetime.now())
            
            return data
        except Exception as e:
            print(f"Failed to make TMDB request: {e}")
            return {}
    
    def search_tv_show(self, query: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for TV shows by name.
        
        Args:
            query: Show name to search for
            year: Optional year to narrow results
            
        Returns:
            List of matching TV shows
        """
        params = {'query': query}
        if year:
            params['first_air_date_year'] = year
        
        result = self._make_request('search/tv', params)
        return result.get('results', [])
    
    def get_tv_show(self, tmdb_id: int) -> Dict[str, Any]:
        """
        Get detailed TV show information.
        
        Args:
            tmdb_id: TMDB TV show ID
            
        Returns:
            TV show details
        """
        return self._make_request(f'tv/{tmdb_id}')
    
    def get_season(self, tmdb_id: int, season_number: int) -> Dict[str, Any]:
        """
        Get season details.
        
        Args:
            tmdb_id: TMDB TV show ID
            season_number: Season number
            
        Returns:
            Season details including episodes
        """
        return self._make_request(f'tv/{tmdb_id}/season/{season_number}')
    
    def get_episode(self, tmdb_id: int, season_number: int, episode_number: int) -> Dict[str, Any]:
        """
        Get episode details.
        
        Args:
            tmdb_id: TMDB TV show ID
            season_number: Season number
            episode_number: Episode number
            
        Returns:
            Episode details
        """
        return self._make_request(
            f'tv/{tmdb_id}/season/{season_number}/episode/{episode_number}'
        )
    
    def get_keywords(self, tmdb_id: int) -> List[Dict[str, Any]]:
        """
        Get keywords/tags for a TV show.
        
        Args:
            tmdb_id: TMDB TV show ID
            
        Returns:
            List of keywords
        """
        result = self._make_request(f'tv/{tmdb_id}/keywords')
        return result.get('results', [])
    
    def get_image_url(self, path: str, size: str = 'original') -> str:
        """
        Get full URL for an image path.
        
        Args:
            path: Image path from TMDB (e.g., /abc123.jpg)
            size: Image size (w500, original, etc.)
            
        Returns:
            Full image URL
        """
        if not path:
            return ""
        return f"https://image.tmdb.org/t/p/{size}{path}"
    
    def find_by_external_id(self, external_id: str, source: str = 'tvdb_id') -> Dict[str, Any]:
        """
        Find a TV show by external ID (TVDB, IMDB, etc.).
        
        Args:
            external_id: External ID value
            source: ID source (tvdb_id, imdb_id, etc.)
            
        Returns:
            TV show results
        """
        return self._make_request(f'find/{external_id}', {'external_source': source})
    
    def clear_cache(self):
        """Clear the internal cache."""
        self._cache.clear()
