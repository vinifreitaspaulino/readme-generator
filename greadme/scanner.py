from pathlib import Path

IGNORE_DIRS = {
    # Python
    "__pycache__", ".venv", "venv", "env", ".env",
    "*.egg-info", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    # Node
    "node_modules", ".next", ".nuxt", "dist", "build",
    # Git / CI
    ".git", ".github", ".gitlab",
    # IDEs
    ".vscode", ".idea",
    # Misc
    ".DS_Store", "tmp", "temp", "logs",
}

IGNORE_EXTENSIONS = {
    # Binaries
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".pdf", ".zip", ".tar", ".gz",
    # Comp
    ".pyc", ".pyo", ".exe", ".dll", ".so"

}

IGNORE_FILES = {
    "package-lock.json",
    "yarn.lock",
    "poetry.lock",
    "uv.lock",
    ".DS_Store",
    "Thumbs.db",
}

def should_ignore(item: Path) -> bool:
    if item.name in IGNORE_DIRS and item.is_dir():
        return True
    if item.name in IGNORE_FILES:
        return True
    if item.suffix in IGNORE_EXTENSIONS:
        return True
    if item.name.startswith(".") and item.is_dir():
        return True
    return False


def scan(path: Path) -> dict:
    return {
        "name": get_name(path),
        "structure": get_tree(path),
        # "dependencies": get_dependencies(path),
        # "description": get_description(path) 
    }

def get_name(path: Path) -> str:
    return path.resolve().name

def get_tree(path: Path, prefix: str = "") -> str:
    lines = []
    for item in sorted(path.iterdir()):
        if should_ignore(item):
            continue
        lines.append(f"{prefix}{item.name}")

        if item.is_dir():
            lines.append(get_tree(item, prefix + "  "))
    return "\n".join(lines)