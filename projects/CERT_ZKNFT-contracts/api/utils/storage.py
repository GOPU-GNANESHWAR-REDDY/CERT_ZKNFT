import json
import os

def save_to_file(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def load_from_file(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return {}
def save_students(data: dict, file_path: str):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
def load_students(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}
