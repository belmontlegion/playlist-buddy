# Tautulli‑Powered Playlist Builder — High‑Level Vision

**Revision:** 2025‑11‑08  •  **Status:** Draft  •  **Owner:** Scott

---

## 1) Overview
**Purpose.** Design and ship a robust, easy‑to‑use desktop GUI tool to create and manage Plex playlists, using **Tautulli** for user‑centric insights (plays, watch state, recency, ratings) and the **Plex API** for playlist CRUD and library data.

**Scope.** Browse shows → select whole shows, seasons, or specific episodes → preview → create/update **static** or **smart (rule‑based)** playlists. The tool should scale to very large libraries while staying responsive and intuitive.

**Non‑Goals (for now).** Media editing/transcoding, server admin, cross‑server playlist sync.

---

## 2) Product Objectives
- **Frictionless selection.** Tree view with posters at Show/Season nodes and desaturated (greyed) thumbnails for Episodes; tri‑state checkboxes for bulk/partial selection.
- **User‑aware curation.** Filters and templates informed by Tautulli stats per Plex user.
- **Safe and transparent.** Dry‑run previews, duplicate/conflict guards, readable logs.
- **Fast at scale.** Virtualized UI, lazy data loading, local thumbnail cache.
- **Two playlist modes.** Static lists and Smart (rule‑based) playlists with auto‑refresh.

---

## 3) Primary Users & Use Cases
**Users**
- Solo viewer curating personal queues.
- Household admin assembling shared family playlists.
- Power user managing large libraries and watch states.

**Top flows**
1. Build a weekend queue from next‑unwatched across 3–4 comedies.
2. Make a season sampler (first 2 episodes of each season) to test a show.
3. Time‑box a playlist to ~2 hours of unwatched 30‑minute episodes.
4. Create a smart “Catch‑Up” list that auto‑refreshes daily for a specific user.

---

## 4) System Architecture (High Level)
- **Tautulli API** → read‑only insights: users, watch history/stats, last‑watched, play counts, user ratings, completion.
- **Plex API (official)** → library browse, metadata/artwork, playlist create/update/delete, search, collections, intro/credits markers (where available).
- **TMDB API** → external enrichment: high‑quality posters/backdrops, season/episode imagery, keywords (for themes/holidays), genres, networks, air dates, alternative titles/orders.
- **App** → merges all three: discovery & personalization powered by **Tautulli**, authoritative library & playlist writes via **Plex**, richer UX & “smart” templates via **TMDB**.

**Security.** Store Plex and Tautulli tokens and TMDB API key encrypted locally; never transmit to third parties.

---

## 5) UX Blueprint
### 5.1 Main Layout
- **Left panel:** Library picker + **Tree** (Show ▸ Season ▸ Episode) with **tri‑state** checkboxes.
- **Top bar:** Search box + Facets (Unwatched, Duration, Genre, Year, Quality, Network).
- **Right panel (Playlist Builder):** Selected items list (de‑duplicated), ordering, limits, timebox meter, drag‑reorder.
- **Bottom bar:** **Dry Run** • **Create/Update** • **Export** • **Undo**.

### 5.2 Tree View Details
- **Thumbnails** at Show/Season nodes; **Episode thumbnails are greyscale** versions of the season poster or episode still.
- **Status badges** (small overlays): Unwatched dot, 4K/HDR, multi‑audio, intro markers.
- **Tooltips** on hover: runtime, air date, play count, last watched, audio/subtitle langs.
- **Tri‑state behavior:**
  - Checking a **Show** selects all child seasons/episodes.
  - Checking a **Season** selects all its episodes.
  - Partial selections bubble up (indeterminate state).
  - Keyboard navigation; expand/collapse all; lazy node loading.

### 5.3 Selection Cart (Right Panel)
- Live, de‑duplicated list of items chosen.
- **Ordering:** Air date, SxxExx, Added date, Recent activity, Random (asc/desc), Manual drag.
- **Quick actions:** “Remove all from this show/season,” “Clear,” “De‑dupe.”
- **Runtime meter:** Sums total runtime; warns if exceeding a set cap.

### 5.4 Quick Picks on Nodes
- **Add All**, **Add Unwatched**, **Add From Next Unwatched**, **Add Last N**, **Add Aired in Year…**

### 5.5 Search & Facets
- Global search by title/summary; facets: **Unwatched**, **Duration (<30/30–60/60+)**, **Genre**, **Year**, **Network**, **Quality (4K/HDR)**, **Audio language**.

### 5.6 Templates
- **Catch‑Up Tonight:** Unwatched ≤30m, runtime cap.
- **Season Sampler:** First 2 eps per season.
- **Holiday Episodes:** Keyword match on title/summary/collections (editable keyword list).
- **Rewatch Favorites:** Highest user ratings or most‑rewatched.

### 5.7 Timebox Builder
- Input target runtime (e.g., 120 minutes). Fills from current scope respecting filters; greedy or balanced algorithm (see §8.4).

### 5.8 Paste‑to‑Add Parser
- Accepts lines like `Show Name S02E03`, `Show Name 1x03–1x06`, `Show Name Season 3`.
- Resolves to exact episodes/seasons; on conflicts, prompts.

