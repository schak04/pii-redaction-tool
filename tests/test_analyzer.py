import unittest
from src.analyzer import PIIAnalyzer

class TestAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = PIIAnalyzer()

    def test_detect_email(self) -> None:
        text = "Contact Sans at sans@snowdin.com for hot dogs."
        results = self.analyzer.analyze(text)
        email_results = [r for r in results if r.entity_type == "EMAIL_ADDRESS"]
        self.assertTrue(len(email_results) > 0)
        res = email_results[0]
        self.assertEqual(text[res.start:res.end], "sans@snowdin.com")

    def test_detect_person(self) -> None:
        text = "Solaire of Astora is searching for his own sun."
        results = self.analyzer.analyze(text)
        person_results = [r for r in results if r.entity_type == "PERSON"]
        self.assertTrue(len(person_results) > 0)

if __name__ == "__main__":
    unittest.main()
