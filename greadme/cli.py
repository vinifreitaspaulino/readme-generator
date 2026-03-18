import argparse
import sys
from pathlib import Path    
from greadme import scanner, builder, ai
from greadme.config import load_config, save_config
from importlib.metadata import version

def log(msg, verbose):
    if verbose:
        print(msg)

def handle_gen(args):
    config = load_config()

    # CLI overrides config
    lang = args.lang or config["general"]["lang"]

    provider = args.provider or config["general"]["provider"]
    provider = provider.strip().lower()
    if not provider:
        print("Error: provider not set. Run: greadme config set general.provider <provider>")
        return
    if provider not in ("gemini", "groq", "openai"):
        print(f"Error: unknown provider '{provider}'. It must be one of these: gemini, groq, or openai")
        return

    api_key = args.api_key or config[provider]["api_key"]
    model = args.model or config[provider]["model"]
    github_user = config["general"]["github_user"]

    if api_key is None:
        api_key = config[provider]["api_key"]
    if not api_key:
        print("Error: api_key not set. Run: greadme config set <provider>.api_key <key>")
        return
    
    if model is None:
        model = config[provider]["model"]
    if not model:
        print("Error: model not set. Run: greadme config set <provider>.model <key>")
        return
    
    if not github_user:
        print("Error: github_user not set. Run: greadme config set general.github_user <key>")
        return
    
    args.output = args.path / "README.md"

    log(f"Project: {args.path}, lang: {args.lang}, provider: {provider}, model: {model} output: {args.output}", args.verbose)

    log("\033[1;94mAnalyzing the project...\033[0m", args.verbose) #scanner.py
    context = scanner.scan(args.path)
    
    context.update({"language": args.lang, "github_user": args.github_user})

    log("\033[1;94mBuilding prompt...\033[0m", args.verbose) #builder.py
    prompt = builder.build(context, args.lang)

    print("\033[1;94mSending to the IA...\033[0m") #ai.py
    response_text, total_tokens = ai.ai_api(provider, prompt, model, api_key)
    log(response_text, args.verbose)
    log(f"\033[32mTotal number of tokens: \033[0m{total_tokens}", args.verbose)
 
    if args.output is None:
        readme_path = args.path / f"README.md"
    else:
        readme_path = args.output.resolve()
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(response_text)

    print(f"\033[32mSucess! File {readme_path} created.\033[0m")

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
    print(f"✅ {key} = {value}")

def main():
    ver = version("greadme")
    BANNER = rf"""                       _           
  __ _ _ _ ___ __ _ __| |_ __  ___ 
 / _` | '_/ -_) _` / _` | '  \/ -_)
 \__, |_| \___\__,_\__,_|_|_|_\___|
 |___/               """ + f"\033[34mv{ver:<23}\033[0m"                                                     

    if (sys.argv[1:]) == []:
            print(BANNER)
            print("\033[1;34mgreadme - Generates README files using AI in the terminal")
            print("\n\033[90mUsage:")
            print("  greadme ./your-project                         Generate README")
            print("  greadme config show                            Show current config")
            print("  greadme config set general.provider <PROVIDER> Set provider")
            print("  greadme config set <PROVIDER>.api_key <KEY>    Set API key\033[0m")
            print("\n\033[33mRun greadme --help for more information.\033[0m")
            return

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
    gen.add_argument("--github_user", default=config["general"]["github_user"], help="Your GitHub user")
    gen.add_argument("--provider", "-p", choices=["gemini", "groq", "openai"], default=config["general"]["provider"], help="Which provider is your LLM model (gemini, groq or openai?) (default: gemini)")

    gen.add_argument("--api-key", default=None, help="AI api-key")
    gen.add_argument("--model", default=None, help="AI model (default: gemini: gemini-2.5-flash, groq: llama-3.3-70b-versatile, openai: gpt-5.4-mini)")
    
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