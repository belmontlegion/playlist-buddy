"""Connection dialog for Plex and Tautulli setup."""

from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTabWidget, QWidget,
    QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt

from src.utils.credential_store import CredentialStore
from src.api.plex_client import PlexClient
from src.api.tautulli_client import TautulliClient
from src.api.tmdb_client import TMDBClient


class ConnectionDialog(QDialog):
    """Dialog for configuring API connections."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Services")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self.credential_store = CredentialStore()
        self.plex_client: Optional[PlexClient] = None
        self.tautulli_client: Optional[TautulliClient] = None
        self.tmdb_client: Optional[TMDBClient] = None
        
        self._setup_ui()
        self._load_saved_credentials()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Tab widget for different services
        tabs = QTabWidget()
        
        # Plex tab
        plex_tab = self._create_plex_tab()
        tabs.addTab(plex_tab, "Plex")
        
        # Tautulli tab
        tautulli_tab = self._create_tautulli_tab()
        tabs.addTab(tautulli_tab, "Tautulli")
        
        # TMDB tab
        tmdb_tab = self._create_tmdb_tab()
        tabs.addTab(tmdb_tab, "TMDB")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self._test_connection)
        button_layout.addWidget(test_button)
        
        save_button = QPushButton("Save && Connect")
        save_button.clicked.connect(self._save_and_connect)
        save_button.setDefault(True)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def _create_plex_tab(self) -> QWidget:
        """Create Plex configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Plex Media Server Configuration</b>"))
        layout.addWidget(QLabel("Required for library access and playlist management."))
        layout.addSpacing(10)
        
        # Server URL
        layout.addWidget(QLabel("Server URL:"))
        self.plex_url_input = QLineEdit()
        self.plex_url_input.setPlaceholderText("http://localhost:32400")
        layout.addWidget(self.plex_url_input)
        
        # Token
        layout.addWidget(QLabel("Authentication Token:"))
        self.plex_token_input = QLineEdit()
        self.plex_token_input.setPlaceholderText("Your Plex token")
        self.plex_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.plex_token_input)
        
        show_token_check = QCheckBox("Show token")
        show_token_check.stateChanged.connect(
            lambda state: self.plex_token_input.setEchoMode(
                QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
            )
        )
        layout.addWidget(show_token_check)
        
        layout.addSpacing(10)
        help_label = QLabel(
            '<a href="https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/">'
            'How to find your Plex token</a>'
        )
        help_label.setOpenExternalLinks(True)
        layout.addWidget(help_label)
        
        layout.addStretch()
        return widget
    
    def _create_tautulli_tab(self) -> QWidget:
        """Create Tautulli configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Tautulli Configuration</b>"))
        layout.addWidget(QLabel("Optional. Provides user watch statistics and insights."))
        layout.addSpacing(10)
        
        # Server URL
        layout.addWidget(QLabel("Server URL:"))
        self.tautulli_url_input = QLineEdit()
        self.tautulli_url_input.setPlaceholderText("http://localhost:8181")
        layout.addWidget(self.tautulli_url_input)
        
        # API Key
        layout.addWidget(QLabel("API Key:"))
        self.tautulli_key_input = QLineEdit()
        self.tautulli_key_input.setPlaceholderText("Your Tautulli API key")
        self.tautulli_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.tautulli_key_input)
        
        show_key_check = QCheckBox("Show API key")
        show_key_check.stateChanged.connect(
            lambda state: self.tautulli_key_input.setEchoMode(
                QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
            )
        )
        layout.addWidget(show_key_check)
        
        layout.addSpacing(10)
        help_label = QLabel(
            'Find your API key in Tautulli: Settings → Web Interface → API'
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)
        
        layout.addStretch()
        return widget
    
    def _create_tmdb_tab(self) -> QWidget:
        """Create TMDB configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>TMDB (The Movie Database) Configuration</b>"))
        layout.addWidget(QLabel("Optional. Provides enhanced artwork and metadata."))
        layout.addSpacing(10)
        
        # API Key
        layout.addWidget(QLabel("API Key:"))
        self.tmdb_key_input = QLineEdit()
        self.tmdb_key_input.setPlaceholderText("Your TMDB API key (v3 auth)")
        self.tmdb_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.tmdb_key_input)
        
        show_key_check = QCheckBox("Show API key")
        show_key_check.stateChanged.connect(
            lambda state: self.tmdb_key_input.setEchoMode(
                QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
            )
        )
        layout.addWidget(show_key_check)
        
        layout.addSpacing(10)
        help_label = QLabel(
            '<a href="https://www.themoviedb.org/settings/api">'
            'Get a free TMDB API key</a>'
        )
        help_label.setOpenExternalLinks(True)
        layout.addWidget(help_label)
        
        layout.addStretch()
        return widget
    
    def _load_saved_credentials(self):
        """Load saved credentials from storage."""
        creds = self.credential_store.load_credentials()
        
        if plex_url := creds.get('plex_url'):
            self.plex_url_input.setText(plex_url)
        if plex_token := creds.get('plex_token'):
            self.plex_token_input.setText(plex_token)
        
        if tautulli_url := creds.get('tautulli_url'):
            self.tautulli_url_input.setText(tautulli_url)
        if tautulli_key := creds.get('tautulli_api_key'):
            self.tautulli_key_input.setText(tautulli_key)
        
        if tmdb_key := creds.get('tmdb_api_key'):
            self.tmdb_key_input.setText(tmdb_key)
    
    def _test_connection(self):
        """Test connections to all configured services."""
        results = []
        
        # Test Plex
        plex_url = self.plex_url_input.text().strip()
        plex_token = self.plex_token_input.text().strip()
        
        if plex_url and plex_token:
            try:
                client = PlexClient(plex_url, plex_token)
                if client.connect():
                    results.append("✓ Plex: Connected successfully")
                    server_name = client.server.friendlyName
                    results.append(f"  Server: {server_name}")
                else:
                    results.append("✗ Plex: Connection failed")
            except Exception as e:
                results.append(f"✗ Plex: {str(e)}")
        else:
            results.append("⊘ Plex: Not configured")
        
        # Test Tautulli
        tautulli_url = self.tautulli_url_input.text().strip()
        tautulli_key = self.tautulli_key_input.text().strip()
        
        if tautulli_url and tautulli_key:
            try:
                client = TautulliClient(tautulli_url, tautulli_key)
                if client.test_connection():
                    results.append("✓ Tautulli: Connected successfully")
                else:
                    results.append("✗ Tautulli: Connection failed")
            except Exception as e:
                results.append(f"✗ Tautulli: {str(e)}")
        else:
            results.append("⊘ Tautulli: Not configured (optional)")
        
        # Test TMDB
        tmdb_key = self.tmdb_key_input.text().strip()
        
        if tmdb_key:
            try:
                client = TMDBClient(tmdb_key)
                # Simple test: search for a known show
                result = client.search_tv_show("Breaking Bad")
                if result:
                    results.append("✓ TMDB: API key valid")
                else:
                    results.append("✗ TMDB: Invalid response")
            except Exception as e:
                results.append(f"✗ TMDB: {str(e)}")
        else:
            results.append("⊘ TMDB: Not configured (optional)")
        
        # Show results
        QMessageBox.information(
            self,
            "Connection Test Results",
            "\n".join(results)
        )
    
    def _save_and_connect(self):
        """Save credentials and establish connections."""
        # Validate Plex (required)
        plex_url = self.plex_url_input.text().strip()
        plex_token = self.plex_token_input.text().strip()
        
        if not plex_url or not plex_token:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Plex server URL and token are required."
            )
            return
        
        # Test Plex connection
        try:
            self.plex_client = PlexClient(plex_url, plex_token)
            if not self.plex_client.connect():
                QMessageBox.critical(
                    self,
                    "Connection Failed",
                    "Could not connect to Plex server. Please check your URL and token."
                )
                return
        except Exception as e:
            QMessageBox.critical(
                self,
                "Connection Error",
                f"Error connecting to Plex: {str(e)}"
            )
            return
        
        # Save credentials
        credentials = {
            'plex_url': plex_url,
            'plex_token': plex_token,
        }
        
        # Optional: Tautulli
        tautulli_url = self.tautulli_url_input.text().strip()
        tautulli_key = self.tautulli_key_input.text().strip()
        
        if tautulli_url and tautulli_key:
            try:
                self.tautulli_client = TautulliClient(tautulli_url, tautulli_key)
                if self.tautulli_client.test_connection():
                    credentials['tautulli_url'] = tautulli_url
                    credentials['tautulli_api_key'] = tautulli_key
            except Exception as e:
                print(f"Tautulli connection warning: {e}")
        
        # Optional: TMDB
        tmdb_key = self.tmdb_key_input.text().strip()
        
        if tmdb_key:
            try:
                self.tmdb_client = TMDBClient(tmdb_key)
                credentials['tmdb_api_key'] = tmdb_key
            except Exception as e:
                print(f"TMDB connection warning: {e}")
        
        # Save to encrypted storage
        self.credential_store.save_credentials(credentials)
        
        # Accept dialog
        self.accept()
    
    def get_clients(self) -> Dict:
        """
        Get connected clients.
        
        Returns:
            Dictionary with 'plex', 'tautulli', 'tmdb' clients
        """
        return {
            'plex': self.plex_client,
            'tautulli': self.tautulli_client,
            'tmdb': self.tmdb_client,
        }
