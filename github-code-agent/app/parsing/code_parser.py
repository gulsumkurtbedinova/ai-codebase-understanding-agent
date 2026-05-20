from pathlib import Path


SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx"
]


def load_code_files(repo_path: str):

    repo = Path(repo_path)

    documents = []

    for file_path in repo.rglob("*"):

        if file_path.suffix in SUPPORTED_EXTENSIONS:

            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )

                documents.append({
                    "file_path": str(file_path),
                    "content": content
                })

            except Exception:
                pass

    return documents