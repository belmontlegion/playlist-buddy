"""Secure credential storage using encryption."""

import os
import json
from pathlib import Path
from typing import Optional, Dict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64


class CredentialStore:
    """Secure storage for API credentials."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize credential store.
        
        Args:
            config_dir: Directory for storing credentials. Defaults to user config dir.
        """
        if config_dir is None:
            config_dir = Path.home() / '.playlist_buddy'
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.creds_file = self.config_dir / 'credentials.enc'
        self.key_file = self.config_dir / '.key'
        
        self._cipher: Optional[Fernet] = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize or load encryption key."""
        if self.key_file.exists():
            # Load existing key
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Secure the key file (platform-specific)
            try:
                os.chmod(self.key_file, 0o600)
            except Exception:
                pass  # May fail on Windows
        
        self._cipher = Fernet(key)
    
    def save_credentials(self, credentials: Dict[str, str]):
        """
        Save credentials securely.
        
        Args:
            credentials: Dictionary of credential key-value pairs
        """
        if not self._cipher:
            raise RuntimeError("Encryption not initialized")
        
        # Serialize to JSON
        json_data = json.dumps(credentials)
        
        # Encrypt
        encrypted_data = self._cipher.encrypt(json_data.encode('utf-8'))
        
        # Save to file
        with open(self.creds_file, 'wb') as f:
            f.write(encrypted_data)
    
    def load_credentials(self) -> Dict[str, str]:
        """
        Load credentials from secure storage.
        
        Returns:
            Dictionary of credentials
        """
        if not self.creds_file.exists():
            return {}
        
        if not self._cipher:
            raise RuntimeError("Encryption not initialized")
        
        # Read encrypted data
        with open(self.creds_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt
        try:
            json_data = self._cipher.decrypt(encrypted_data).decode('utf-8')
            return json.loads(json_data)
        except Exception as e:
            print(f"Failed to decrypt credentials: {e}")
            return {}
    
    def update_credential(self, key: str, value: str):
        """
        Update a single credential.
        
        Args:
            key: Credential key
            value: Credential value
        """
        credentials = self.load_credentials()
        credentials[key] = value
        self.save_credentials(credentials)
    
    def get_credential(self, key: str) -> Optional[str]:
        """
        Get a single credential value.
        
        Args:
            key: Credential key
            
        Returns:
            Credential value or None if not found
        """
        credentials = self.load_credentials()
        return credentials.get(key)
    
    def delete_credential(self, key: str):
        """
        Delete a credential.
        
        Args:
            key: Credential key to delete
        """
        credentials = self.load_credentials()
        if key in credentials:
            del credentials[key]
            self.save_credentials(credentials)
    
    def clear_all(self):
        """Clear all stored credentials."""
        if self.creds_file.exists():
            self.creds_file.unlink()
