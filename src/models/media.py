"""Data models for media items and playlists."""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MediaType(Enum):
    """Media node types."""
    SHOW = "show"
    SEASON = "season"
    EPISODE = "episode"


class PlaylistMode(Enum):
    """Playlist operation modes."""
    STATIC = "static"
    SMART = "smart"


class WatchState(Enum):
    """Watch state for episodes."""
    UNWATCHED = "unwatched"
    IN_PROGRESS = "in_progress"
    WATCHED = "watched"


@dataclass
class MediaNode:
    """Represents a media item (Show, Season, or Episode)."""
    id: str
    type: MediaType
    title: str
    parent_id: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None
    thumb_url: Optional[str] = None
    runtime_ms: Optional[int] = None
    air_date: Optional[datetime] = None
    quality_flags: List[str] = None
    audio_langs: List[str] = None
    subtitle_langs: List[str] = None
    
    def __post_init__(self):
        if self.quality_flags is None:
            self.quality_flags = []
        if self.audio_langs is None:
            self.audio_langs = []
        if self.subtitle_langs is None:
            self.subtitle_langs = []


@dataclass
class Selection:
    """Represents a selected media item."""
    node_id: str
    type: MediaType
    added_at: datetime
    source: str  # manual, template, rule
    
    def __hash__(self):
        return hash(self.node_id)


@dataclass
class SmartRule:
    """Rules for smart playlist generation."""
    # Scope
    libraries: List[str] = None
    include_shows: List[str] = None
    include_seasons: List[str] = None
    include_collections: List[str] = None
    
    # User context
    user_id: Optional[int] = None
    
    # Conditions
    watch_state: Optional[WatchState] = None
    play_count_min: Optional[int] = None
    play_count_max: Optional[int] = None
    air_date_from: Optional[datetime] = None
    air_date_to: Optional[datetime] = None
    runtime_min_ms: Optional[int] = None
    runtime_max_ms: Optional[int] = None
    genres: List[str] = None
    networks: List[str] = None
    quality: List[str] = None
    audio_langs: List[str] = None
    min_user_rating: Optional[float] = None
    last_watched_from: Optional[datetime] = None
    last_watched_to: Optional[datetime] = None
    include_specials: bool = True
    
    # Limits
    max_items: Optional[int] = None
    runtime_cap_ms: Optional[int] = None
    per_show_cap: Optional[int] = None
    
    # Ordering
    ordering: str = "seasonEpisode"  # airDate, seasonEpisode, recentActivity, addedDate, random
    ordering_direction: str = "asc"
    
    # Interleave
    interleave: str = "none"  # none, roundRobin, chunk
    interleave_chunk_size: int = 1
    
    # Refresh
    refresh_mode: str = "manual"  # manual, daily, weekly
    
    def __post_init__(self):
        if self.libraries is None:
            self.libraries = []
        if self.include_shows is None:
            self.include_shows = []
        if self.include_seasons is None:
            self.include_seasons = []
        if self.include_collections is None:
            self.include_collections = []
        if self.genres is None:
            self.genres = []
        if self.networks is None:
            self.networks = []
        if self.quality is None:
            self.quality = []
        if self.audio_langs is None:
            self.audio_langs = []


@dataclass
class Playlist:
    """Represents a playlist."""
    name: str
    mode: PlaylistMode
    owner_user: Optional[int] = None
    items: List[str] = None  # List of episode IDs
    ordering: str = "seasonEpisode"
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    smart_rule: Optional[SmartRule] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
