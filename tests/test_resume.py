"""Smoke tests: guard the resume_data shape and the three generators."""

from generator import (
    generate_html_resume,
    generate_markdown_resume,
    generate_pdf_resume,
)
from resume_data import resume_data


def test_resume_data_shape():
    """resume_data must carry the keys the templates rely on."""
    for key in ("name", "title", "contact", "executive_summary", "experience"):
        assert key in resume_data, f"missing top-level key: {key}"

    for key in ("email", "phone", "linkedin", "github"):
        assert key in resume_data["contact"], f"missing contact key: {key}"

    assert isinstance(resume_data["experience"], list)
    assert resume_data["experience"], "experience must not be empty"
    for entry in resume_data["experience"]:
        for key in ("company", "role", "duration", "details"):
            assert key in entry, f"experience entry missing key: {key}"


def test_html_generates(tmp_path):
    out = generate_html_resume(resume_data, output_dir=str(tmp_path))
    content = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert out.endswith("index.html")
    assert "<html" in content.lower()
    # The generated site must contain current data, not a stale artifact.
    assert resume_data["experience"][0]["company"] in content


def test_markdown_generates(tmp_path):
    generate_markdown_resume(resume_data, output_dir=str(tmp_path))
    content = (tmp_path / "resume.md").read_text(encoding="utf-8")
    assert content.strip(), "markdown output is empty"
    assert resume_data["name"] in content


def test_pdf_generates(tmp_path):
    generate_pdf_resume(resume_data, output_dir=str(tmp_path))
    pdf = tmp_path / "resume.pdf"
    assert pdf.exists()
    data = pdf.read_bytes()
    assert data.startswith(b"%PDF"), "output is not a valid PDF"
