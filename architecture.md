# Simple Git GUI — Architecture

## 1. Project Goal

Build a modern Linux desktop Git client with a frontend experience inspired by GitHub Desktop, implemented with:

- React / Next.js frontend
- Tailwind CSS styling
- Python + FastAPI backend
- Native Git CLI for local Git operations
- GitHub App authentication for direct GitHub login
- GitHub REST API for personal and organization repositories
- Optional Tauri desktop shell for production packaging

The application must support:

1. Personal GitHub repositories
2. Organization repositories the authenticated user has permission to access

Core workflows include clone, fetch, pull, inspect changes, stage, unstage, commit, branch switching, merge, history, and push.

---

## 2. Core Architecture

```text
Desktop Application
│
├── React / Next.js + Tailwind Frontend
│   ├── GitHub Login
│   ├── Repository Browser
│   ├── Organization Browser
│   ├── Branch Selector
│   ├── Changes Panel
│   ├── Diff Viewer
│   ├── Commit Panel
│   ├── Commit History
│   └── Sync Controls
│
└── Python FastAPI Backend
    ├── Auth Service
    ├── Git Service
    ├── GitHub Service
    └── Repository Service
        │
        ├── Native Git CLI
        └── GitHub REST API
```

---

## 3. Recommended Project Structure

```text
Simple-git-gui/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── repositories.py
│   │   │   ├── git.py
│   │   │   ├── branches.py
│   │   │   └── github.py
│   │   ├── services/
│   │   │   ├── git_service.py
│   │   │   ├── github_service.py
│   │   │   ├── auth_service.py
│   │   │   └── repository_service.py
│   │   ├── models/
│   │   │   ├── git_models.py
│   │   │   ├── github_models.py
│   │   │   └── auth_models.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── paths.py
│   │   └── storage/
│   │       └── local_state.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   └── dashboard/page.tsx
│   ├── components/
│   │   ├── layout/
│   │   ├── repositories/
│   │   ├── git/
│   │   └── ui/
│   ├── lib/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── constants.ts
│   ├── public/
│   ├── package.json
│   └── tailwind.config.ts
│
├── legacy/
│   └── src/
│       └── git_gui.py
│
├── resources/
├── architecture.md
├── phases.md
├── README.md
└── TODO.md
```

---

## 4. Frontend Responsibilities

The frontend handles presentation and user interaction only.

### Authentication
- Continue with GitHub
- Logged-in user profile
- Logout
- Authentication status

### Repository Navigation
- Personal repositories
- Organizations
- Organization repositories
- Local repositories
- Clone repository
- Add existing repository

### Repository Workspace
- Current repository
- Current branch
- Incoming/outgoing status
- Changed files
- Added, modified, deleted, renamed and untracked states

### Diff Viewer
- Line numbers
- Added/removed highlighting
- Staged/unstaged state
- File path
- Binary file handling

### Commit Workflow
- Select files
- Stage/unstage
- Commit summary
- Commit description
- Commit action

### History
- Commit SHA
- Subject
- Author
- Date
- Branch badges
- Visual graph later

---

## 5. Backend Responsibilities

The Python backend owns all application logic.

### Git Service

Wrap native Git safely using subprocess argument arrays.

Core commands include:

```text
git status --porcelain=v1
git diff
git diff --cached
git add
git restore --staged
git commit
git fetch
git pull
git push
git branch
git switch
git merge
git log
git rev-list
git remote
git clone
```

### GitHub Service

Responsible for:

- Current GitHub user
- Organizations
- Personal repositories
- Organization repositories
- Repository metadata
- Repository permissions
- Default branch
- Clone URLs
- GitHub App installation state

### Authentication Service

Responsible for:

- Starting GitHub login
- OAuth/GitHub App callback
- Token exchange
- Secure credential storage
- Session validation
- Logout

---

## 6. GitHub Authentication Architecture

Preferred approach:

**GitHub App + user authorization**

