# Simple Git GUI — Development Phases

## Status Legend

- [ ] Not started
- [~] In progress
- [x] Completed
- [!] Blocked

---

# Phase 0 — Preserve Existing Application

**Goal:** Protect the current PyQt implementation before restructuring.

- [ ] Create `legacy/`
- [ ] Move current `src/` to `legacy/src/`
- [ ] Verify legacy code is preserved
- [ ] Commit current project state
- [x] Create `architecture.md`
- [x] Create `phases.md`

### Exit Criteria

Existing PyQt code is preserved and the new architecture is documented.

---

# Phase 1 — Project Restructure

**Goal:** Establish frontend/backend separation.

- [ ] Create `backend/`
- [ ] Create `frontend/`
- [ ] Create backend package structure
- [ ] Add `requirements.txt`
- [ ] Add `.env.example`
- [ ] Update `.gitignore`
- [ ] Verify repository remains usable

### Exit Criteria

Frontend and backend can be developed independently.

---

# Phase 2 — Python Git Backend

**Goal:** Extract Git logic from the old PyQt application.

Implement:

- [ ] Validate repository
- [ ] Open repository
- [ ] Get current branch
- [ ] List branches
- [ ] Get repository status
- [ ] List changed files
- [ ] Read unstaged diff
- [ ] Read staged diff
- [ ] Stage file
- [ ] Unstage file
- [ ] Commit selected files
- [ ] Fetch
- [ ] Pull
- [ ] Push
- [ ] Clone
- [ ] Commit history
- [ ] Ahead/behind counts
- [ ] Remote detection
- [ ] Conflict detection

### Safety

- [ ] No `shell=True`
- [ ] Validate repository paths
- [ ] Validate branch names
- [ ] Structured errors
- [ ] No automatic force push
- [ ] No automatic destructive cleanup

### Exit Criteria

Python can perform all core Git operations without any UI.

---

# Phase 3 — FastAPI Layer

**Goal:** Expose Git operations through HTTP.

- [ ] `GET /api/health`
- [ ] `POST /api/repositories/open`
- [ ] `GET /api/repositories/current`
- [ ] `POST /api/repositories/clone`
- [ ] `GET /api/git/status`
- [ ] `GET /api/git/changes`
- [ ] `GET /api/git/diff`
- [ ] `GET /api/git/history`
- [ ] `POST /api/git/stage`
- [ ] `POST /api/git/unstage`
- [ ] `POST /api/git/commit`
- [ ] `POST /api/git/fetch`
- [ ] `POST /api/git/pull`
- [ ] `POST /api/git/push`
- [ ] `GET /api/branches`
- [ ] `POST /api/branches/create`
- [ ] `POST /api/branches/switch`
- [ ] `POST /api/branches/merge`

### Exit Criteria

Core Git actions work through FastAPI.

---

# Phase 4 — React / Next.js Frontend Foundation

**Goal:** Create the new visual client.

- [ ] Initialize Next.js
- [ ] Add TypeScript
- [ ] Add Tailwind CSS
- [ ] Configure API client
- [ ] Create dark theme
- [ ] Create application shell
- [ ] Create top bar
- [ ] Create sidebar
- [ ] Create repository workspace
- [ ] Create status bar
- [ ] Add icons
- [ ] Add toasts
- [ ] Add loaders

### Components

- [ ] `TopBar`
- [ ] `Sidebar`
- [ ] `RepositorySelector`
- [ ] `BranchSelector`
- [ ] `ChangesPanel`
- [ ] `DiffViewer`
- [ ] `CommitPanel`
- [ ] `CommitHistory`
- [ ] `SyncControls`
- [ ] `StatusBar`

### Exit Criteria

The frontend looks like a modern desktop Git client and communicates with FastAPI.

---

# Phase 5 — GitHub Direct Login

**Goal:** Replace manual token entry.

Preferred approach:

**GitHub App + user authorization**

- [ ] Create GitHub App
- [ ] Configure callback URL
- [ ] Configure required permissions
- [ ] Implement login route
- [ ] Implement callback
- [ ] Exchange authorization code
- [ ] Secure credential storage
- [ ] Backend session handling
- [ ] `/api/auth/me`
- [ ] Logout
- [ ] Login page
- [ ] `Continue with GitHub`
- [ ] Show authenticated profile

### Exit Criteria

User signs in without manually pasting a token.

---

# Phase 6 — Personal Repository Integration

- [ ] Fetch authenticated user
- [ ] Fetch personal repositories
- [ ] Read repository permissions
- [ ] Read default branch
- [ ] Get clone URLs
- [ ] Personal repository UI
- [ ] Repository search
- [ ] Clone action
- [ ] Open on GitHub action

### Exit Criteria

User can browse and clone personal repositories.

---

# Phase 7 — Organization Repository Integration

- [ ] Fetch organizations
- [ ] Detect GitHub App installation access
- [ ] Fetch organization repositories
- [ ] Read repository permissions
- [ ] Detect read-only repositories
- [ ] Detect write-access repositories
- [ ] Organization selector
- [ ] Organization repository browser
- [ ] Permission indicators
- [ ] Clone organization repository
- [ ] Disable push for read-only repositories

### Exit Criteria

User can work with authorized organization repositories.

---

# Phase 8 — Complete Changes Workflow

### Changed Files

- [ ] Visual file list
- [ ] Added state
- [ ] Modified state
- [ ] Deleted state
- [ ] Renamed state
- [ ] Untracked state
- [ ] File selection
- [ ] Select all/deselect all