### 5.9 Import/Export
- **CSV/JSON** export of playlist contents (for sharing/versioning).
- **Import** previously exported lists.
- **M3U** export for external players.

### 5.10 Dynamic (“Smart”) Playlists
- **Mode:** switch Static ↔ Smart.
- **Rule builder** (form, no code): scope, conditions, limits, ordering, interleave, refresh cadence.
- **Auto‑refresh**: manual/daily/weekly.

### 5.11 Interleave Options
- **Round‑robin** across shows (1 episode per show in rotation).
- **Chunked** (2–3 from each before moving on).

### 5.12 Multi‑User & Visibility
- Select **Plex user/home user**; rules apply to that user’s watch state.
- Visibility: personal vs shared (where Plex supports it).

### 5.13 Safety & Feedback
- **Dry Run Preview** shows create/update diff before committing.
- **Duplicate/conflict guard** with reasons for exclusions.
- **Broken/missing media warning** (file unavailable, unmatched, etc.).
- **Logs**: human‑readable summary of each operation.

### 5.14 Accessibility & Polish
- Large‑thumb mode; keyboard‑complete; color‑blind‑safe badges; high‑contrast option.
- Local caching of thumbs/metadata; virtualized lists for large datasets.

---

## 6) Data Model (Conceptual)
### 6.1 Core Entities
- **MediaNode** `{ id, type: Show|Season|Episode, parentId, title, seasonNumber?, episodeNumber?, thumbUrl, runtimeMs, airDate, qualityFlags, audioLangs, subtitleLangs }`
- **Selection** `{ nodeId, type, addedAt, source: manual|template|rule }`
- **Playlist** `{ id?, name, mode: Static|Smart, ownerUser, items:[EpisodeId…], ordering, createdAt, updatedAt }`
- **SmartRule** (see below) persisted with the playlist when in Smart mode.

### 6.2 Rule Schema (Smart Playlists)
- **Scope**: libraries[], includeShows[], includeSeasons[], includeCollections[]
- **User Context**: userId (required for watch‑state filters)
- **Conditions**: watchedState (unwatched|in‑progress|watched), playCount range, airDate range, runtime range, genres[], networks[], quality (4K/HDR/SDR), audioLangs[], minUserRating, lastWatched range, includeSpecials (bool)
- **Limits**: maxItems, runtimeCap, perShowCap
- **Ordering**: airDate|seasonEpisode|recentActivity|addedDate|random (asc/desc)
- **Interleave**: none|roundRobin|chunk(size)
- **Refresh**: manual|daily|weekly

### 6.3 CSV Export Schema (Static Playlists)
`type, plex_id, guid, show, season, episode_code, title, runtime_minutes`

### 6.4 JSON Export Schema (Static or Smart)
```json
{
  "name": "Weekend Queue",
  "mode": "Smart",
  "rules": { /* SmartRule */ },
  "ordering": "seasonEpisode",
  "items": [ /* optional for Static */ ]
}
```

---

## 7) API Responsibilities (High Level)
### 7.1 Plex API (authoritative source for your library & playlists)
- **Auth & discovery:** server, libraries, sections; list shows/seasons/episodes; pull metadata, posters, and markers when available.
- **Playlists:** create/update/delete static playlists; set item order; read back contents to diff during dry‑run.
- **Search & resolve:** resolve items by `ratingsKey`/`guid`; search by title/season/episode when parsing pasted input.
- **Collections & hubs:** (optional) read “On Deck,” “Recently Added,” and Collections to seed templates.
- **Thumbnails:** prefer Plex‑hosted art; fall back to TMDB when missing.

### 7.2 Tautulli API (personalization & stats)
- Users & watch history; play counts, last watched, completion rate, in‑progress.
- Per‑user filtering: **Unwatched for USER**, **Neglected (no plays in X months)**, **Most rewatched**, **Abandoned (low completion)**.
- Activity‑based ordering: **Recent activity** sort.

### 7.3 TMDB API (enrichment & suggestions)
- Posters/backdrops and season art when Plex lacks good art.
- **Keywords** (holiday/theme detectors), **genres**, **networks**, air dates; alternate titles for matching.
- Lightweight **trending/popular** (optional) to inspire templates if the item exists in Plex.
- Rate‑limit aware caching: memoize lookups by TMDB id and Plex guid; honor TMDB’s daily limits.

*Exact endpoints are mapped during technical design; this document stays API‑agnostic at the vision level.*

---

## 8) Core Algorithms & Logic
### 8.1 Tri‑State Selection
- Node state = {checked | unchecked | indeterminate}. Child toggles bubble up; parent toggles cascade down. Keep **de‑duplication** when nodes are included via both a parent and explicit child.

### 8.2 Duplicate & Conflict Guard
- Unique key = Episode (ratingsKey/guid). If an item is already included, reject subsequent adds and annotate with **reason** (duplicate, not in scope, filtered out by rule, etc.).

### 8.3 Next‑Unwatched Resolution
- For a user, determine next unwatched per show/season using Tautulli last‑watched + Plex episode ordering; skip specials if configured.

