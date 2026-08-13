from pathlib import Path
from typing import Union, Optional, Set, List
from docx import Document

from src.extractor import extract_paragraphs
from src.analyzer import PIIAnalyzer
from src.policy import PIIPolicy
from src.redactor import DOCXRedactor

class PIIRedactionPipeline:
    def __init__(
        self,
        allowed_entities: Optional[Set[str]] = None,
        score_threshold: float = 0.4,
    ) -> None:
        self.analyzer = PIIAnalyzer()
        self.policy = PIIPolicy(
            allowed_entities=allowed_entities,
            score_threshold=score_threshold,
        )

    def process_document(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
    ) -> Document:
        input_p = Path(input_path)
        output_p = Path(output_path)

        paragraphs = extract_paragraphs(input_p)
        paragraph_detections = []

        for p_text in paragraphs:
            raw_results = self.analyzer.analyze(p_text)
            filtered_results = self.policy.filter_detections(raw_results)
            paragraph_detections.append(filtered_results)

        redactor = DOCXRedactor(input_p)
        sanitized_doc = redactor.redact(paragraph_detections)
        
        output_p.parent.mkdir(parents=True, exist_ok=True)
        redactor.save(output_p)

        return sanitized_doc
