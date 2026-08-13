from pathlib import Path
from typing import List, Union
from docx import Document
from presidio_analyzer import RecognizerResult

def redact_paragraph_runs(paragraph, detections: List[RecognizerResult]) -> None:
    if not detections or not paragraph.runs:
        return

    sorted_detections = sorted(detections, key=lambda d: d.start, reverse=True)

    for det in sorted_detections:
        placeholder = f"<{det.entity_type}>"
        d_start = det.start
        d_end = det.end

        run_bounds = []
        curr = 0
        for run in paragraph.runs:
            length = len(run.text)
            run_bounds.append((curr, curr + length, run))
            curr += length

        if not run_bounds or curr < d_end:
            continue

        start_run_i = None
        end_run_i = None

        for i, (r_start, r_end, run) in enumerate(run_bounds):
            if start_run_i is None and r_start <= d_start < r_end:
                start_run_i = i
            if r_start < d_end <= r_end:
                end_run_i = i
                break

        if start_run_i is None or end_run_i is None:
            continue

        if start_run_i == end_run_i:
            r_start, _, run = run_bounds[start_run_i]
            local_start = d_start - r_start
            local_end = d_end - r_start
            run.text = run.text[:local_start] + placeholder + run.text[local_end:]
        else:
            r_start, _, start_run = run_bounds[start_run_i]
            local_start = d_start - r_start
            start_run.text = start_run.text[:local_start] + placeholder

            for mid_i in range(start_run_i + 1, end_run_i):
                paragraph.runs[mid_i].text = ""

            r_start_e, _, end_run = run_bounds[end_run_i]
            local_end = d_end - r_start_e
            end_run.text = end_run.text[local_end:]

class DOCXRedactor:
    def __init__(self, docx_path: Union[str, Path]) -> None:
        self.docx_path = Path(docx_path)
        self.document = Document(str(self.docx_path))

    def redact(self, paragraph_detections: List[List[RecognizerResult]]) -> Document:
        for paragraph, detections in zip(self.document.paragraphs, paragraph_detections):
            redact_paragraph_runs(paragraph, detections)
        return self.document

    def save(self, output_path: Union[str, Path]) -> None:
        self.document.save(str(output_path))
