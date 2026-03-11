import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        prog="greadme",
        description="Generate README files using AI"
    )

    parser.add_argument("path", type=Path, help="Path to the project")
    parser.add_argument("--lang", "-l",  choices=["en","pt"], default="en", help="README language (default: pt)")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output path (default: <project>/README.md)")
    
    args = parser.parse_args()
    print(f"Projeto: {args.path}, idioma: {args.lang}, saída: {args.output}")  # teste

if __name__ == "__main__":
    main()