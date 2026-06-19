import os
import tempfile
from loaders.drive_loader import GoogleDriveLoader
from loaders.sheet_loader import SheetLoader
from loaders.pdf_loader import PDFLoader


class DocumentLoader:

    def __init__(self, folder_id):

        self.drive = GoogleDriveLoader(
            folder_id
        )

        self.sheet_loader = SheetLoader(
            self.drive.sheets_service
        )
        
        self.pdf_loader = PDFLoader()

    def load_all_documents(self):

        files = self.drive.list_files()

        documents = []

        for file in files:

            mime = file["mimeType"]

            # =====================================
            # GOOGLE DOCS
            # =====================================

            if (
                mime
                ==
                "application/vnd.google-apps.document"
            ):

                doc = self.drive.load_google_doc(
                    file["id"]
                )

                documents.append(
                    {
                        "content": doc["content"],
                        "metadata": {

                            "file_id":
                            file["id"],

                            "file_name":
                            file["name"],

                            "file_type":
                            "google_doc",

                            "modified_time":
                            file["modifiedTime"]
                        }
                    }
                )

            # =====================================
            # GOOGLE SLIDES
            # =====================================

            elif (
                mime
                ==
                "application/vnd.google-apps.presentation"
            ):

                deck = self.drive.load_google_slide(
                    file["id"]
                )

                for slide in deck["slides"]:

                    if not slide["content"].strip():
                        continue

                    documents.append(
                        {
                            "content":
                            slide["content"],

                            "metadata": {

                                "file_id":
                                file["id"],

                                "file_name":
                                file["name"],

                                "file_type":
                                "google_slide",

                                "slide_number":
                                slide["slide_number"],

                                "modified_time":
                                file["modifiedTime"]
                            }
                        }
                    )

            # =====================================
            # GOOGLE SHEETS
            # =====================================

            elif (
                mime
                ==
                "application/vnd.google-apps.spreadsheet"
            ):

                sheets = (
                    self.sheet_loader
                    .load_google_sheet(
                        file["id"]
                    )
                )

                for sheet in sheets:

                    documents.append(
                        {
                            "content":
                            sheet["content"],

                            "metadata": {

                                "file_id":
                                file["id"],

                                "file_name":
                                file["name"],

                                "file_type":
                                "google_sheet",

                                "sheet_name":
                                sheet["sheet_name"],

                                "modified_time":
                                file["modifiedTime"]
                            }
                        }
                    )

            # =====================================
            # PDF FILES
            # =====================================

            elif (
                mime
                ==
                "application/pdf"
            ):

                try:
                    # Download PDF from Drive
                    file_id = file["id"]
                    
                    # Create temp directory
                    temp_dir = tempfile.gettempdir()
                    temp_pdf_path = os.path.join(
                        temp_dir,
                        f"{file_id}.pdf"
                    )

                    # Download file
                    request = self.drive.drive_service.files().get_media(
                        fileId=file_id
                    )
                    
                    with open(temp_pdf_path, 'wb') as f:
                        f.write(request.execute())

                    # Load PDF
                    pdf_content = self.pdf_loader.load_pdf(
                        temp_pdf_path
                    )

                    # Clean up
                    if os.path.exists(temp_pdf_path):
                        os.remove(temp_pdf_path)

                    # Add to documents
                    if pdf_content.strip():
                        documents.append(
                            {
                                "content": pdf_content,
                                "metadata": {
                                    "file_id": file["id"],
                                    "file_name": file["name"],
                                    "file_type": "pdf",
                                    "modified_time": file["modifiedTime"]
                                }
                            }
                        )

                except Exception as e:
                    print(
                        f"⚠️  Error loading PDF {file['name']}: {e}"
                    )

        return documents