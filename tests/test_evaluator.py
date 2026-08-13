import unittest
from src.evaluator import Evaluator

class TestEvaluator(unittest.TestCase):
    def test_perfect_matches(self) -> None:
        predictions = [(0, 10, "EMAIL_ADDRESS"), (15, 20, "PERSON")]
        ground_truth = [(0, 10, "EMAIL_ADDRESS"), (15, 20, "PERSON")]

        metrics = Evaluator.evaluate(predictions, ground_truth)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)
        self.assertEqual(metrics["f1_score"], 1.0)

    def test_false_positive_and_negative(self) -> None:
        predictions = [(0, 10, "EMAIL_ADDRESS"), (30, 40, "LOCATION")]
        ground_truth = [(0, 10, "EMAIL_ADDRESS"), (15, 20, "PERSON")]

        metrics = Evaluator.evaluate(predictions, ground_truth)
        self.assertEqual(metrics["true_positives"], 1)
        self.assertEqual(metrics["false_positives"], 1)
        self.assertEqual(metrics["false_negatives"], 1)
        self.assertEqual(metrics["precision"], 0.5)
        self.assertEqual(metrics["recall"], 0.5)

if __name__ == "__main__":
    unittest.main()
