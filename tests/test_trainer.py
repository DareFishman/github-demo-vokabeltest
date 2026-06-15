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
