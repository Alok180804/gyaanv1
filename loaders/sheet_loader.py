class SheetLoader:

    def __init__(self, sheets_service):
        self.sheets_service = sheets_service

    def load_google_sheet(self, file_id):

        spreadsheet = (
            self.sheets_service.spreadsheets()
            .get(spreadsheetId=file_id)
            .execute()
        )

        sheets = []

        for sheet in spreadsheet["sheets"]:

            sheet_name = sheet["properties"]["title"]

            result = (
                self.sheets_service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=file_id,
                    range=sheet_name
                )
                .execute()
            )

            values = result.get("values", [])

            text = "\n".join(
                [
                    " | ".join(map(str, row))
                    for row in values
                ]
            )

            sheets.append(
                {
                    "sheet_name": sheet_name,
                    "content": text,
                }
            )

        return sheets