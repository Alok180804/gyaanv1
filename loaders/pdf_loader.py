import fitz


class PDFLoader:

    def load_pdf(self, pdf_path):

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()
            text += "\n"

        doc.close()

        return text