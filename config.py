from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

STUDENTS_FILE = DATA_DIR / "students.json"
ROOMS_FILE = DATA_DIR / "rooms.json"
PAYMENTS_FILE = DATA_DIR / "payments.json"

DATE_FORMAT = "%Y-%m-%d"
