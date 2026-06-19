from dotenv import load_dotenv
import os

load_dotenv()

FOLDER_ID = "1r0mmL6sjQOtk6itIGX-Y-yvxwdwnslab"

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

COLLECTION_NAME = "gyaan"


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200