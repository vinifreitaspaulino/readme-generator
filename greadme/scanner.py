from pathlib import Path
import json
import tomllib  # pip install toml
import xml.etree.ElementTree as ET  # built-in for XML parsing
from typing import List, Dict, Any, Set

IGNORE_DIRS: Set[str] = {
    "assets", "public",

    # Python
    "__pycache__", ".venv", "venv", "env", ".env",
    ".egg-info", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", ".nox", ".hypothesis", ".coverage",

    # Node / JS / TS
    "node_modules", ".next", ".nuxt", "dist", "build",
    ".cache", ".turbo", "coverage",

    # Rust
    "target",

    # Go
    "vendor", "bin",

    # Java / Kotlin / Gradle / Maven
    ".gradle", ".mvn", "out",

    # Ruby
    ".bundle",

    # C# / .NET
    "obj", "packages",

    # Git / Version Control / CI
    ".git", ".github", ".gitlab", ".svn", ".hg",
    ".circleci", ".travis",

    # IDEs / Editors
    ".vscode", ".idea", ".eclipse", ".settings",
    ".metadata",

    # Databases / Caches
    ".db", "db", "data", ".redis", ".mongo",

    # Logs / Temp / Misc
    ".DS_Store", "tmp", "temp", "logs", "log",
    "thumbs", "cache", "downloads",

    # Examples / Fixtures
    "examples", "example", "fixtures",
}

IGNORE_EXTENSIONS: Set[str] = {
    # Images / Media
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".ico", ".svg", ".webp",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv",

    # Documents / Archives
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",

    # Binaries / Compiled
    ".pyc", ".pyo", ".pyd", ".class", ".jar", ".war", ".ear",
    ".exe", ".dll", ".so", ".dylib", ".o", ".a", ".obj", ".lib",
    ".bin", ".dat", ".db", ".sqlite", ".sqlite3",

    # Logs / Temp / Backups
    ".log", ".tmp", ".bak", ".swp", ".lock",

    # Misc
    ".DS_Store",
}

IGNORE_FILES: Set[str] = {
    # Lock files
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Pipfile.lock", "uv.lock",
    "Cargo.lock", "go.sum", "Gemfile.lock", "mix.lock",

    # Git / Editor config
    ".gitignore", ".gitattributes", ".gitmodules",
    ".editorconfig", ".prettierrc", ".eslintrc", ".eslintignore",
    ".stylelintrc", "tsconfig.json", "jsconfig.json",

    # Licenses / Docs
    "LICENSE", "LICENSE.txt", "README.md", "README.rst",
    "CHANGELOG.md", "CONTRIBUTING.md",

    # OS-specific
    ".DS_Store", "Thumbs.db", "desktop.ini",
    ".npmrc", ".yarnrc", ".env.local", ".env.example",

    # Coverage / Test config
    "coverage.lcov", ".coveragerc", "jest.config.js",
    "setup.cfg", "tox.ini", "noxfile.py",
}

READABLE_EXTENSIONS: Set[str] = {
    ".py", ".pyw",
    ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".vue", ".svelte",
    ".rs",
    ".go",
    ".java", ".kt", ".kts", ".gradle",
    ".cs", ".vb", ".fs",
    ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx",
    ".rb", ".rake", ".gemspec",
    ".php",
    ".swift", ".m", ".mm",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".gml", ".yy",
    ".lua",
    ".r", ".R",
    ".dart",
    ".ex", ".exs", ".erl", ".hrl",
    ".hs", ".lhs",
    ".scala", ".sbt",
    ".zig",
    ".json", ".toml", ".yaml", ".yml", ".xml", ".ini", ".cfg", ".conf",
    ".env", ".properties",
    ".md", ".rst", ".txt", ".adoc",
    ".sql",
    ".dockerfile",
}

def scan(path: Path) -> dict:
    load_gitignore_into_ignores(path)
    return {
        "name": get_name(path),
        "type": get_project_type(path),
        "structure": get_tree(path),
        "dependencies": get_dependencies(path),
        "files": read_main_files(path),
        "project_name": get_project_name(),
        "repository_name": get_repository_name(),
        "description": get_description()
    }