### Diff Viewer

- [ ] Added-line highlighting
- [ ] Removed-line highlighting
- [ ] Line numbers
- [ ] Staged/unstaged indicator
- [ ] File header
- [ ] Large diff handling
- [ ] Binary file handling

### Commit

- [ ] Summary
- [ ] Description
- [ ] Stage selected files
- [ ] Commit
- [ ] Refresh
- [ ] Validation

### Exit Criteria

User can review and commit selected changes safely.

---

# Phase 9 — Fetch / Pull / Push Workflow

- [ ] Fetch button
- [ ] Pull button
- [ ] Push button
- [ ] Sync button
- [ ] Incoming count
- [ ] Outgoing count
- [ ] Remote display
- [ ] Upstream branch display
- [ ] Authentication errors
- [ ] Permission errors
- [ ] Protected branch errors
- [ ] Pull conflict handling
- [ ] Network error handling
- [ ] Progress UI

### Exit Criteria

Remote synchronization works reliably for personal and organization repositories.

---

# Phase 10 — Branch Management

- [ ] List branches
- [ ] Current branch indicator
- [ ] Switch branch
- [ ] Create branch
- [ ] Delete local branch
- [ ] Fetch remote branches
- [ ] Checkout remote branch
- [ ] Merge branch
- [ ] Warn about local changes
- [ ] Detect conflicts

### Exit Criteria

Normal branch workflows work without a terminal.

---

# Phase 11 — Visual Commit History

- [ ] Commit list
- [ ] SHA
- [ ] Author
- [ ] Timestamp
- [ ] Commit message
- [ ] Changed-file summary
- [ ] Branch badges
- [ ] Remote badges
- [ ] Visual commit graph
- [ ] Graph lanes
- [ ] Merge connections
- [ ] Commit details

### Exit Criteria

Commit history is fully graphical, not ASCII-based.

---

# Phase 12 — UX / Styling Pass

- [ ] Dark theme
- [ ] Optional light theme
- [ ] Colorful status indicators
- [ ] Smooth transitions
- [ ] Resizable panes
- [ ] Icons
- [ ] Keyboard shortcuts
- [ ] Empty states
- [ ] Error states
- [ ] Toasts
- [ ] Confirmation modals
- [ ] Skeleton loading
- [ ] Responsive layout
- [ ] Repository icons
- [ ] Organization avatars

### Exit Criteria

The application feels like a production desktop client.

---

# Phase 13 — Local State & Settings

Store:

- [ ] Recent repositories
- [ ] Current repository
- [ ] Last organization
- [ ] Theme
- [ ] Window/layout preferences
- [ ] Workspace state

Never store:

- [ ] Plain-text GitHub token
- [ ] Plain-text password

### Exit Criteria

Normal app state persists safely across restarts.

---

# Phase 14 — Desktop Packaging

Preferred shell:

**Tauri**

- [ ] Add Tauri
- [ ] Package React frontend
- [ ] Launch Python backend automatically
- [ ] Detect backend startup
- [ ] Stop backend on exit
- [ ] Bundle icon
- [ ] Add `.desktop` launcher
- [ ] Create Linux package
- [ ] Test clean installation
- [ ] Test upgrade flow

### Exit Criteria

One desktop app launches without manual server commands.

---

# Phase 15 — Testing & Hardening

### Functional Tests

- [ ] Clean repo
- [ ] Modified repo
- [ ] New files
- [ ] Deleted files
- [ ] Detached HEAD
- [ ] No remote
- [ ] Multiple branches
- [ ] Incoming commits
- [ ] Outgoing commits
- [ ] Merge conflicts
- [ ] Authentication failure
- [ ] Read-only org repository
- [ ] Protected branch
- [ ] Large repository

### Security Tests

- [ ] Path traversal
- [ ] Malicious branch names
- [ ] Shell injection
- [ ] Credential leakage
- [ ] Token logging
- [ ] Unsafe repository path
- [ ] Destructive operations

### Exit Criteria

Core workflows are safe for daily use.

---

# Phase 16 — MVP Release

- [ ] GitHub direct login
- [ ] Personal repositories
- [ ] Organization repositories
- [ ] Clone
- [ ] Open local repo
- [ ] Changes
- [ ] Visual diff
- [ ] Stage/unstage
- [ ] Commit
- [ ] Fetch
- [ ] Pull
- [ ] Push
- [ ] Branch switching
- [ ] Commit history
- [ ] Ahead/behind indicator
- [ ] Production Linux desktop package

### Exit Criteria

The app can replace a normal GitHub Desktop-style daily workflow on Linux.

---

# Phase 17 — Post-MVP

Only after MVP stability:

- [ ] Pull requests
- [ ] GitHub Issues
- [ ] GitHub Actions
- [ ] Stashes
- [ ] Tags
- [ ] Releases
- [ ] Cherry-pick
- [ ] Revert
- [ ] Interactive rebase
- [ ] Built-in conflict editor
- [ ] Multi-account support
- [ ] Multiple remotes
- [ ] Repository settings
- [ ] Commit signing
- [ ] Git LFS status
- [ ] Notifications

---

# Current Priority

```text
Phase 0
↓
Phase 1
↓
Phase 2
↓
Phase 3
↓
Phase 4
↓
Phase 5
```

Do not start advanced GitHub features until the local Git backend and frontend/API boundary are stable.
