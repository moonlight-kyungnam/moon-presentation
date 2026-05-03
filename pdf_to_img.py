import fitz
import sys

def convert_pdf_to_images():
    pdf_path = "e:/AI/llm-wiki(개인이력서)/raw/Sustainable_Architectural_Safety_Innovation (1).pdf"
    try:
        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"e:/AI/llm-wiki(개인이력서)/presentation_result/images/safety_innovation_page_{i}.png")
        print(f"Extracted {len(doc)} pages as images.")
    except Exception as e:
        print(f"Error: {e}")

convert_pdf_to_images()
