from pathlib import Path
import textwrap, json

base = Path('output/vokabeltrainer-pr-projekt')
(base / 'tests').mkdir(parents=True, exist_ok=True)
(base / 'data').mkdir(parents=True, exist_ok=True)

readme = '''
# Vokabeltrainer für Pull-Request-Übungen

Dies ist eine kleine Python-Terminalanwendung für den Unterricht. Die Grundversion ist bewusst einfach gehalten, damit Schülerinnen und Schüler sie verstehen, ausführen und anschließend über kleine Erweiterungen per Pull Request verbessern können.

## Lernziele

- Python-Code lesen und erweitern
- Arbeit mit Funktionen, Modulen und JSON-Dateien
- erste Unit-Tests verstehen und ergänzen
- Branches, Commits, Pull Requests und Code-Reviews üben

## Start

```bash
python3 main.py
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## Projektstruktur

- `main.py`: Startpunkt und Menü
- `trainer.py`: Quiz- und Auswertungslogik
- `storage.py`: Laden und Speichern der Vokabeln
- `data/vocabulary.json`: Beispieldaten
- `tests/`: einfache Unit-Tests

## Vorschlag für Unterrichtseinsatz

1. Repository klonen oder per GitHub Classroom verteilen.
2. Basisprogramm gemeinsam testen.
3. Kleine Erweiterungsaufgaben als Issues vergeben.
4. Jede Gruppe arbeitet in einem eigenen Branch.
5. Änderungen werden per Pull Request eingereicht.
6. Eine andere Gruppe macht das Review.

## Mögliche Pull-Request-Aufgaben

1. Eingaben ohne Beachtung der Groß- und Kleinschreibung vergleichen.
2. Menüpunkt zum Hinzufügen neuer Vokabeln ergänzen.
3. Kategorien wie `IT`, `Englisch`, `Biologie` einführen.
4. Nur fünf zufällige Fragen pro Runde abfragen.
5. Punktestand nach jeder Frage anzeigen.
6. Fehlerliste am Ende der Runde ausgeben.
7. Statistikdatei mit Anzahl richtiger und falscher Antworten speichern.
8. CSV-Import für neue Vokabeln ergänzen.
9. Zusätzliche Tests für Randfälle schreiben.
10. Hilfe-Menü mit Bedienhinweisen ergänzen.
'''

main_py = '''
from trainer import run_quiz, ask_yes_no
from storage import load_vocabulary


def show_menu():
    print("\nVokabeltrainer")
    print("-" * 20)
    print("1) Quiz starten")
    print("2) Vokabeln anzeigen")
    print("3) Beenden")


def show_vocabulary(entries):
    print("\nVorhandene Vokabeln:")
    for index, item in enumerate(entries, start=1):
        print(f"{index:>2}. {item['question']} -> {item['answer']}")


def main():
    entries = load_vocabulary("data/vocabulary.json")

    while True:
        show_menu()
        choice = input("Auswahl: ").strip()

        if choice == "1":
            run_quiz(entries)
        elif choice == "2":
            show_vocabulary(entries)
        elif choice == "3":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe.")

        if choice in {"1", "2"}:
            ask_yes_no("Weiter mit Enter bestätigen")


if __name__ == "__main__":
    main()
'''

trainer_py = '''
from dataclasses import dataclass


@dataclass
class QuizResult:
    total: int
    correct: int

    @property
    def wrong(self):
        return self.total - self.correct

    @property
    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.correct / self.total) * 100)


def normalize_answer(text: str) -> str:
    return text.strip().lower()


def is_correct(user_answer: str, expected_answer: str) -> bool:
    return normalize_answer(user_answer) == normalize_answer(expected_answer)


def evaluate_answers(answer_pairs):
    total = len(answer_pairs)
    correct = sum(1 for user_answer, expected_answer in answer_pairs if is_correct(user_answer, expected_answer))
    return QuizResult(total=total, correct=correct)


def run_quiz(entries):
    print("\nQuiz startet. Bitte Übersetzungen eingeben.\n")
    given_answers = []

    for item in entries:
        user_answer = input(f"{item['question']}: ")
        given_answers.append((user_answer, item['answer']))

    result = evaluate_answers(given_answers)
    print("\nErgebnis")
    print("-" * 20)
    print(f"Richtig: {result.correct} von {result.total}")
    print(f"Falsch : {result.wrong}")
    print(f"Quote  : {result.percentage} %")


def ask_yes_no(prompt):
    input(f"\n{prompt}")
'''

storage_py = '''
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
'''

test_trainer = '''
import unittest

from trainer import is_correct, evaluate_answers


class TrainerTests(unittest.TestCase):
    def test_answer_comparison_is_case_insensitive(self):
        self.assertTrue(is_correct("Haus", "haus"))

    def test_answer_comparison_ignores_spaces(self):
        self.assertTrue(is_correct("  Baum  ", "Baum"))

    def test_evaluate_answers_counts_correct_and_wrong(self):
        result = evaluate_answers([
            ("Haus", "Haus"),
            ("baum", "Baum"),
            ("falsch", "Schule"),
        ])
        self.assertEqual(result.total, 3)
        self.assertEqual(result.correct, 2)
        self.assertEqual(result.wrong, 1)
        self.assertEqual(result.percentage, 67)


if __name__ == "__main__":
    unittest.main()
'''

vocab = [
    {"question": "house", "answer": "Haus"},
    {"question": "tree", "answer": "Baum"},
    {"question": "school", "answer": "Schule"},
    {"question": "keyboard", "answer": "Tastatur"},
    {"question": "network", "answer": "Netzwerk"},
    {"question": "backup", "answer": "Sicherung"}
]

files = {
    base / 'README.md': readme,
    base / 'main.py': main_py,
    base / 'trainer.py': trainer_py,
    base / 'storage.py': storage_py,
    base / 'tests' / 'test_trainer.py': test_trainer,
}

for path, content in files.items():
    path.write_text(textwrap.dedent(content).strip() + '\n', encoding='utf-8')

(base / 'data' / 'vocabulary.json').write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(str(base))