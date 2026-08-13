from pathlib import Path

from docx import Document
from presidio_analyzer import AnalyzerEngine

INPUT_FILE = Path("../input/Red Herring Prospectus.docx")

def extract_text(path: Path) -> str:
    document = Document(path)

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    return "\n".join(paragraphs)

def detect_pii(text: str):
    analyzer = AnalyzerEngine()

    return analyzer.analyze(
            text=text,
            language="en",
    )

def main():
    text = extract_text(INPUT_FILE)

    results = detect_pii(text)

    print(f"Extracted {len(text)} characters")
    print(f"Found {len(results)} potential PII entities")

    for result in results:
        value = text[result.start:result.end]

        print(
            f"{result.entity_type:<25}"
            f"{result.score:.2f}  "
            f"{value!r}"
        )

if __name__ == "__main__":
    main()
