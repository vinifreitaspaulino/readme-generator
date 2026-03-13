import os
import tomllib
from pathlib import Path

DEFAULT_CONFIG = {
    "general": {
        "lang": "en",
        "github_user": "",
    },
    "ai": {
        "api_key": "",
        "model": "gemini-2.5-flash",
    }
}

def get_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "greadme" / "config.toml"

def create_default_config() -> None:
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                '[general]\n'
                'lang = "en"\n'
                'github_user = ""\n\n'
                '[ai]\n'
                'api_key = ""\n'
                'model = "gemini-2.5-flash"\n'
            )

def load_config() -> dict:
    path = get_config_path()
    if not path.exists():
        create_default_config()
        return DEFAULT_CONFIG
    with open(path, "rb") as f:
        data = tomllib.load(f)
    config = DEFAULT_CONFIG.copy()
    for section, values in data.items():
        config[section].update(values)
    return config

def save_config(config: dict) -> None:
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for section, values in config.items():
            f.write(f"[{section}]\n")
            for key, value in values.items():
                f.write(f'{key} = "{value}"\n')
            f.write("\n")

CONFIG_PATH = get_config_path()