### 8.4 Timebox Fill
- **Greedy**: pick shortest items first until cap met, or
- **Balanced**: pick from each selected show in round‑robin while approaching cap within ±5 minutes. Prefer unwatched and recent items when ties occur.

### 8.5 Paste‑to‑Add Grammar (Examples)
- `Show Name S02E03`
- `Show Name 2x03–2x06`
- `Show Name Season 3`
- `Show Name S3E1, S3E4`
- On ambiguity, present a resolve dialog.

---

## 9) Performance & Reliability
- **Virtualized lists** and **lazy loading** of tree nodes.
- **Local cache** for metadata/artwork with freshness windows.
- **Batch** Plex lookups; exponential back‑off on throttling.
- **Optimistic UI** for selections; reconcile on server responses.

---

## 10) Error Handling & Observability
- Network/auth errors surfaced inline with retry.
- Partial‑success handling (some items added, some skipped) with a **Results** panel.
- Structured logs: time, action, count of items added/removed, warnings.

---

## 11) Accessibility & Internationalization
- Full keyboard navigation; screen‑reader labels; color‑blind safe status icons.
- Text scaling, high‑contrast theme.
- String externalization for future i18n.

---

## 12) Privacy & Security
- Tokens stored encrypted at rest; never included in exports.
- Local‑first architecture; no cloud relay.
- Optional PIN to open the app.
- **Third‑party keys** (TMDB) stored securely; expose a UI to rotate keys; back off on rate‑limit errors.

---

## 13) Roadmap
**MVP (Weeks 1–3)**
- Auth to Plex & Tautulli; library browse; tree view with tri‑state; selection cart; static playlist create; dry run; runtime meter; duplicate guard.

**Beta (Weeks 4–6)**
- Quick picks; search + facets; templates (Catch‑Up Tonight, Season Sampler);
- Timebox builder; paste‑to‑add; CSV/JSON export.
- **TMDB enrichment** (posters/backdrops/keywords) with cache; basic holiday/theme detectors.

**v1.0 (Weeks 7–8)**
- Smart playlists (rule builder, auto‑refresh); interleave; multi‑user support; logs.
- **ID reconciliation** (Plex guid → TMDB id) and fallback title matching for stubborn items.

**v1.1+**
- Collections bridge; M3U export; advanced A11y; import from Trakt/PMM YAML; trending‑based templates (optional).

---

## 14) Success Metrics
- Time‑to‑playlist (median) from app open → create.
- Clicks per playlist created (median).
- % playlists created via templates or smart rules.
- Error rate and duplicate‑add rate.
- App startup time; tree expansion latency; thumbnail load hit‑rate.
- **TMDB cache hit‑rate**; **external call error/timeout rate**; **rate‑limit backoff events**.

---

## 15) Open Questions
1. Target platform(s): Windows first, or cross‑platform?
2. Preferred packaging: portable EXE vs installer.
3. Smart playlist persistence: Plex‑native constructs vs app‑managed with periodic sync.
4. How to handle specials and episode ordering for anime/alternates?
5. Do we surface collections as first‑class selection scopes in the tree?

---

## 16) Acceptance Criteria (v1.0)
- Users can create/update static and smart playlists against a Plex server.
- Tri‑state tree with posters (Show/Season) and greyscale episode thumbnails is performant on large libraries.
- Tautulli‑aware filters (unwatched, last watched, play counts) work per selected user.
- Dry‑run preview and logs accurately reflect server changes.
- Imports/exports function and preserve unique IDs for reliable round‑trips.

---

## 17) External Integrations: Plex API & TMDB (Design Notes)
**Plex API**
- **Preferred art source** when present; avoid extra calls by caching Plex image URLs by `ratingsKey`.
- **Playlists are authoritative**: always read‑back after write to confirm order and contents.
- **Hubs** (On Deck/Recently Added) can pre‑seed quick templates.

**TMDB API**
- Use for **keywords** (holiday/theme), **genres**, **networks**, and **art backfill** (posters, season art) when Plex images are missing/poor.
- Respect rate limits; use an **LRU cache** + on‑disk TTL cache (e.g., 24h) for TMDB responses.
- Provide settings to **disable TMDB** in offline/minimal mode.

**User Experience wins**
- Better posters improve the tree’s scannability.
- Keywords enable one‑click themed playlists (Halloween, Xmas, Bottle episodes list curated with a keyword file + TMDB data).

---

## 18) ID Mapping & Reconciliation (Plex ↔ TMDB)
- **Primary path:** read Plex item `guid` (e.g., tmdb://, tvdb://, imdb://, or plex:// agent forms). If it includes a TMDB id, use it directly.
- **Fallback path:** query TMDB by title + year + season/episode; apply fuzzy rules and prefer exact matches within the same show.
- **Persistence:** store `{ ratingsKey, guid, tmdbId?, tvdbId?, imdbId? }` in a local SQLite cache for instant reuse.
- **Conflict handling:** if multiple candidates match, present a one‑time resolve dialog and remember the choice.
- **Artwork policy:** prefer Plex images; use TMDB images only when Plex art is missing or low‑res; cache both with normalized sizes.

