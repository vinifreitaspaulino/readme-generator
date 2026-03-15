import argparse
import sys
from pathlib import Path    
from greadme import scanner, builder, ai
from greadme.config import load_config, save_config

def log(msg, verbose):
    if verbose:
        print(msg)

def handle_gen(args):
    config = load_config()

    # CLI overrides config
    lang = args.lang or config["general"]["lang"]
    api_key = config["ai"]["api_key"]
    github_user = config["general"]["github_user"]

    if not api_key:
        print("Error: api_key not set. Run: greadme config set ai.api_key <key>")
        return
    if not github_user:
        print("Error: github_user not set. Run: greadme config set general.github_user <key>")
        return
    
    args.output = args.path / "README.md"

    log(f"Project: {args.path}, lang: {args.lang}, model: {args.model} output: {args.output}", args.verbose)

    log("Analyzing the project...", args.verbose) #scanner.py
    context = scanner.scan(args.path)
    
    context.update({"language": args.lang, "github_user": args.github_user})

    log("Building prompt...", args.verbose) #builder.py
    prompt = builder.build(context, args.lang)
    log(prompt, args.verbose)

    print("Sending to the IA...") #ai.py
    response = ai.gemini(prompt, args.model, args.api_key)
 
    if args.output is None:
        readme_path = args.path / f"README.md"
    else:
        readme_path = args.output.resolve()
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(response)

    print(f"Sucess! File {readme_path} created.")

def handle_config_show():
    config = load_config()
    for section, values in config.items():
        print(f"\n[{section}]")
        for key, value in values.items():
            print(f"  {key} = {value}")

def handle_config_set(key: str, value: str):
    if "." not in key:
        print(f"Error: key must be in format section.key (ex: general.lang)")
        return

    section, field = key.split(".", 1)
    config = load_config()

    if section not in config:
        print(f"Error: unknown section '{section}'")
        return
    if field not in config[section]:
        print(f"Error: unknown key '{field}' in section '{section}'")
        return

    config[section][field] = value
    save_config(config)
    print(f"√ {key} = {value}")

def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-") and sys.argv[1] not in ("gen", "config"):
        sys.argv.insert(1, "gen")
    parser = argparse.ArgumentParser(prog="greadme")
    subparsers = parser.add_subparsers(dest="command")

    # sub generate readme
    gen = subparsers.add_parser("gen", help="Generate README")
    gen.add_argument("path", type=Path, help="Path to the project")
    gen.add_argument("--output", "-o", type=Path, default=None, help="Output path (default: <project>/README.md)")
    gen.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")
    
    # sub config
    cfg = subparsers.add_parser("config", help="Manage configuration")
    cfg_sub = cfg.add_subparsers(dest="config_command")

    cfg_show = cfg_sub.add_parser("show", help="Show current config")

    cfg_set = cfg_sub.add_parser("set", help="Set a config value")
    cfg_set.add_argument("key", help="Key to be set (e.g., 'general.lang')")
    cfg_set.add_argument("value", help="Value to set")

    config = load_config()

    gen.add_argument("--lang", "-l", choices=["pt", "en"], default=config["general"]["lang"], help="README language (default: en)")
    gen.add_argument("--api-key", default=config["ai"]["api_key"])
    gen.add_argument("--model", default=config["ai"]["model"])
    gen.add_argument("--github_user", default=config["general"]["github_user"])
    
    args = parser.parse_args()

    if args.command == "config":
        if args.config_command == "show":
            handle_config_show()
        elif args.config_command == "set":
            handle_config_set(args.key, args.value)
    elif args.command == "gen":
        handle_gen(args)

if __name__ == "__main__":
    main()