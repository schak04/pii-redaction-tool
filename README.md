# PII Redaction Tool

A document-processing tool that detects and redacts personally identifiable information (PII) from DOCX documents.

## Tech Stack

- **Language**: Python 3.11+
- **Document Parsing**: `python-docx` (XML paragraph and table run extraction)
- **PII Detection Engine**: Presidio (`presidio-analyzer`) & spaCy (`en_core_web_sm` NLP pipeline)
- **Web API**: FastAPI & Uvicorn (ASGI web server)
- **CLI & Utilities**: `argparse`, `pathlib`
- **Testing**: `unittest` standard library runner
- **Deployment & Containerization**: Render Cloud Web Service & Docker

---

## Architecture

![Architecture Diagram](./diagrams/pii-redaction-tool-architecture.png)

The application follows a decoupled 5-stage pipeline:
1. **Extraction** (`src/extractor.py`): Extract text from body paragraphs and table cells (`doc.tables`) using `python-docx`.
2. **Analysis** (`src/analyzer.py`): Detect PII candidate entity ranges using Presidio `AnalyzerEngine` and spaCy NER.
3. **Policy Filtering** (`src/policy.py`): Filter detections using entity whitelist (`PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `IP_ADDRESS`) and confidence score thresholds (`0.4`).
4. **Redaction** (`src/redactor.py`): Map paragraph character offsets across `.docx` `Run` elements, replacing PII right-to-left while preserving formatting.
5. **Orchestration & Interfaces** (`src/pipeline.py`, `src/redact.py`, `src/api.py`): Pipeline facade exposed via CLI and REST API.

---

## Testing & Evaluation

### Evaluation Framework (`src/evaluator.py`)

Computes Precision, Recall, and F1-score against ground truth entity character ranges:
- **Precision**: Ratio of correctly redacted PII to total detections.
- **Recall**: Ratio of detected PII to total actual PII in document.
- **F1 Score**: Harmonic mean balancing precision and recall.

The evaluation uses curated synthetic test cases with known PII spans as a controlled benchmark, alongside telemetry and qualitative inspection from running the pipeline against the supplied Red Herring Prospectus.

### Results on the Supplied Prospectus

The final run processed:

- **5,205 paragraphs** (1,006 body paragraphs and 4,199 paragraphs inside 76 tables)
- **2,175 raw Presidio detections**
- **478 policy-filtered detections**
- **447 successfully applied redaction placeholders**
  - `<PERSON>`: 329
  - `<EMAIL_ADDRESS>`: 68
  - `<PHONE_NUMBER>`: 50

---

## Security & Privacy Considerations

- Input documents (`input/`), outputs (`output/`), and virtual environment (`.venv/`) are gitignored to prevent exposing sensitive data.
- Unit tests use synthetic test fixtures rather than real sensitive documents.

---

## Limitations & Future Work

- **Probabilistic PII Detection**: Presidio and spaCy NER rely on statistical models and regular expressions. Detection is probabilistic and produces trade-offs between false positives and false negatives. Our policy intentionally prioritizes high-confidence direct PII (`PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `IP_ADDRESS`).
- **Scanned Images & Embedded Documents (PAN Cards)**: PII embedded inside images, scanned identity documents (e.g. PAN cards, driver licenses), or QR codes cannot be extracted via text parsing alone. Redacting image-embedded PII requires adding an Optical Character Recognition (OCR) pipeline (such as Tesseract or AWS Textract) followed by image bounding box redaction.
- **Document Structure**: Paragraph text and Word tables (`doc.tables`) are fully supported. Headers, footers, and floating text boxes are outside the current text extraction scope and represent future roadmap items.