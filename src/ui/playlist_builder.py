"""Playlist builder panel for managing selected episodes."""

from typing import List, Dict, Set
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QPushButton, QComboBox,
    QProgressBar, QGroupBox, QSpinBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class PlaylistBuilderWidget(QWidget):
    """Widget for building and managing playlist contents."""
    
    # Signals
    create_playlist_requested = pyqtSignal(str, list)  # name, episode_ids
    dry_run_requested = pyqtSignal(str, list)          # name, episode_ids
    
    def __init__(self):
        super().__init__()
        self._selected_episodes: Dict[str, Dict] = {}  # episode_id -> metadata
        self._total_runtime_ms = 0
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Playlist Builder")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Playlist name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.playlist_name_input = QLineEdit()
        self.playlist_name_input.setPlaceholderText("My Playlist")
        name_layout.addWidget(self.playlist_name_input)
        layout.addLayout(name_layout)
        
        # Runtime meter
        runtime_group = QGroupBox("Runtime")
        runtime_layout = QVBoxLayout(runtime_group)
        
        self.runtime_label = QLabel("Total: 0 minutes")
        self.runtime_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        runtime_layout.addWidget(self.runtime_label)
        
        self.runtime_progress = QProgressBar()
        self.runtime_progress.setMaximum(100)
        self.runtime_progress.setValue(0)
        self.runtime_progress.setFormat("%v%")
        runtime_layout.addWidget(self.runtime_progress)
        
        # Runtime cap control
        cap_layout = QHBoxLayout()
        cap_layout.addWidget(QLabel("Cap:"))
        self.runtime_cap_spinbox = QSpinBox()
        self.runtime_cap_spinbox.setMinimum(0)
        self.runtime_cap_spinbox.setMaximum(1000)
        self.runtime_cap_spinbox.setValue(120)
        self.runtime_cap_spinbox.setSuffix(" min")
        self.runtime_cap_spinbox.valueChanged.connect(self._update_runtime_display)
        cap_layout.addWidget(self.runtime_cap_spinbox)
        cap_layout.addStretch()
        runtime_layout.addLayout(cap_layout)
        
        layout.addWidget(runtime_group)
        
        # Ordering controls
        order_layout = QHBoxLayout()
        order_layout.addWidget(QLabel("Order by:"))
        
        self.order_combo = QComboBox()
        self.order_combo.addItems([
            "Air Date",
            "Season/Episode (SxxExx)",
            "Added to Library",
            "Random",
            "Manual (drag to reorder)"
        ])
        order_layout.addWidget(self.order_combo, 1)
        layout.addLayout(order_layout)
        
        # Episode list
        list_header_layout = QHBoxLayout()
        list_header_layout.addWidget(QLabel("Selected Episodes"))
        
        self.episode_count_label = QLabel("(0)")
        self.episode_count_label.setStyleSheet("color: #666;")
        list_header_layout.addWidget(self.episode_count_label)
        list_header_layout.addStretch()
        layout.addLayout(list_header_layout)
        
        self.episode_list = QListWidget()
        self.episode_list.setAlternatingRowColors(True)
        self.episode_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.episode_list)
        
        # Quick actions
        quick_actions_layout = QHBoxLayout()
        
        remove_selected_btn = QPushButton("Remove Selected")
        remove_selected_btn.clicked.connect(self._remove_selected)
        quick_actions_layout.addWidget(remove_selected_btn)
        
        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.clicked.connect(self._clear_all)
        quick_actions_layout.addWidget(clear_all_btn)
        
        layout.addLayout(quick_actions_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.dry_run_btn = QPushButton("Dry Run Preview")
        self.dry_run_btn.setEnabled(False)
        self.dry_run_btn.clicked.connect(self._on_dry_run)
        action_layout.addWidget(self.dry_run_btn)
        
        self.create_btn = QPushButton("Create Playlist")
        self.create_btn.setEnabled(False)
        self.create_btn.clicked.connect(self._on_create_playlist)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        action_layout.addWidget(self.create_btn)
        
        layout.addLayout(action_layout)
    
    def update_selection(self, episode_ids: Set[str], episode_metadata: Dict[str, Dict]):
        """
        Update selected episodes.
        
        Args:
            episode_ids: Set of selected episode IDs
            episode_metadata: Dictionary mapping episode IDs to metadata
        """
        # Update internal state
        self._selected_episodes = {
            ep_id: episode_metadata.get(ep_id, {})
            for ep_id in episode_ids
        }
        
        # Recalculate runtime
        self._total_runtime_ms = sum(
            ep.get('duration', 0) for ep in self._selected_episodes.values()
        )
        
        # Update UI
        self._refresh_episode_list()
        self._update_runtime_display()
        self._update_button_states()
    
    def _refresh_episode_list(self):
        """Refresh the episode list widget."""
        self.episode_list.clear()
        
        # Sort episodes based on selected ordering
        episodes = list(self._selected_episodes.items())
        order_mode = self.order_combo.currentText()
        
        if "Air Date" in order_mode:
            episodes.sort(key=lambda x: x[1].get('originallyAvailableAt', ''))
        elif "SxxExx" in order_mode:
            episodes.sort(key=lambda x: (
                x[1].get('parentIndex', 0),
                x[1].get('index', 0)
            ))
        elif "Added" in order_mode:
            episodes.sort(key=lambda x: x[1].get('addedAt', ''))
        elif "Random" in order_mode:
            import random
            random.shuffle(episodes)
        
        # Add to list
        for ep_id, metadata in episodes:
            show_title = metadata.get('grandparentTitle', 'Unknown Show')
            season_num = metadata.get('parentIndex', 0)
            episode_num = metadata.get('index', 0)
            ep_title = metadata.get('title', 'Unknown Episode')
            
            duration_ms = metadata.get('duration', 0)
            duration_min = duration_ms // 60000 if duration_ms else 0
            
            display_text = f"{show_title} - {season_num}x{episode_num:02d} - {ep_title} ({duration_min} min)"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, ep_id)
            self.episode_list.addItem(item)
        
        # Update count
        self.episode_count_label.setText(f"({len(episodes)})")
    
    def _update_runtime_display(self):
        """Update runtime meter display."""
        total_minutes = self._total_runtime_ms // 60000
        cap_minutes = self.runtime_cap_spinbox.value()
        
        self.runtime_label.setText(f"Total: {total_minutes} minutes")
        
        if cap_minutes > 0:
            percentage = min(100, int((total_minutes / cap_minutes) * 100))
            self.runtime_progress.setValue(percentage)
            
            # Color code the progress bar
            if percentage > 100:
                color = "#f44336"  # Red - over cap
            elif percentage > 90:
                color = "#ff9800"  # Orange - near cap
            else:
                color = "#4CAF50"  # Green - within cap
            
            self.runtime_progress.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {color};
                }}
            """)
        else:
            self.runtime_progress.setValue(0)
    
    def _update_button_states(self):
        """Update enabled state of action buttons."""
        has_episodes = len(self._selected_episodes) > 0
        has_name = bool(self.playlist_name_input.text().strip())
        
        self.dry_run_btn.setEnabled(has_episodes)
        self.create_btn.setEnabled(has_episodes and has_name)
    
    def _remove_selected(self):
        """Remove selected items from the list."""
        for item in self.episode_list.selectedItems():
            ep_id = item.data(Qt.ItemDataRole.UserRole)
            if ep_id in self._selected_episodes:
                del self._selected_episodes[ep_id]
        
        self._refresh_episode_list()
        self._update_runtime_display()
        self._update_button_states()
    
    def _clear_all(self):
        """Clear all episodes from the list."""
        self._selected_episodes.clear()
        self._total_runtime_ms = 0
        self._refresh_episode_list()
        self._update_runtime_display()
        self._update_button_states()
    
    def _on_dry_run(self):
        """Handle dry run preview request."""
        name = self.playlist_name_input.text().strip() or "Untitled Playlist"
        episode_ids = list(self._selected_episodes.keys())
        self.dry_run_requested.emit(name, episode_ids)
    
    def _on_create_playlist(self):
        """Handle playlist creation request."""
        name = self.playlist_name_input.text().strip()
        if not name:
            return
        
        episode_ids = list(self._selected_episodes.keys())
        self.create_playlist_requested.emit(name, episode_ids)
    
    def get_selected_episode_ids(self) -> List[str]:
        """
        Get ordered list of selected episode IDs.
        
        Returns:
            List of episode IDs in current order
        """
        return [
            self.episode_list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.episode_list.count())
        ]
    
    def clear(self):
        """Clear all selections."""
        self._clear_all()
