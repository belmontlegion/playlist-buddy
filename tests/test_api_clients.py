"""Tests for API clients."""

import pytest
from unittest.mock import Mock, patch
from src.api.plex_client import PlexClient
from src.api.tautulli_client import TautulliClient
from src.api.tmdb_client import TMDBClient


class TestPlexClient:
    """Tests for Plex API client."""
    
    @patch('src.api.plex_client.PlexServer')
    def test_connect_success(self, mock_server):
        """Test successful Plex connection."""
        client = PlexClient('http://localhost:32400', 'test_token')
        result = client.connect()
        
        assert result is True
        mock_server.assert_called_once_with('http://localhost:32400', 'test_token')
    
    @patch('src.api.plex_client.PlexServer')
    def test_connect_failure(self, mock_server):
        """Test failed Plex connection."""
        mock_server.side_effect = Exception("Connection failed")
        
        client = PlexClient('http://localhost:32400', 'test_token')
        result = client.connect()
        
        assert result is False


class TestTautulliClient:
    """Tests for Tautulli API client."""
    
    def test_make_request_success(self):
        """Test successful API request."""
        client = TautulliClient('http://localhost:8181', 'test_key')
        
        with patch.object(client._session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'response': {
                    'result': 'success',
                    'data': {'test': 'data'}
                }
            }
            mock_get.return_value = mock_response
            
            result = client._make_request('test_cmd')
            
            assert result == {'test': 'data'}
    
    def test_test_connection(self):
        """Test connection test method."""
        client = TautulliClient('http://localhost:8181', 'test_key')
        
        with patch.object(client, '_make_request') as mock_request:
            mock_request.return_value = {'success': True}
            
            result = client.test_connection()
            
            assert result is True
            mock_request.assert_called_once_with('arnold')


class TestTMDBClient:
    """Tests for TMDB API client."""
    
    def test_search_tv_show(self):
        """Test TV show search."""
        client = TMDBClient('test_api_key')
        
        with patch.object(client._session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'results': [
                    {'id': 1, 'name': 'Test Show'}
                ]
            }
            mock_get.return_value = mock_response
            
            results = client.search_tv_show('Test Show')
            
            assert len(results) == 1
            assert results[0]['name'] == 'Test Show'
    
    def test_get_image_url(self):
        """Test image URL generation."""
        client = TMDBClient('test_api_key')
        
        url = client.get_image_url('/abc123.jpg', 'w500')
        
        assert url == 'https://image.tmdb.org/t/p/w500/abc123.jpg'
    
    def test_cache(self):
        """Test response caching."""
        client = TMDBClient('test_api_key')
        
        with patch.object(client._session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {'id': 1}
            mock_get.return_value = mock_response
            
            # First call should hit the API
            result1 = client.get_tv_show(1)
            assert mock_get.call_count == 1
            
            # Second call should use cache
            result2 = client.get_tv_show(1)
            assert mock_get.call_count == 1  # Still 1, not 2
            
            assert result1 == result2
