from pathlib import Path
from git import Repo


REPOS_DIR = Path("repos")


def clone_repository(repo_url: str) -> str:

    repo_name = repo_url.split("/")[-1].replace(".git", "")

    local_path = REPOS_DIR / repo_name

    if local_path.exists():
        return str(local_path)

    Repo.clone_from(repo_url, local_path)

    return str(local_path)