"""Main application window."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QMenuBar, QMenu, QToolBar, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    """Main application window for Playlist Buddy."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playlist Buddy")
        self.setGeometry(100, 100, 1400, 900)
        
        self._setup_ui()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main horizontal splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Library tree (will be implemented)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self._create_placeholder("Library Tree"))
        
        # Right panel - Playlist builder (will be implemented)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self._create_placeholder("Playlist Builder"))
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
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
        view_menu.addAction(refresh_action)
        
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
        toolbar.addAction(connect_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction("Refresh", self)
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
