from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleDriveLoader:

    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/presentations.readonly",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]

    def __init__(self, folder_id):

        self.folder_id = folder_id

        self.creds = self._authenticate()

        self.drive_service = build(
            "drive",
            "v3",
            credentials=self.creds
        )

        self.docs_service = build(
            "docs",
            "v1",
            credentials=self.creds
        )

        self.slides_service = build(
            "slides",
            "v1",
            credentials=self.creds
        )

        self.sheets_service = build(
            "sheets",
            "v4",
            credentials=self.creds
        )

    # =====================================================
    # AUTH
    # =====================================================

    def _authenticate(self):

        creds = None

        if Path("token.json").exists():

            creds = Credentials.from_authorized_user_file(
                "token.json",
                self.SCOPES
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:

                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    self.SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:

                token.write(
                    creds.to_json()
                )

        return creds

    # =====================================================
    # DRIVE FILES
    # =====================================================

    def list_files(self):

        query = (
            f"'{self.folder_id}' in parents "
            f"and trashed=false"
        )

        results = (
            self.drive_service.files()
            .list(
                q=query,
                pageSize=1000,
                fields="files(id,name,mimeType,modifiedTime)"
            )
            .execute()
        )

        return results.get(
            "files",
            []
        )

    def get_file_by_name(
        self,
        file_name
    ):

        files = self.list_files()

        for file in files:

            if file["name"] == file_name:

                return file

        return None

    # =====================================================
    # GOOGLE DOCS
    # =====================================================

    def load_google_doc(
        self,
        file_id
    ):

        doc = (
            self.docs_service.documents()
            .get(
                documentId=file_id
            )
            .execute()
        )

        return {
            "title": doc["title"],
            "content": self._extract_doc_text(
                doc
            )
        }

    def _extract_doc_text(
        self,
        doc
    ):

        text = ""

        content = (
            doc.get(
                "body",
                {}
            )
            .get(
                "content",
                []
            )
        )

        for element in content:

            paragraph = element.get(
                "paragraph"
            )

            if not paragraph:
                continue

            for item in paragraph.get(
                "elements",
                []
            ):

                text_run = item.get(
                    "textRun"
                )

                if text_run:

                    text += text_run.get(
                        "content",
                        ""
                    )

        return text

    # =====================================================
    # GOOGLE SLIDES
    # =====================================================

    def load_google_slide(
        self,
        file_id
    ):

        presentation = (
            self.slides_service.presentations()
            .get(
                presentationId=file_id
            )
            .execute()
        )

        return {
            "title": presentation["title"],
            "slides": self._extract_slide_text(
                presentation
            )
        }

    def _extract_slide_text(
        self,
        presentation
    ):

        slides_output = []

        slides = presentation.get(
            "slides",
            []
        )

        for slide_idx, slide in enumerate(
            slides,
            start=1
        ):

            slide_text = ""

            for element in slide.get(
                "pageElements",
                []
            ):

                shape = element.get(
                    "shape"
                )

                if not shape:
                    continue

                text_obj = shape.get(
                    "text"
                )

                if not text_obj:
                    continue

                for text_element in text_obj.get(
                    "textElements",
                    []
                ):

                    text_run = text_element.get(
                        "textRun"
                    )

                    if text_run:

                        slide_text += (
                            text_run.get(
                                "content",
                                ""
                            )
                        )

            slides_output.append(
                {
                    "slide_number": slide_idx,
                    "content": slide_text.strip()
                }
            )

        return slides_output