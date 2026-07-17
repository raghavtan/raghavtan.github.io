import os

from jinja2 import Template

from html_template import HTML_TEMPLATE
from markdown_template import MARKDOWN_TEMPLATE
from pdf_template import PDF_TEMPLATE

# All generated files are written here. This directory is the deploy artifact
# and is intentionally not tracked in git — resume_data.py is the source of truth.
OUTPUT_DIR = "public"


def render_template(template_str, context):
    """Render a Jinja2 template with the provided context."""
    template = Template(template_str)
    return template.render(**context)


def _output_path(output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


def generate_html_resume(data, output_dir=OUTPUT_DIR):
    """Generate the HTML resume. Written as index.html so GitHub Pages serves it."""
    rendered_html = render_template(HTML_TEMPLATE, data)
    output_file = _output_path(output_dir, "index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"HTML resume generated and saved as '{output_file}'.")
    return output_file


def generate_markdown_resume(data, output_dir=OUTPUT_DIR):
    """Generate a Markdown resume."""
    rendered_md = render_template(MARKDOWN_TEMPLATE, data)
    output_file = _output_path(output_dir, "resume.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_md)
    print(f"Markdown resume generated and saved as '{output_file}'.")
    return output_file


def generate_pdf_resume(data, output_dir=OUTPUT_DIR):
    """Generate a PDF resume using xhtml2pdf."""
    from xhtml2pdf import pisa  # Import xhtml2pdf library

    rendered_pdf_html = render_template(PDF_TEMPLATE, data)
    output_file = _output_path(output_dir, "resume.pdf")

    with open(output_file, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(rendered_pdf_html, dest=result_file)

    if pisa_status.err:
        print("An error occurred while generating the PDF resume using xhtml2pdf.")
    else:
        print(f"PDF resume generated and saved as '{output_file}'.")
    return output_file
