from pathlib import Path
from typing import List, Union
from docx import Document

def extract_paragraphs(docx_path: Union[str, Path]) -> List[str]:
    doc = Document(str(docx_path))
    return [p.text for p in doc.paragraphs]

def extract_text(docx_path: Union[str, Path]) -> str:
    paragraphs = extract_paragraphs(docx_path)
    return "\n".join(paragraphs)
