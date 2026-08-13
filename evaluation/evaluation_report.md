# Evaluation Strategy and Report: PII Redaction Tool

This document outlines the evaluation strategy, benchmark metrics, and real-world results of the PII Redaction Tool.

---

## 1. Objective
The goal of this evaluation is to measure the performance, correctness, and safety of the PII Redaction Tool. A successful redaction pipeline must balance two competing forces:
1. **Privacy Protection (Recall)**: Maximize detection of sensitive personal data (minimizing False Negatives).
2. **Document Readability (Precision)**: Avoid over-redacting non-sensitive business terms, locations, and generic numbers (minimizing False Positives).

---

## 2. Evaluation Methodology
PII detection is probabilistic. Rather than manually auditing the entire 200,000+ character prospectus document (which is unfeasible to do continuously and error-prone), we evaluate the core system using a dual approach:
1. **Automated Benchmark Suite**: A set of curated synthetic test cases with known expected PII spans.
2. **Real-Document Verification (Telemetry)**: Analysis of raw and filtered entity distributions from running the pipeline against the actual *Red Herring Prospectus.docx*.

---

## 3. Definitions and Formulae

### Metrics Definition
- **True Positive (TP)**: Actual PII that was correctly detected and redacted (e.g., Solaire's email correctly replaced by `<EMAIL_ADDRESS>`).
- **False Positive (FP)**: Non-sensitive text incorrectly flagged and redacted as PII (over-redaction; e.g., redacting a street name or currency code as a personal identifier).
- **False Negative (FN)**: Actual PII missed by the detector (privacy leak; e.g., leaving a director's name unredacted).
- **True Negative (TN)**: Generic business text correctly left untouched (not scored in span-based evaluations).

### Metrics Formulae
- **Precision**: The ratio of correctly redacted PII to total detections. Higher precision means fewer false positives (less text corrupted).
  $$\text{Precision} = \frac{TP}{TP + FP}$$

- **Recall**: The ratio of detected PII to total actual PII in the document. Higher recall means fewer false negatives (better privacy coverage).
  $$\text{Recall} = \frac{TP}{TP + FN}$$

- **F1 Score**: The harmonic mean of Precision and Recall, providing a balanced measure of the system's performance.
  $$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## 4. Quantitative Benchmark Results
To establish baseline correctness, the pipeline was evaluated using curated synthetic test cases inside `tests/` containing typical context sentences and expected PII spans.

### Summary Metrics
| Metric | Benchmark Result |
| :--- | :--- |
| **True Positives (TP)** | 14 |
| **False Positives (FP)** | 0 |
| **False Negatives (FN)** | 0 |
| **Precision** | 100% |
| **Recall** | 100% |
| **F1 Score** | 100% |

*Note: These baseline metrics represent the performance on the controlled synthetic benchmark to verify algorithmic correctness, not performance metrics for the entire real prospectus document. Real-world documents introduce statistical variance, contextual ambiguity, and formatting edge cases.*

---

## 5. Observations from the Red Herring Prospectus Run
Processing the actual prospectus document (`input/Red Herring Prospectus.docx`) provides the following operational telemetry:

- **Total Paragraphs Processed**: **5,205 paragraphs** (comprising 1,006 body text paragraphs and 4,199 paragraphs inside 76 tables).
- **Raw Presidio Detections**: **2,175 raw entities** (e.g., dates, locations, bank accounts, driver licenses).
- **Policy-Filtered Detections (Threshold 0.4)**: **478 candidate PII entities** (whitelisted to `PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `IP_ADDRESS`).
- **Successfully Applied Redactions**: **447 placeholders** inserted in the final output:
  - `<PERSON>`: **329 occurrences**
  - `<EMAIL_ADDRESS>`: **68 occurrences**
  - `<PHONE_NUMBER>`: **50 occurrences**

### Qualitative Observations
1. **Tables (High-Density PII)**: By expanding the parser to traverse tables (`doc.tables`), the system additionally processed 295 policy-filtered detections that were previously missed by the body-paragraph-only implementation. Officer tables, compliance contacts, and director profiles were successfully redacted.
2. **False Negatives (Missed Names)**: Some Indian names (e.g., "Sarthak Malvadkar" in certain context titles) were missed by the spaCy `en_core_web_sm` English language model. Statistical NER models are trained on capitalization and grammatical structures; unfamiliar contexts can lead to false negatives.
3. **Image-Embedded PII (PAN Cards)**: Near the end of the document, a scanned PAN card is embedded as an image. Because the pipeline operates strictly on text extraction and XML run manipulation, it does not analyze image pixels. Consequently, the names, father's names, dates of birth, PAN numbers, and QR codes inside the PAN card image remained unredacted.

---

## 6. Limitations and Future Work
- **OCR Integration**: Adding a library like Tesseract OCR or AWS Textract to extract text from images prior to NLP analysis, then applying bounding-box redaction directly on the images, is the recommended solution for image-embedded PII.
- **Custom NER Models**: Utilizing a language model trained specifically on Indian names or business terminology would resolve contextual false negatives.
- **XML Sections**: Headers, footers, and shapes are not currently traversed, which represents a known structural limitation.
