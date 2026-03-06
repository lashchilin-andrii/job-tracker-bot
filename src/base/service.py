from pathlib import Path
from jinja2 import Template


def render_template(template_path: Path, **context) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**context)
