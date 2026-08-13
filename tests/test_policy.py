import unittest
from presidio_analyzer import RecognizerResult
from src.policy import PIIPolicy

class TestPIIPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = PIIPolicy(
            allowed_entities={"PERSON", "EMAIL_ADDRESS"},
            score_threshold=0.5,
        )

    def test_filter_allowed_entities(self) -> None:
        results = [
            RecognizerResult(entity_type="PERSON", start=0, end=7, score=0.8),
            RecognizerResult(entity_type="LOCATION", start=10, end=15, score=0.9),
            RecognizerResult(entity_type="EMAIL_ADDRESS", start=20, end=35, score=0.7),
        ]
        filtered = self.policy.filter_detections(results)
        self.assertEqual(len(filtered), 2)
        entity_types = {r.entity_type for r in filtered}
        self.assertIn("PERSON", entity_types)
        self.assertIn("EMAIL_ADDRESS", entity_types)
        self.assertNotIn("LOCATION", entity_types)

    def test_filter_confidence_threshold(self) -> None:
        results = [
            RecognizerResult(entity_type="PERSON", start=0, end=7, score=0.8),
            RecognizerResult(entity_type="PERSON", start=10, end=15, score=0.3),
        ]
        filtered = self.policy.filter_detections(results)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].score, 0.8)

if __name__ == "__main__":
    unittest.main()
