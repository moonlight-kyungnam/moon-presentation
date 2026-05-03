import fitz

def extract_text():
    pdf_path = "e:/AI/llm-wiki(개인이력서)/raw/Sustainable_Architectural_Safety_Innovation (1).pdf"
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i in range(len(doc)):
            text += doc.load_page(i).get_text()
        with open("e:/AI/llm-wiki(개인이력서)/presentation_result/archive_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Text extracted.")
    except Exception as e:
        print(f"Error: {e}")

extract_text()
