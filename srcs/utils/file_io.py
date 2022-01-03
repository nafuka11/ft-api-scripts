import csv
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path("data")


def save_json(filename: str, data: Any):
    filepath = DATA_DIR / filename
    with filepath.open("w") as f:
        json.dump(data, f)
        print(f"Dumped: {filepath}")


def save_csv(filename: str, rows: list):
    filepath = DATA_DIR / filename
    with filepath.open("w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        print(f"Dumped: {filepath}")
