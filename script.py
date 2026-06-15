from pathlib import Path
import textwrap

base = Path('output/vokabeltrainer-pr-projekt')

main_py = r'''
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

trainer_py = r'''
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

(base / 'main.py').write_text(textwrap.dedent(main_py).strip() + '\n', encoding='utf-8')
(base / 'trainer.py').write_text(textwrap.dedent(trainer_py).strip() + '\n', encoding='utf-8')
print('fixed')