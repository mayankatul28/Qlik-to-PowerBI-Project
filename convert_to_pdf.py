"""
Convert markdown file to PDF using markdown-pdf library
"""
from markdown_pdf import MarkdownPdf, Section

# Input and output paths
input_md = r"C:\Users\mayan\.gemini\antigravity\brain\31c1ec74-f58f-41c7-ad7a-14e71a865fe5\project_overview.md"
output_pdf = r"d:\IQVIA\Task 1\DAX-Converter\project_overview.pdf"

# Read markdown content
with open(input_md, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Create PDF
pdf = MarkdownPdf()
pdf.add_section(Section(markdown_content))
pdf.save(output_pdf)

print(f"PDF created successfully: {output_pdf}")
