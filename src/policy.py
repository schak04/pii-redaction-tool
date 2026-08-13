from typing import List, Set, Optional
from presidio_analyzer import RecognizerResult

DEFAULT_REDACTABLE_ENTITIES: Set[str] = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "IP_ADDRESS",
}

DEFAULT_SCORE_THRESHOLD: float = 0.4

class PIIPolicy:
    def __init__(
        self,
        allowed_entities: Optional[Set[str]] = None,
        score_threshold: float = DEFAULT_SCORE_THRESHOLD,
    ) -> None:
        self.allowed_entities = allowed_entities or DEFAULT_REDACTABLE_ENTITIES
        self.score_threshold = score_threshold

    def filter_detections(
        self,
        results: List[RecognizerResult],
    ) -> List[RecognizerResult]:
        filtered = []
        for res in results:
            if res.entity_type in self.allowed_entities and res.score >= self.score_threshold:
                filtered.append(res)
        return filtered