def load_gitignore_into_ignores(root: Path) -> None:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return
    
    for line in read_text_safe(gitignore).splitlines():
        line = line.strip()
        
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            continue
        line = line.lstrip("/") 
        if line.startswith("*."):
            IGNORE_EXTENSIONS.add(line[1:])
            continue
        name = line.rstrip("/")

        # skip complex patterns with * in the middle
        if "*" in name:
            continue
        if name.startswith("."):
            IGNORE_EXTENSIONS.add(name)

        IGNORE_DIRS.add(name)
        IGNORE_FILES.add(name)

def is_in_ignored_dir(file: Path, root: Path) -> bool:
    for parent in file.relative_to(root).parts[:-1]:
        if parent in IGNORE_DIRS:
            return True
    return False

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

def read_text_safe(file: Path) -> str:
    for encoding in ["utf-8", "utf-16", "latin-1"]:
        try:
            return file.read_text(encoding=encoding)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return ""

def get_project_name() -> str:
    name = str(input("\033[34mWhat is the name of your project? \033[0m"))
    return name

def get_repository_name() -> str:
    repo_name = str(input("\033[34mWhats is the name of repository? \033[0m"))
    repo_name = repo_name.replace(" ","-").lower()
    return repo_name

def get_description() -> str:
    desc = str(input("\033[34mWrite a short description of the project: \033[0m"))
    return desc

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

def get_project_type(path: Path, no_input: bool = False) -> str:
    path = path.resolve()

    if (path / "package.json").exists():
        return "node"
    if (path / "pom.xml").exists():
        return "java"
    if (path / "build.gradle.kts").exists():
        return "kotlin"
    if any(path.glob("*.yyp")):
        return "gml"
    if any(path.glob("**/*.csproj")) or any(path.glob("*.sln")):
        return "csharp"
    if (path / "Gemfile").exists():
        return "ruby"
    if (path / "Cargo.toml").exists():
        return "rust"
    if (path / "go.mod").exists():
        return "go"
    if ((path / "pyproject.toml").exists() or (path / "setup.py").exists() or (path / "setup.cfg").exists() or (path / "requirements.txt").exists() or any(path.glob("*.py"))):
        return "python"
    if no_input:
        return "unknown"
    
    project_type = str(input("What is the primary language of the project? "))
    return project_type

