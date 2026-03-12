import argparse
from pathlib import Path    
from greadme import scanner

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
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")
    
    args = parser.parse_args()
    print("Rodando")  # teste

    if args.output is None:
        args.output = args.path / "README.md"

    log(f"Projeto: {args.path}, idioma: {args.lang}, saída: {args.output}", args.verbose)

    print("Varrendo projeto...") #scanner.py
    context = scanner.scan(args.path)
    print(context)
    print(context["structure"])

    print("Montando o prompt...") #builder.py
    print("Chamando a IA...") #ai.py
    print("README gerado com sucesso!")

if __name__ == "__main__":
    main()