import os
import tomllib
from pathlib import Path

DEFAULT_CONFIG = {
    "general": {
        "lang": "en",
        "provider": "gemini",
        "github_user": "",
    },
    "gemini": {
        "api_key": "",
        "model": "gemini-2.5-flash",
    },
    "groq": {
        "api_key": "",
        "model": "meta-llama/llama-4-scout-17b-16e-instruct"
    },
    "openai": {
        "api_key": "",
        "model": "gpt-5.4-mini"
    }
}

def migrate_config(data: dict) -> dict:
    if "ai" in data:
        old_ai = data.pop("ai")
        if "gemini" not in data:
            data["gemini"] = {}
            data["general"]["provider"] = "gemini"
        data["gemini"]["api_key"] = old_ai.get("api_key", "")
        data["gemini"]["model"] = old_ai.get("model", DEFAULT_CONFIG["gemini"]["model"])
    return data

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
                'provider = "gemini"\n'
                'github_user = ""\n\n'
                '[gemini]\n'
                'api_key = ""\n'
                'model = "gemini-2.5-flash"\n\n'
                '[groq]\n'
                'api_key = ""\n'
                'model = "meta-llama/llama-4-scout-17b-16e-instruct"\n\n'
                '[openai]\n'
                'api_key = ""\n'
                'model = "gpt-5.4-mini"\n\n'
            )

def load_config() -> dict:
    path = get_config_path()
    if not path.exists():
        create_default_config()
        return DEFAULT_CONFIG
    
    with open(path, "rb") as f:
        data = tomllib.load(f)
    data = migrate_config(data)

    config = {}
    for section, defaults in DEFAULT_CONFIG.items():
        config[section] = defaults.copy()
        if section in data:
            config[section].update(data[section])
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