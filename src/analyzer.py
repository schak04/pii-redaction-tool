from typing import List, Optional
from presidio_analyzer import AnalyzerEngine, RecognizerResult

class PIIAnalyzer:
    def __init__(self, analyzer_engine: Optional[AnalyzerEngine] = None) -> None:
        self.engine = analyzer_engine or AnalyzerEngine()

    def analyze(
        self,
        text: str,
        language: str = "en",
        entities: Optional[List[str]] = None,
        score_threshold: Optional[float] = None,
    ) -> List[RecognizerResult]:
        return self.engine.analyze(
            text=text,
            language=language,
            entities=entities,
            score_threshold=score_threshold,
        )
