import PyPDF2
from docx import Document

# Function to read a DOCX file
def read_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to read a PDF file
def read_pdf(file):
    pdfReader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdfReader.pages:
        text += page.extract_text() + "\n"
    return text