"""Git repository handler with secure credential management."""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass
import logging

try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logging.warning("GitPython not available, repository cloning disabled")


@dataclass
class RepositoryContext:
    """Context information for a repository."""

    local_path: str
    is_temp: bool
    commit_hash: str
    branch: str
    total_files: int
    total_lines: int


class RepositoryHandler:
    """Handles Git repository operations with secure credential handling."""

    def __init__(self, clone_timeout: int = 300):
        self.clone_timeout = clone_timeout
        self.logger = logging.getLogger(__name__)

    def prepare_repository(
        self,
        repository_url: Optional[str] = None,
        local_path: Optional[str] = None,
        branch: str = "main",
    ) -> RepositoryContext:
        """
        Prepare repository for analysis.

        Args:
            repository_url: URL to clone from (if remote)
            local_path: Path to local repository
            branch: Target branch name

        Returns:
            RepositoryContext with repository information
        """
        if local_path:
            return self._prepare_local_repository(local_path, branch)
        elif repository_url:
            return self._prepare_remote_repository(repository_url, branch)
        else:
            raise ValueError("Either repository_url or local_path must be provided")

    def _prepare_local_repository(self, local_path: str, branch: str) -> RepositoryContext:
        """Prepare a local repository for analysis."""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local path does not exist: {local_path}")

        # Get commit hash if it's a git repository
        commit_hash = "local"
        if GIT_AVAILABLE and os.path.exists(os.path.join(local_path, ".git")):
            try:
                repo = Repo(local_path)
                commit_hash = repo.head.commit.hexsha[:8]
                branch = repo.active_branch.name
            except Exception as e:
                self.logger.warning(f"Could not access git info: {e}")

        total_files, total_lines = self._count_files_and_lines(local_path)

        return RepositoryContext(
            local_path=local_path,
            is_temp=False,
            commit_hash=commit_hash,
            branch=branch,
            total_files=total_files,
            total_lines=total_lines,
        )

    def _prepare_remote_repository(self, repository_url: str, branch: str) -> RepositoryContext:
        """Clone and prepare a remote repository."""
        if not GIT_AVAILABLE:
            raise RuntimeError("GitPython is required for remote repository cloning")

        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="code_review_")
        self.logger.info(f"Cloning repository to {temp_dir}")

        try:
            # Sanitize URL for logging (remove credentials)
            safe_url = self._sanitize_url_for_logging(repository_url)
            self.logger.info(f"Cloning from {safe_url}")

            # Clone repository with timeout
            repo = Repo.clone_from(
                repository_url,
                temp_dir,
                branch=branch,
                depth=1,  # Shallow clone for faster performance
            )

            commit_hash = repo.head.commit.hexsha[:8]
            total_files, total_lines = self._count_files_and_lines(temp_dir)

            return RepositoryContext(
                local_path=temp_dir,
                is_temp=True,
                commit_hash=commit_hash,
                branch=branch,
                total_files=total_files,
                total_lines=total_lines,
            )

        except GitCommandError as e:
            self.logger.error(f"Failed to clone repository: {e}")
            self._cleanup_temp_directory(temp_dir)
            raise RuntimeError(f"Failed to clone repository: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error cloning repository: {e}")
            self._cleanup_temp_directory(temp_dir)
            raise

    def _sanitize_url_for_logging(self, url: str) -> str:
        """Remove credentials from URL for safe logging."""
        # Pattern: https://user:pass@github.com -> https://***@github.com
        if "@" in url and "://" in url:
            protocol, rest = url.split("://", 1)
            if "@" in rest:
                credentials, host = rest.rsplit("@", 1)
                return f"{protocol}://***@{host}"
        return url

    def _count_files_and_lines(self, path: str) -> Tuple[int, int]:
        """Count total files and lines in repository."""
        total_files = 0
        total_lines = 0

        # Extensions to analyze
        code_extensions = {".py", ".js", ".ts", ".java", ".go", ".rb", ".cpp", ".c", ".h"}

        for root, dirs, files in os.walk(path):
            # Skip common non-code directories
            dirs[:] = [
                d
                for d in dirs
                if d
                not in {
                    ".git",
                    "node_modules",
                    "__pycache__",
                    ".venv",
                    "venv",
                    "build",
                    "dist",
                }
            ]

            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)

                if ext in code_extensions:
                    total_files += 1
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            total_lines += sum(1 for _ in f)
                    except Exception as e:
                        self.logger.warning(f"Could not read file {file_path}: {e}")

        return total_files, total_lines

    def get_changed_files(
        self, repo_path: str, base_branch: str = "main", target_branch: str = "HEAD"
    ) -> List[str]:
        """Get list of changed files for incremental analysis."""
        if not GIT_AVAILABLE:
            self.logger.warning("GitPython not available, returning all files")
            return self._get_all_code_files(repo_path)

        try:
            repo = Repo(repo_path)
            diff = repo.git.diff(f"{base_branch}..{target_branch}", name_only=True)
            changed_files = diff.split("\n") if diff else []
            return [os.path.join(repo_path, f) for f in changed_files if f]
        except Exception as e:
            self.logger.warning(f"Could not get diff, returning all files: {e}")
            return self._get_all_code_files(repo_path)

    def _get_all_code_files(self, repo_path: str) -> List[str]:
        """Get all code files in repository."""
        code_files = []
        code_extensions = {".py", ".js", ".ts", ".java", ".go"}

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [
                d
                for d in dirs
                if d not in {".git", "node_modules", "__pycache__", ".venv", "venv"}
            ]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext in code_extensions:
                    code_files.append(os.path.join(root, file))

        return code_files

    def cleanup(self, context: RepositoryContext):
        """Clean up temporary repository if needed."""
        if context.is_temp and os.path.exists(context.local_path):
            self._cleanup_temp_directory(context.local_path)

    def _cleanup_temp_directory(self, path: str):
        """Safely remove temporary directory."""
        try:
            shutil.rmtree(path)
            self.logger.info(f"Cleaned up temporary directory: {path}")
        except Exception as e:
            self.logger.warning(f"Could not clean up temporary directory {path}: {e}")
