import docx
from pypdf import PdfReader

def extract_resume_text(file):
    try:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()

        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs]).strip()

        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8").strip()

        else:
            return "ERROR: Unsupported file format."

    except Exception as e:
        return f"ERROR: Failed to read resume: {str(e)}"