from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

# Resolve the templates directory relative to *this file*, not the
# process's current working directory. This avoids breakage if the
# app is launched from a different folder (e.g. via `uvicorn app.main:app`
# from the project root vs. from inside `app/`).
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def generate_pdf_bytes(template_name: str, context_data: dict) -> bytes:
    """
    Render a Jinja2 template with the given context and convert the
    resulting HTML into PDF bytes, entirely in memory.
    """
    # 1. Load the specific HTML template
    template = env.get_template(template_name)

    # 2. Inject the data into the HTML
    html_content = template.render(**context_data)

    # 3. Use WeasyPrint to convert HTML to PDF bytes (no disk I/O for the
    #    output). `base_url` tells WeasyPrint where to resolve the
    #    template's relative references (styles.css, logo/logo.jpg, etc.)
    #    against — without it, those assets silently fail to load.
    pdf_bytes = HTML(string=html_content, base_url=str(TEMPLATES_DIR)).write_pdf()

    return pdf_bytes