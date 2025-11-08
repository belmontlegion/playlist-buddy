"""Library tree view with tri-state checkboxes for media browsing."""

from typing import Optional, Dict, Set, List
from PyQt6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, 
    QLabel, QComboBox, QProgressBar, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

from src.models.media import MediaType


class MediaTreeItem(QTreeWidgetItem):
    """Custom tree item for media nodes with tri-state checkbox."""
    
    def __init__(self, parent, node_id: str, node_type: MediaType, title: str):
        super().__init__(parent)
        self.node_id = node_id
        self.node_type = node_type
        self.title = title
        self.is_loaded = False  # For lazy loading
        
        self.setText(0, title)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Unchecked)
    
    def setData(self, column: int, role: int, value):
        """Override to handle tri-state checkbox behavior."""
        if role == Qt.ItemDataRole.CheckStateRole and column == 0:
            # Store the old state
            old_state = self.checkState(0)
            
            # Set the new state
            super().setData(column, role, value)
            
            # If this is a parent node, propagate to children
            if self.node_type in [MediaType.SHOW, MediaType.SEASON]:
                self._propagate_to_children(value)
            
            # Update parent state
            self._update_parent_state()
        else:
            super().setData(column, role, value)
    
    def _propagate_to_children(self, state: Qt.CheckState):
        """Propagate check state to all children."""
        for i in range(self.childCount()):
            child = self.child(i)
            if isinstance(child, MediaTreeItem):
                child.setCheckState(0, state)
    
    def _update_parent_state(self):
        """Update parent's check state based on children."""
        parent = self.parent()
        if not isinstance(parent, MediaTreeItem):
            return
        
        # Count checked and unchecked children
        total = parent.childCount()
        checked = 0
        partially_checked = 0
        
        for i in range(total):
            child = parent.child(i)
            if isinstance(child, MediaTreeItem):
                state = child.checkState(0)
                if state == Qt.CheckState.Checked:
                    checked += 1
                elif state == Qt.CheckState.PartiallyChecked:
                    partially_checked += 1
        
        # Set parent state
        if checked == total:
            parent.setCheckState(0, Qt.CheckState.Checked)
        elif checked > 0 or partially_checked > 0:
            parent.setCheckState(0, Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(0, Qt.CheckState.Unchecked)


class LibraryTreeWidget(QWidget):
    """Widget containing library tree view with controls."""
    
    # Signals
    selection_changed = pyqtSignal(set)  # Emits set of selected node IDs
    library_changed = pyqtSignal(str)    # Emits library ID
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._selected_items: Set[str] = set()
        self._node_map: Dict[str, MediaTreeItem] = {}  # node_id -> item
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Library selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Library:"))
        
        self.library_combo = QComboBox()
        self.library_combo.currentTextChanged.connect(self._on_library_changed)
        selector_layout.addWidget(self.library_combo, 1)
        
        layout.addLayout(selector_layout)
        
        # Progress bar for loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "Episodes", "Duration"])
        self.tree.setColumnWidth(0, 300)
        self.tree.itemChanged.connect(self._on_item_changed)
        self.tree.itemExpanded.connect(self._on_item_expanded)
        layout.addWidget(self.tree)
        
        # Status label
        self.status_label = QLabel("No library loaded")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def set_libraries(self, libraries: List[Dict]):
        """
        Set available libraries.
        
        Args:
            libraries: List of library dicts with 'id' and 'title'
        """
        self.library_combo.clear()
        for lib in libraries:
            self.library_combo.addItem(lib['title'], lib['id'])
    
    def load_shows(self, shows: List[Dict]):
        """
        Load shows into the tree.
        
        Args:
            shows: List of show dicts with metadata
        """
        self.tree.clear()
        self._node_map.clear()
        self._selected_items.clear()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(shows))
        
        for idx, show in enumerate(shows):
            self._add_show(show)
            self.progress_bar.setValue(idx + 1)
        
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Loaded {len(shows)} shows")
    
    def _add_show(self, show: Dict):
        """Add a show to the tree."""
        show_id = str(show.get('id', show.get('ratingKey')))
        title = show.get('title', 'Unknown Show')
        
        item = MediaTreeItem(self.tree, show_id, MediaType.SHOW, title)
        item.setToolTip(0, f"{title}\nClick to expand seasons")
        
        # Add placeholder for lazy loading
        if show.get('childCount', 0) > 0:
            placeholder = QTreeWidgetItem(item)
            placeholder.setText(0, "Loading...")
            placeholder.setFlags(Qt.ItemFlag.NoItemFlags)
        
        self._node_map[show_id] = item
    
    def load_seasons(self, show_id: str, seasons: List[Dict]):
        """
        Load seasons for a show (lazy loading).
        
        Args:
            show_id: Show node ID
            seasons: List of season dicts
        """
        if show_id not in self._node_map:
            return
        
        show_item = self._node_map[show_id]
        
        # Remove placeholder
        show_item.takeChildren()
        
        for season in seasons:
            self._add_season(show_item, season)
        
        show_item.is_loaded = True
    
    def _add_season(self, show_item: MediaTreeItem, season: Dict):
        """Add a season to a show."""
        season_id = str(season.get('id', season.get('ratingKey')))
        season_num = season.get('index', season.get('seasonNumber', 0))
        title = season.get('title', f'Season {season_num}')
        
        item = MediaTreeItem(show_item, season_id, MediaType.SEASON, title)
        item.setText(1, str(season.get('leafCount', 0)))
        item.setToolTip(0, f"{title}\nClick to expand episodes")
        
        # Add placeholder for lazy loading
        if season.get('leafCount', 0) > 0:
            placeholder = QTreeWidgetItem(item)
            placeholder.setText(0, "Loading...")
            placeholder.setFlags(Qt.ItemFlag.NoItemFlags)
        
        self._node_map[season_id] = item
    
    def load_episodes(self, season_id: str, episodes: List[Dict]):
        """
        Load episodes for a season (lazy loading).
        
        Args:
            season_id: Season node ID
            episodes: List of episode dicts
        """
        if season_id not in self._node_map:
            return
        
        season_item = self._node_map[season_id]
        
        # Remove placeholder
        season_item.takeChildren()
        
        for episode in episodes:
            self._add_episode(season_item, episode)
        
        season_item.is_loaded = True
    
    def _add_episode(self, season_item: MediaTreeItem, episode: Dict):
        """Add an episode to a season."""
        episode_id = str(episode.get('id', episode.get('ratingKey')))
        episode_num = episode.get('index', episode.get('episodeNumber', 0))
        title = episode.get('title', f'Episode {episode_num}')
        
        # Format: "1x01 - Episode Title"
        display_title = f"{episode.get('parentIndex', 0)}x{episode_num:02d} - {title}"
        
        item = MediaTreeItem(season_item, episode_id, MediaType.EPISODE, display_title)
        
        # Duration
        duration_ms = episode.get('duration', 0)
        if duration_ms:
            minutes = duration_ms // 60000
            item.setText(2, f"{minutes} min")
        
        item.setToolTip(0, self._build_episode_tooltip(episode))
        
        self._node_map[episode_id] = item
    
    def _build_episode_tooltip(self, episode: Dict) -> str:
        """Build tooltip for episode with metadata."""
        lines = [episode.get('title', 'Unknown')]
        
        if summary := episode.get('summary'):
            lines.append(f"\n{summary[:100]}...")
        
        if air_date := episode.get('originallyAvailableAt'):
            lines.append(f"\nAired: {air_date}")
        
        if duration := episode.get('duration'):
            minutes = duration // 60000
            lines.append(f"Runtime: {minutes} minutes")
        
        return '\n'.join(lines)
    
    def _on_library_changed(self, library_name: str):
        """Handle library selection change."""
        library_id = self.library_combo.currentData()
        if library_id:
            self.library_changed.emit(library_id)
    
    def _on_item_changed(self, item: QTreeWidgetItem, column: int):
        """Handle item check state changes."""
        if not isinstance(item, MediaTreeItem):
            return
        
        # Update selected items
        self._update_selected_items()
        self.selection_changed.emit(self._selected_items.copy())
    
    def _on_item_expanded(self, item: QTreeWidgetItem):
        """Handle item expansion for lazy loading."""
        if not isinstance(item, MediaTreeItem):
            return
        
        if item.is_loaded:
            return
        
        # Emit signal to load children (handled by controller)
        if item.node_type == MediaType.SHOW:
            # Signal will be connected to load seasons
            pass
        elif item.node_type == MediaType.SEASON:
            # Signal will be connected to load episodes
            pass
    
    def _update_selected_items(self):
        """Update the set of selected episode IDs."""
        self._selected_items.clear()
        
        # Recursively collect all checked episodes
        def collect_episodes(item: QTreeWidgetItem):
            if isinstance(item, MediaTreeItem):
                if item.checkState(0) != Qt.CheckState.Unchecked:
                    if item.node_type == MediaType.EPISODE:
                        self._selected_items.add(item.node_id)
                
                for i in range(item.childCount()):
                    collect_episodes(item.child(i))
        
        # Check all top-level items
        for i in range(self.tree.topLevelItemCount()):
            collect_episodes(self.tree.topLevelItem(i))
    
    def get_selected_episodes(self) -> Set[str]:
        """
        Get set of selected episode IDs.
        
        Returns:
            Set of episode node IDs
        """
        return self._selected_items.copy()
    
    def clear_selection(self):
        """Clear all selections."""
        # Uncheck all items
        def uncheck_recursive(item: QTreeWidgetItem):
            if isinstance(item, MediaTreeItem):
                item.setCheckState(0, Qt.CheckState.Unchecked)
            
            for i in range(item.childCount()):
                uncheck_recursive(item.child(i))
        
        for i in range(self.tree.topLevelItemCount()):
            uncheck_recursive(self.tree.topLevelItem(i))
    
    def expand_all(self):
        """Expand all tree items."""
        self.tree.expandAll()
    
    def collapse_all(self):
        """Collapse all tree items."""
        self.tree.collapseAll()
