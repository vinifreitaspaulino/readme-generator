from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"


def build(context: dict, lang: str = "pt") -> str:
    template_path = TEMPLATES_DIR / f"{lang}.md"
    assert template_path.exists(), f"{template_path} DOESN'T EXISTS"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    format_template = template.format(**context)
    print(format_template)

