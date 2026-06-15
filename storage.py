import json
from pathlib import Path


DEFAULT_VOCABULARY = [
    {"question": "house", "answer": "Haus"},
    {"question": "tree", "answer": "Baum"},
    {"question": "school", "answer": "Schule"},
    {"question": "network", "answer": "Netzwerk"},
    {"question": "server", "answer": "Server"},
]


def load_vocabulary(file_path):
    path = Path(file_path)
    if not path.exists():
        save_vocabulary(file_path, DEFAULT_VOCABULARY)
        return DEFAULT_VOCABULARY.copy()

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def save_vocabulary(file_path, entries):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(entries, file, ensure_ascii=False, indent=2)
