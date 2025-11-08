"""Main application window."""

from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from src.ui.library_tree import LibraryTreeWidget
from src.ui.connection_dialog import ConnectionDialog
from src.api.plex_client import PlexClient
from src.api.tautulli_client import TautulliClient
from src.api.tmdb_client import TMDBClient
from src.utils.credential_store import CredentialStore


class MainWindow(QMainWindow):
    """Main application window for Playlist Buddy."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playlist Buddy")
        self.setGeometry(100, 100, 1400, 900)
        
        # API clients
        self.plex_client: Optional[PlexClient] = None
        self.tautulli_client: Optional[TautulliClient] = None
        self.tmdb_client: Optional[TMDBClient] = None
        
        # Credential store
        self.credential_store = CredentialStore()
        
        self._setup_ui()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        
        # Try to auto-connect if credentials exist
        QTimer.singleShot(100, self._auto_connect)
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main horizontal splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Library tree
        self.library_tree = LibraryTreeWidget()
        self.library_tree.library_changed.connect(self._on_library_changed)
        self.library_tree.selection_changed.connect(self._on_selection_changed)
        
        # Right panel - Playlist builder (placeholder for now)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self._create_placeholder("Playlist Builder\n\nSelected items will appear here"))
        
        # Add panels to splitter
        splitter.addWidget(self.library_tree)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 600])
        
        main_layout.addWidget(splitter)
    
    def _create_placeholder(self, text: str) -> QWidget:
        """Create a placeholder widget for development."""
        from PyQt6.QtWidgets import QLabel
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #666;")
        return label
    
    def _create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        connect_action = QAction("&Connect to Plex...", self)
        connect_action.setShortcut("Ctrl+O")
        connect_action.triggered.connect(self._show_connection_dialog)
        file_menu.addAction(connect_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        preferences_action = QAction("&Preferences...", self)
        preferences_action.setShortcut("Ctrl+,")
        edit_menu.addAction(preferences_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        refresh_action = QAction("&Refresh Library", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_library)
        view_menu.addAction(refresh_action)
        
        view_menu.addSeparator()
        
        expand_all_action = QAction("Expand All", self)
        expand_all_action.triggered.connect(self.library_tree.expand_all)
        view_menu.addAction(expand_all_action)
        
        collapse_all_action = QAction("Collapse All", self)
        collapse_all_action.triggered.connect(self.library_tree.collapse_all)
        view_menu.addAction(collapse_all_action)
        
        # Playlist menu
        playlist_menu = menubar.addMenu("&Playlist")
        
        new_playlist_action = QAction("&New Playlist", self)
        new_playlist_action.setShortcut("Ctrl+N")
        playlist_menu.addAction(new_playlist_action)
        
        new_smart_playlist_action = QAction("New &Smart Playlist", self)
        new_smart_playlist_action.setShortcut("Ctrl+Shift+N")
        playlist_menu.addAction(new_smart_playlist_action)
        
        playlist_menu.addSeparator()
        
        dry_run_action = QAction("&Dry Run Preview", self)
        dry_run_action.setShortcut("Ctrl+D")
        playlist_menu.addAction(dry_run_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About Playlist Buddy", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add toolbar actions (icons will be added later)
        connect_action = QAction("Connect", self)
        connect_action.triggered.connect(self._show_connection_dialog)
        toolbar.addAction(connect_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self._refresh_library)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        new_playlist_action = QAction("New Playlist", self)
        toolbar.addAction(new_playlist_action)
        
        dry_run_action = QAction("Dry Run", self)
        toolbar.addAction(dry_run_action)
    
    def _create_statusbar(self):
        """Create application status bar."""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        statusbar.showMessage("Ready")
    
    def _show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About Playlist Buddy",
            "<h3>Playlist Buddy v0.1.0</h3>"
            "<p>A robust desktop GUI tool for creating and managing Plex playlists</p>"
            "<p>using Tautulli insights and the Plex API.</p>"
            "<p><b>Author:</b> Scott McKay</p>"
            "<p><b>License:</b> MIT</p>"
        )
    
    def _auto_connect(self):
        """Attempt to auto-connect using saved credentials."""
        creds = self.credential_store.load_credentials()
        
        if not creds.get('plex_url') or not creds.get('plex_token'):
            # No saved credentials, show connection dialog
            self.statusBar().showMessage("Not connected - Click 'Connect' to set up")
            return
        
        # Try to connect
        try:
            self.plex_client = PlexClient(creds['plex_url'], creds['plex_token'])
            if self.plex_client.connect():
                self.statusBar().showMessage(f"Connected to {self.plex_client.server.friendlyName}")
                self._load_libraries()
            else:
                self.statusBar().showMessage("Connection failed - Check settings")
        except Exception as e:
            self.statusBar().showMessage(f"Connection error: {str(e)}")
        
        # Optional clients
        if creds.get('tautulli_url') and creds.get('tautulli_api_key'):
            try:
                self.tautulli_client = TautulliClient(
                    creds['tautulli_url'],
                    creds['tautulli_api_key']
                )
            except Exception as e:
                print(f"Tautulli connection failed: {e}")
        
        if creds.get('tmdb_api_key'):
            try:
                self.tmdb_client = TMDBClient(creds['tmdb_api_key'])
            except Exception as e:
                print(f"TMDB connection failed: {e}")
    
    def _show_connection_dialog(self):
        """Show connection configuration dialog."""
        dialog = ConnectionDialog(self)
        if dialog.exec():
            clients = dialog.get_clients()
            self.plex_client = clients['plex']
            self.tautulli_client = clients['tautulli']
            self.tmdb_client = clients['tmdb']
            
            if self.plex_client:
                self.statusBar().showMessage(f"Connected to {self.plex_client.server.friendlyName}")
                self._load_libraries()
    
    def _load_libraries(self):
        """Load libraries from Plex server."""
        if not self.plex_client:
            return
        
        try:
            libraries = self.plex_client.get_libraries()
            self.library_tree.set_libraries(libraries)
            
            if libraries:
                self.statusBar().showMessage(f"Loaded {len(libraries)} libraries")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading libraries: {str(e)}")
    
    def _on_library_changed(self, library_id: str):
        """Handle library selection change."""
        if not self.plex_client:
            return
        
        self.statusBar().showMessage("Loading shows...")
        
        try:
            # Get shows from library
            shows = self.plex_client.get_shows(library_id)
            
            # Convert to dict format for tree
            show_data = []
            for show in shows:
                show_data.append({
                    'id': show.ratingKey,
                    'ratingKey': show.ratingKey,
                    'title': show.title,
                    'childCount': show.childCount,
                })
            
            self.library_tree.load_shows(show_data)
            self.statusBar().showMessage(f"Loaded {len(shows)} shows")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading shows: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load shows: {str(e)}")
    
    def _on_selection_changed(self, selected_ids: set):
        """Handle selection changes in the tree."""
        count = len(selected_ids)
        if count > 0:
            self.statusBar().showMessage(f"{count} episode(s) selected")
        else:
            self.statusBar().showMessage("Ready")
    
    def _refresh_library(self):
        """Refresh the current library."""
        current_lib = self.library_tree.library_combo.currentData()
        if current_lib:
            self._on_library_changed(current_lib)
