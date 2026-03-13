from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"


def build(context: dict, lang: str = "pt") -> str:
    template_path = TEMPLATES_DIR / f"{lang}.md"
    assert template_path.exists(), f"{template_path} DOESN'T EXISTS"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    source_files = ""
    for file in context["files"]:
        source_files += (f"\n--- {file['name']} ---")
        source_files += (file["content"])
    format_template = template.format(**context)
    format_template = format_template.replace("[FILE CONTENTS HERE]", source_files)
    print(format_template)

    nome_arquivo_saida = f"prompt.md"
    with open(nome_arquivo_saida, "w", encoding="utf-8") as saida:
        saida.write(format_template)

    print(f"Sucess! File '{nome_arquivo_saida}' created.")

    return format_template

