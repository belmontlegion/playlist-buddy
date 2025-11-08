"""Configuration management for the application."""

from pathlib import Path
from typing import Optional
import json


class Config:
    """Application configuration."""
    
    DEFAULT_CONFIG = {
        'window': {
            'width': 1400,
            'height': 900,
            'remember_position': True,
        },
        'cache': {
            'max_size_mb': 500,
            'ttl_hours': 24,
        },
        'ui': {
            'theme': 'system',  # system, light, dark
            'large_thumbnails': False,
            'show_runtime_warnings': True,
        },
        'api': {
            'request_timeout': 30,
            'max_retries': 3,
            'enable_tmdb': True,
        },
        'defaults': {
            'runtime_cap_minutes': 120,
            'max_playlist_items': 100,
        }
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration.
        
        Args:
            config_dir: Directory for config file. Defaults to user config dir.
        """
        if config_dir is None:
            config_dir = Path.home() / '.playlist_buddy'
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self._config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults to add any new keys
                return self._merge_dicts(self.DEFAULT_CONFIG.copy(), loaded)
            except Exception as e:
                print(f"Failed to load config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG.copy())
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_dicts(self, base: dict, override: dict) -> dict:
        """Recursively merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_config(self, config: Optional[dict] = None):
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save. If None, saves current config.
        """
        if config is None:
            config = self._config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def get(self, key: str, default=None):
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'window.width')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value):
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'window.width')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save_config()