```text
App
↓
Continue with GitHub
↓
GitHub authorization
↓
Callback to FastAPI
↓
Code exchanged for token
↓
Secure backend session
↓
Load user, personal repos and organizations
```

Organization access must respect:

- User permissions
- Organization permissions
- GitHub App installation permissions
- Repository restrictions
- Protected branches

---

## 7. Pull / Push Authentication

GitHub API authentication and Git transport authentication are separate concerns.

Initial recommended approach:

```text
GitHub API → GitHub App login
Git clone/pull/push → existing system Git/SSH credentials
```

Later, authenticated HTTPS transport can be added if needed.

---

## 8. Initial Backend API

```text
GET  /api/health

GET  /api/auth/github/login
GET  /api/auth/github/callback
GET  /api/auth/me
POST /api/auth/logout

GET  /api/github/organizations
GET  /api/github/repositories
GET  /api/github/organizations/{org}/repositories

GET  /api/repositories
POST /api/repositories/open
POST /api/repositories/clone
GET  /api/repositories/current

GET  /api/git/status
GET  /api/git/changes
GET  /api/git/diff
GET  /api/git/history

POST /api/git/stage
POST /api/git/unstage
POST /api/git/commit
POST /api/git/fetch
POST /api/git/pull
POST /api/git/push

GET  /api/branches
POST /api/branches/create
POST /api/branches/switch
POST /api/branches/merge
```

---

## 9. Security Rules

1. Never store GitHub tokens in plain-text files.
2. Keep secrets in the backend.
3. Validate repository paths.
4. Never use `shell=True` for Git commands.
5. Never build raw shell commands from frontend input.
6. Validate branch names and file paths.
7. Respect GitHub permissions.
8. Never force-push automatically.
9. Never discard local changes automatically.
10. Require confirmation for destructive operations.
11. Do not hide merge conflicts.
12. Never log access tokens.

---

## 10. Local Application State

Safe local state may include:

- Recent repositories
- Current repository
- Theme
- Last organization
- Last selected branch
- UI layout preferences

Authentication secrets must be stored separately and securely.

---

## 11. UI Direction

The visual direction should be:

- GitHub Desktop-inspired workflow
- React/Tailwind quality
- Dark-first interface
- Colorful status indicators
- Smooth transitions
- Real icons
- No ASCII commit graphs
- GitHub-style diff viewer
- Resizable panels

Suggested status colors:

```text
Green  → added / success / push
Orange → modified
Red    → deleted / conflict / error
Blue   → branch / active selection
Purple → organization / remote
Gray   → neutral / inactive
```

---

## 12. Desktop Packaging

Development:

```text
Next.js dev server
+
FastAPI dev server
```

Production target:

```text
Tauri Desktop Shell
↓
React frontend
↓
Local Python backend
↓
Git + GitHub
```

Tauri should be added only after the core Git workflow is stable.

---

## 13. Legacy PyQt Application

The existing PyQt application should be preserved at:

```text
legacy/src/git_gui.py
```

Useful Git logic will be extracted and rewritten into backend services.

The PyQt UI will not be the production frontend.

---

## 14. MVP Definition

The MVP is complete when a Linux user can:

1. Sign in with GitHub.
2. See personal repositories.
3. See organizations.
4. See accessible organization repositories.
5. Clone repositories.
6. Open local repositories.
7. See current branch.
8. See changed files.
9. View visual diffs.
10. Stage and unstage files.
11. Commit selected files.
12. Fetch.
13. Pull.
14. Push.
15. Switch branches.
16. See commit history.
17. See incoming/outgoing counts.

---

## 15. Non-MVP Features

Do not implement until the core workflow is reliable:

- Pull requests
- Issues
- GitHub Actions
- Interactive rebase
- Cherry-pick
- Revert UI
- Stash manager
- Tags/releases
- Built-in conflict editor
- Multiple accounts
- Multiple remotes UI
- Repository settings editor
