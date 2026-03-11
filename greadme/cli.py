import argparse
from pathlib import Path

def log(msg, verbose):
    if verbose:
        print(msg)

def main():
    parser = argparse.ArgumentParser(
        prog="greadme",
        description="Generate README files using AI"
    )

    parser.add_argument("path", type=Path, help="Path to the project")
    parser.add_argument("--lang", "-l",  choices=["en","pt"], default="en", help="README language (default: pt)")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output path (default: <project>/README.md)")
    parser.add_argument("--verbose", "-v", action="store_true")
    
    args = parser.parse_args()
    print("Rodando")  # teste

    if args.output is None:
        args.output = args.path / "README.md"

    log(f"Projeto: {args.path}, idioma: {args.lang}, saída: {args.output}", args.verbose)

if __name__ == "__main__":
    main()