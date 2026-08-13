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

## Setup & Local Installation

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies & spaCy Model
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Usage

### 1. CLI Redaction Command
```bash
./.venv/bin/python src/redact.py "input/Red Herring Prospectus.docx" -o "output/sanitized.docx" -t 0.4
```

### 2. Run Local Web API
```bash
./.venv/bin/uvicorn src.api:app --reload --port 8000
```
Access interactive Swagger API docs at `http://127.0.0.1:8000/docs` to test file uploads.

---

## Deployment (Render)

### Deploying to Render
1. Connect repository to Render dashboard.
2. Select **Web Service**.
3. Set **Build Command**:
   ```bash
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```
4. Set **Start Command**:
   ```bash
   uvicorn src.api:app --host 0.0.0.0 --port $PORT
   ```

---

## Testing & Evaluation

### Run Test Suite
```bash
./.venv/bin/python -m unittest discover -s tests -p "test_*.py"
```

### Evaluation Framework (`src/evaluator.py`)
Computes Precision, Recall, and F1-score against ground truth entity character ranges:
- **Precision**: Ratio of correctly redacted PII to total detections.
- **Recall**: Ratio of detected PII to total actual PII in document.
- **F1 Score**: Harmonic mean balancing precision and recall.

---

## Security & Privacy Considerations

- Input documents (`input/`), outputs (`output/`), and virtual environment (`.venv/`) are gitignored to prevent exposing sensitive data.
- Unit tests use synthetic test fixtures (e.g. fictional characters) rather than real sensitive documents.

---

## Limitations & Future Work

- **Probabilistic PII Detection**: Presidio and spaCy NER rely on statistical models and regular expressions. Detection is probabilistic and produces trade-offs between false positives and false negatives. Our policy intentionally prioritizes high-confidence direct PII (`PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `IP_ADDRESS`).
- **Scanned Images & Embedded Documents (PAN Cards)**: PII embedded inside images, scanned identity documents (e.g. PAN cards, driver licenses), or QR codes cannot be extracted via text parsing alone. Redacting image-embedded PII requires adding an Optical Character Recognition (OCR) pipeline (such as Tesseract or AWS Textract) followed by image bounding box redaction.
- **Document Structure**: Paragraph text and Word tables (`doc.tables`) are fully supported. Headers, footers, and floating text boxes are outside the current text extraction scope and represent future roadmap items.
