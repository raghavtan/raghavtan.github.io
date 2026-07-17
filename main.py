from generator import (
    generate_html_resume,
    generate_markdown_resume,
    generate_pdf_resume,
)
from resume_data import resume_data


def main():
    generate_html_resume(resume_data)
    generate_markdown_resume(resume_data)
    generate_pdf_resume(resume_data)


if __name__ == "__main__":
    main()
