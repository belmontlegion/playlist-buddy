"""Tests for credential storage."""

import pytest
from pathlib import Path
import tempfile
import shutil
from src.utils.credential_store import CredentialStore


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp = Path(tempfile.mkdtemp())
    yield temp
    shutil.rmtree(temp)


def test_save_and_load_credentials(temp_dir):
    """Test saving and loading credentials."""
    store = CredentialStore(temp_dir)
    
    credentials = {
        'plex_url': 'http://localhost:32400',
        'plex_token': 'test_token_123',
        'tautulli_url': 'http://localhost:8181',
        'tautulli_api_key': 'test_api_key',
    }
    
    store.save_credentials(credentials)
    loaded = store.load_credentials()
    
    assert loaded == credentials


def test_update_credential(temp_dir):
    """Test updating a single credential."""
    store = CredentialStore(temp_dir)
    
    store.update_credential('plex_token', 'token1')
    assert store.get_credential('plex_token') == 'token1'
    
    store.update_credential('plex_token', 'token2')
    assert store.get_credential('plex_token') == 'token2'


def test_delete_credential(temp_dir):
    """Test deleting a credential."""
    store = CredentialStore(temp_dir)
    
    store.update_credential('test_key', 'test_value')
    assert store.get_credential('test_key') == 'test_value'
    
    store.delete_credential('test_key')
    assert store.get_credential('test_key') is None


def test_clear_all(temp_dir):
    """Test clearing all credentials."""
    store = CredentialStore(temp_dir)
    
    credentials = {
        'key1': 'value1',
        'key2': 'value2',
    }
    store.save_credentials(credentials)
    
    store.clear_all()
    loaded = store.load_credentials()
    
    assert loaded == {}


def test_encryption_persistence(temp_dir):
    """Test that encryption key persists across instances."""
    store1 = CredentialStore(temp_dir)
    store1.update_credential('test', 'value')
    
    store2 = CredentialStore(temp_dir)
    assert store2.get_credential('test') == 'value'