def get_dependencies(path: Path) -> List[Dict[str, str]]:
    project_type = get_project_type(path, True)
    path = path.resolve()
    deps: List[Dict[str, str]] = []

    if project_type == "python":
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                if "tool" in data and "poetry" in data["tool"]:
                    deps = [{"name": k, "version": v} for k, v in data["tool"]["poetry"]["dependencies"].items() if k != "python"]
                else:
                    # PEP 621 — setuptools, hatch, flit, uv...
                    deps = [{"name": d, "version": "*"} for d in data.get("project", {}).get("dependencies", [])]
            except Exception:
                pass
        else:
            # fallback requirements.txt
            req_txt = path / "requirements.txt"
            if req_txt.exists():
                try:
                    content = read_text_safe(req_txt)
                    deps = [
                        {
                            "name": line.strip().split("==")[0],
                            "version": line.strip().split("==")[1] if "==" in line else "*"
                        }
                        for line in content.splitlines()
                        if line.strip() and not line.startswith("#")
                    ]
                except Exception:
                    pass

    elif project_type == "node":
        pkg_json = path / "package.json"
        if pkg_json.exists():
            try:
                with pkg_json.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if "dependencies" in data:
                    deps = [{"name": k, "version": v} for k, v in data["dependencies"].items()]
            except Exception:
                pass

    elif project_type == "rust":
        cargo_toml = path / "Cargo.toml"
        if cargo_toml.exists():
            try:
                with open(cargo_toml, "rb") as f:
                    data = tomllib.load(f)
                if "dependencies" in data:
                    deps = [{"name": k, "version": v if isinstance(v, str) else v.get("version", "*")} 
                                    for k, v in data["dependencies"].items()]
            except Exception:
                pass

    elif project_type == "go":
        go_mod = path / "go.mod"
        if go_mod.exists():
            try:
                with go_mod.open("r", encoding="utf-8") as f:
                    lines = f.readlines()
                in_require = False
                deps = []
                for line in lines:
                    line = line.strip()
                    if line == "require (":
                        in_require = True
                    elif line == ")":
                        in_require = False
                    elif in_require and line:
                        parts = line.split()
                        deps.append({"name": parts[0], "version": parts[1] if len(parts) > 1 else "*"})
            except Exception:
                pass

    elif project_type == "ruby":
        gemfile = path / "Gemfile"
        if gemfile.exists():
            try:
                with gemfile.open("r", encoding="utf-8") as f:
                    lines = f.readlines()
                deps = []
                for line in lines:
                    if line.strip().startswith("gem "):
                        parts = line.strip().split(",")
                        name = parts[0].strip("gem ").strip("'\"")
                        version = parts[1].strip("'\" ") if len(parts) > 1 else "*"
                        deps.append({"name": name, "version": version})
            except Exception:
                pass

    elif project_type in ["java", "kotlin"]:
        # basic support for Maven (pom.xml) and Gradle (build.gradle or .kts)        
        pom = path / "pom.xml"
        if pom.exists():
            try:
                tree = ET.parse(pom)
                root = tree.getroot()
                ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}  # default namespace
                deps = []
                for dep in root.findall(".//mvn:dependency", ns):
                    group = dep.find("mvn:groupId", ns).text if dep.find("mvn:groupId", ns) is not None else ""
                    artifact = dep.find("mvn:artifactId", ns).text if dep.find("mvn:artifactId", ns) is not None else ""
                    version = dep.find("mvn:version", ns).text if dep.find("mvn:version", ns) is not None else "*"
                    name = f"{group}:{artifact}"
                    deps.append({"name": name, "version": version})
            except Exception:
                pass
        else:
            # Gradle
            gradle_file = path / "build.gradle.kts" if project_type == "kotlin" else path / "build.gradle"
            if gradle_file.exists():
                try:
                    with gradle_file.open("r", encoding="utf-8") as f:
                        lines = f.readlines()
                    deps = []
                    in_deps = False
                    for line in lines:
                        line = line.strip()
                        if line.startswith("dependencies {"):
                            in_deps = True
                        elif line == "}":
                            in_deps = False
                        elif in_deps and (line.startswith("implementation") or line.startswith("api") or line.startswith("compileOnly")):
                            dep_str = line.split("(")[1].split(")")[0].strip("'\" ()")
                            parts = dep_str.split(":")
                            name = ":".join(parts[:-1]) if len(parts) > 1 else dep_str
                            version = parts[-1] if len(parts) > 1 else "*"
                            deps.append({"name": name, "version": version})
                except Exception:
                    pass

    elif project_type == "csharp":
        # search for the first .csproj file (assume single-project for simplicity)        
        csproj_files = list(path.glob("**/*.csproj"))
        if csproj_files:
            csproj = csproj_files[0]  # first
            try:
                tree = ET.parse(csproj)
                root = tree.getroot()
                ns = {"ms": "http://schemas.microsoft.com/developer/msbuild/2003"} if root.tag.endswith("Project") else {}
                deps = []
                for pkg in root.findall(".//PackageReference", ns) or root.findall(".//ms:PackageReference", ns):
                    name = pkg.get("Include")
                    version = pkg.get("Version", "*")
                    if name:
                        deps.append({"name": name, "version": version})
            except Exception:
                pass

    elif project_type == "gml":
        yyp_files = list(path.glob("*.yyp"))
        if yyp_files:
            yyp = yyp_files[0]
            try:
                data = json.loads(yyp.read_text(encoding="utf-8"))
                # only extensions
                extensions = [
                    r for r in data.get("resources", [])
                    if "extensions" in r.get("id", {}).get("path", "")
                ]
                deps = [{"name": e["id"]["name"], "version": "*"} for e in extensions]
            except Exception:
                pass

    return deps

def read_main_files(path: Path, min_lines=50, max_lines=300) -> list[dict]:
    files = []

    for file in path.rglob("*"):
        if file.is_dir():
            continue
        if should_ignore(file):
            continue
        if is_in_ignored_dir(file, path):
            continue
        if file.suffix not in READABLE_EXTENSIONS:
            continue

        lines = read_text_safe(file).splitlines()

        if min_lines <= len(lines) <= max_lines:
            files.append({"name": str(file.relative_to(path)), "content": "\n".join(lines)})
        elif len(lines) > max_lines:
            truncated = lines[:max_lines] + [f"... ({len(lines) - max_lines} more lines truncated)"]
            files.append({"name": str(file.relative_to(path)), "content": "\n".join(truncated)})

    return files