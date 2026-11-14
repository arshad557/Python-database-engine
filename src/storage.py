
import json
from pathlib import Path


class Storage:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, data):
        with self.file_path.open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not self.file_path.exists():
            return {}

        with self.file_path.open(
            "r", encoding="utf-8"
        ) as file:
            return json.load(file)
