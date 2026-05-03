import sys
import importlib.util

def extract_pdf():
    pdf_path = "e:/AI/autopresent-cowork-plugin - moon/Sustainable_Architecture_Research_Archive.pdf"
    output_path = "e:/AI/autopresent-cowork-plugin - moon/result/archive_text.txt"
    
    if importlib.util.find_spec("PyPDF2") is not None:
        import PyPDF2
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully extracted using PyPDF2.")
        return

    if importlib.util.find_spec("fitz") is not None:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully extracted using PyMuPDF.")
        return

    print("Error: No PDF library found.")

extract_pdf()
