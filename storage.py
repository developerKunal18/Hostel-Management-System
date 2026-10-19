import json
from config import DATA_DIR


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    files = {
        "students.json": [],
        "rooms.json": [],
        "payments.json": []
    }

    for filename, default_data in files.items():
        path = DATA_DIR / filename

        if not path.exists():
            with open(path, "w", encoding="utf-8") as file:
                json.dump(default_data, file, indent=4)


def read_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"{file_path.name} must contain a JSON list.")

        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path.name}. "
            "Please repair the file before continuing."
        ) from error


def write_data(file_path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temporary_path = file_path.with_suffix(".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    temporary_path.replace(file_path)
