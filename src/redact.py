import argparse
from pathlib import Path
from src.pipeline import PIIRedactionPipeline

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect and redact PII from DOCX documents."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to input DOCX file",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output/sanitized_document.docx"),
        help="Path to save sanitized DOCX file",
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.4,
        help="Confidence score threshold for redaction (default 0.4)",
    )

    args = parser.parse_args()

    pipeline = PIIRedactionPipeline(score_threshold=args.threshold)
    print(f"Processing document: {args.input}")
    pipeline.process_document(args.input, args.output)
    print(f"Sanitized document successfully saved to: {args.output}")

if __name__ == "__main__":
    main()
