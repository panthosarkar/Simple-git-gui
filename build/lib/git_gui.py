import sys
import subprocess
import os
import requests
from appdirs import user_config_dir

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QLabel, QListWidget,
    QTreeWidget, QTreeWidgetItem, QLineEdit, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie

class GitGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # For saving/loading GitHub token:
        # 1) Choose a config directory in the user's home
        self.config_dir = user_config_dir("SimpleGitGUI", "YourName")
        os.makedirs(self.config_dir, exist_ok=True)

        # 2) Create a path for the token file
        self.token_file = os.path.join(self.config_dir, "github_token.txt")

        # 3) Load the token if it exists
        self.github_token = None
        self.load_github_token()

        self.repo_path = None
        self.selected_branch = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Simple Git GUI with Animation")
        self.setGeometry(100, 100, 800, 600)
        main_layout = QVBoxLayout()

        # Animation label (spinner)
        self.animation_label = QLabel()
        # Load a spinner GIF (adjust path if needed)
        self.spinner_movie = QMovie("../resources/Loading_icon.gif")
        self.animation_label.setMovie(self.spinner_movie)
        # Hidden by default
        self.animation_label.setVisible(False)

        # -- Row 1: Repository Selection & Current Branch --
        repo_layout = QHBoxLayout()
        self.repo_label = QLabel("Select a Git repository", self)
        repo_layout.addWidget(self.repo_label)

        self.select_repo_btn = QPushButton("Select Repository", self)
        self.select_repo_btn.clicked.connect(self.select_repository)
        repo_layout.addWidget(self.select_repo_btn)

        self.current_branch_label = QLabel("Branch: N/A", self)
        repo_layout.addWidget(self.current_branch_label)

        main_layout.addLayout(repo_layout)

        # -- Row 2: Branch List & Commit Tree --
        row2_layout = QHBoxLayout()

        # Left: Branch list
        self.branch_list = QListWidget(self)
        self.branch_list.itemClicked.connect(self.select_branch)
        row2_layout.addWidget(self.branch_list, stretch=1)

        # Right: Commit history tree
        self.commit_tree = QTreeWidget()
        self.commit_tree.setColumnCount(1)
        self.commit_tree.setHeaderLabels(["Commit History"])
        row2_layout.addWidget(self.commit_tree, stretch=2)

        main_layout.addLayout(row2_layout)

        # -- Row 3: Output Text --
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        main_layout.addWidget(self.output)

        # -- Row 4: Git Action Buttons --
        action_layout = QHBoxLayout()

        self.fetch_btn = QPushButton("Fetch", self)
        self.fetch_btn.clicked.connect(lambda: self.run_git_command("git fetch"))
        self.fetch_btn.setEnabled(False)
        action_layout.addWidget(self.fetch_btn)

        self.pull_btn = QPushButton("Pull", self)
        self.pull_btn.clicked.connect(lambda: self.run_git_command("git pull"))
        self.pull_btn.setEnabled(False)
        action_layout.addWidget(self.pull_btn)

        self.merge_btn = QPushButton("Merge Selected Branch", self)
        self.merge_btn.clicked.connect(self.merge_selected_branch)
        self.merge_btn.setEnabled(False)
        action_layout.addWidget(self.merge_btn)

        main_layout.addLayout(action_layout)

        # -- Row 5: Commit & Push --
        commit_layout = QHBoxLayout()

        self.commit_msg_input = QLineEdit()
        self.commit_msg_input.setPlaceholderText("Enter commit message...")
        commit_layout.addWidget(self.commit_msg_input)

        self.commit_btn = QPushButton("Commit")
        self.commit_btn.clicked.connect(self.commit_changes)
        self.commit_btn.setEnabled(False)
        commit_layout.addWidget(self.commit_btn)

        self.push_btn = QPushButton("Push")
        self.push_btn.clicked.connect(self.push_changes)
        self.push_btn.setEnabled(False)
        commit_layout.addWidget(self.push_btn)

        main_layout.addLayout(commit_layout)

        # -- Row 6: Clone new repo --
        clone_layout = QHBoxLayout()
        self.clone_url_input = QLineEdit()
        self.clone_url_input.setPlaceholderText("Enter Git clone URL...")
        clone_layout.addWidget(self.clone_url_input)

        self.clone_btn = QPushButton("Clone")
        self.clone_btn.clicked.connect(self.clone_repository)
        clone_layout.addWidget(self.clone_btn)

        main_layout.addLayout(clone_layout)

        # -- Row 7: GitHub Repos (User & Orgs) --
        github_layout = QHBoxLayout()

        self.github_btn = QPushButton("Set GitHub Token")
        self.github_btn.clicked.connect(self.set_github_token)
        github_layout.addWidget(self.github_btn)

        self.list_repos_btn = QPushButton("List My Repos")
        self.list_repos_btn.clicked.connect(self.list_github_repos)
        github_layout.addWidget(self.list_repos_btn)

        self.list_orgs_btn = QPushButton("List My Org Repos")
        self.list_orgs_btn.clicked.connect(self.list_org_repos)
        github_layout.addWidget(self.list_orgs_btn)

        main_layout.addLayout(github_layout)

        # Finally, add our animation label at the bottom
        main_layout.addWidget(self.animation_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    # ------------ Show/Hide Animation ------------
    def show_animation(self, show: bool):
        if show:
            self.animation_label.setVisible(True)
            self.spinner_movie.start()
        else:
            self.animation_label.setVisible(False)
            self.spinner_movie.stop()

    # ------------------- Repository Selection -------------------
    def select_repository(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Git Repository")
        if folder and os.path.exists(os.path.join(folder, ".git")):
            self.repo_path = folder
            self.repo_label.setText(f"Repository: {folder}")
            self.enable_git_buttons(True)
            self.load_branches()
            self.fetch_current_branch()
            self.fetch_commits()
        else:
            self.output.append("Error: Selected folder is not a Git repository!")

    def enable_git_buttons(self, enable: bool):
        self.fetch_btn.setEnabled(enable)
        self.pull_btn.setEnabled(enable)
        self.merge_btn.setEnabled(enable)
        self.commit_btn.setEnabled(enable)
        self.push_btn.setEnabled(enable)

    # ------------------- Branch Management -------------------
    def load_branches(self):
        if not self.repo_path:
            return
        try:
            self.show_animation(True)
            result = subprocess.run(
                ["git", "branch", "--list"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            branches = result.stdout.strip().split("\n")
            self.branch_list.clear()
            for branch in branches:
                self.branch_list.addItem(branch.strip())
        except subprocess.CalledProcessError as e:
            self.output.append(f"Error: {e.stderr}")
        finally:
            self.show_animation(False)

    def select_branch(self, item):
        self.selected_branch = item.text().replace("*", "").strip()
        self.output.append(f"Selected Branch: {self.selected_branch}")

    def fetch_current_branch(self):
        if not self.repo_path:
            return
        try:
            self.show_animation(True)
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = result.stdout.strip()
            self.current_branch_label.setText(f"Branch: {current_branch}")
        except subprocess.CalledProcessError as e:
            self.output.append(f"Error: {e.stderr}")
        finally:
            self.show_animation(False)

    # ------------------- Merge Branch -------------------
    def merge_selected_branch(self):
        if not self.repo_path or not self.selected_branch:
            self.output.append("Error: No branch selected for merging!")
            return
        self.run_git_command(f"git merge {self.selected_branch}")

    # ------------------- Commit & Push -------------------
    def commit_changes(self):
        if not self.repo_path:
            self.output.append("Error: No repository selected!")
            return
        message = self.commit_msg_input.text().strip()
        if not message:
            self.output.append("Error: Commit message cannot be empty!")
            return
        command = ["git", "commit", "-am", message]
        self.show_animation(True)
        try:
            result = subprocess.run(
                command, cwd=self.repo_path,
                capture_output=True, text=True, check=True
            )
            self.output.append(f"> {' '.join(command)}\n{result.stdout}")
            self.commit_msg_input.clear()
            self.fetch_commits()
        except subprocess.CalledProcessError as e:
            self.output.append(f"> {' '.join(command)}\nError: {e.stderr}")
        finally:
            self.show_animation(False)

    def push_changes(self):
        if not self.repo_path:
            self.output.append("Error: No repository selected!")
            return
        command = ["git", "push", "origin", self.current_branch_label.text().replace("Branch: ", "")]
        self.show_animation(True)
        try:
            result = subprocess.run(
                command, cwd=self.repo_path,
                capture_output=True, text=True, check=True
            )
            self.output.append(f"> {' '.join(command)}\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output.append(f"> {' '.join(command)}\nError: {e.stderr}")
        finally:
            self.show_animation(False)

    # ------------------- Clone Repository -------------------
    def clone_repository(self):
        clone_url = self.clone_url_input.text().strip()
        if not clone_url:
            self.output.append("Error: Clone URL is empty!")
            return
        target_dir = QFileDialog.getExistingDirectory(self, "Select Folder to Clone Into")
        if not target_dir:
            self.output.append("Error: No folder selected!")
            return
        command = ["git", "clone", clone_url]
        self.show_animation(True)
        try:
            result = subprocess.run(
                command, cwd=target_dir,
                capture_output=True, text=True, check=True
            )
            self.output.append(f"> {' '.join(command)}\n{result.stdout}")
            self.clone_url_input.clear()
        except subprocess.CalledProcessError as e:
            self.output.append(f"> {' '.join(command)}\nError: {e.stderr}")
        finally:
            self.show_animation(False)

    # ------------------- Commit Tree (Git Log) -------------------
    def fetch_commits(self):
        if not self.repo_path:
            return
        self.commit_tree.clear()
        self.show_animation(True)
        try:
            result = subprocess.run(
                ["git", "log", "--graph", "--pretty=format:%h - %s (%cr) <%an>", "--abbrev-commit"],
                cwd=self.repo_path,
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().split("\n")
            for line in lines:
                item = QTreeWidgetItem([line])
                self.commit_tree.addTopLevelItem(item)
        except subprocess.CalledProcessError as e:
            self.output.append(f"Error: {e.stderr}")
        finally:
            self.show_animation(False)

    # ------------------- Git Command Runner -------------------
    def run_git_command(self, command):
        if not self.repo_path:
            self.output.append("Error: No repository selected!")
            return
        if isinstance(command, str):
            command = command.split()
        self.show_animation(True)
        try:
            result = subprocess.run(
                command, cwd=self.repo_path,
                capture_output=True, text=True, check=True
            )
            self.output.append(f"> {' '.join(command)}\n{result.stdout}")
            self.load_branches()
            self.fetch_current_branch()
            self.fetch_commits()
        except subprocess.CalledProcessError as e:
            self.output.append(f"> {' '.join(command)}\nError: {e.stderr}")
        finally:
            self.show_animation(False)

    # ------------------- Save / Load Token -------------------
    def load_github_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r", encoding="utf-8") as f:
                self.github_token = f.read().strip()

    def save_github_token(self):
        if self.github_token:
            with open(self.token_file, "w", encoding="utf-8") as f:
                f.write(self.github_token)

    def set_github_token(self):
        token, ok = QInputDialog.getText(self, "GitHub Token", "Enter your GitHub personal access token:")
        if ok and token:
            self.github_token = token
            self.save_github_token()
            self.output.append("GitHub token set and saved.")
        else:
            self.output.append("GitHub token not set.")

    # ------------------- GitHub Integration -------------------
    def list_github_repos(self):
        if not self.github_token:
            self.output.append("Error: GitHub token is not set.")
            return
        url = "https://api.github.com/user/repos"
        headers = {"Authorization": f"token {self.github_token}"}
        self.show_animation(True)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            repos = response.json()
            self.output.append("---- My GitHub Repositories ----")
            for r in repos:
                self.output.append(f"{r['full_name']} (Private: {r['private']})")
        except requests.RequestException as e:
            self.output.append(f"Error fetching user repos: {e}")
        finally:
            self.show_animation(False)

    def list_org_repos(self):
        if not self.github_token:
            self.output.append("Error: GitHub token is not set.")
            return
        headers = {"Authorization": f"token {self.github_token}"}
        orgs_url = "https://api.github.com/user/orgs"
        self.show_animation(True)
        try:
            orgs_resp = requests.get(orgs_url, headers=headers)
            orgs_resp.raise_for_status()
            orgs = orgs_resp.json()
            self.output.append("---- Organization Repositories ----")
            for org in orgs:
                org_name = org["login"]
                repos_url = f"https://api.github.com/orgs/{org_name}/repos"
                repos_resp = requests.get(repos_url, headers=headers)
                repos_resp.raise_for_status()
                repos_data = repos_resp.json()
                self.output.append(f"\nOrg: {org_name}")
                for r in repos_data:
                    self.output.append(f"  {r['full_name']} (Private: {r['private']})")
        except requests.RequestException as e:
            self.output.append(f"Error fetching org repos: {e}")
        finally:
            self.show_animation(False)

def main():
    app = QApplication(sys.argv)
    window = GitGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

