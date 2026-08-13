import os
import sys
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.pipeline import PIIRedactionPipeline

app = FastAPI(
    title="PII Redaction API",
    description="REST API for detecting and redacting PII from DOCX documents.",
    version="1.0.0",
)

def cleanup_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "pii-redaction-tool"}

@app.post("/redact")
async def redact_docx(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    threshold: float = Query(0.4, ge=0.0, le=1.0, description="Confidence threshold"),
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    in_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")

    try:
        content = await file.read()
        in_tmp.write(content)
        in_tmp.close()
        out_tmp.close()

        pipeline = PIIRedactionPipeline(score_threshold=threshold)
        pipeline.process_document(in_tmp.name, out_tmp.name)

        background_tasks.add_task(cleanup_file, in_tmp.name)
        background_tasks.add_task(cleanup_file, out_tmp.name)

        return FileResponse(
            path=out_tmp.name,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"redacted_{file.filename}",
        )
    except Exception as e:
        cleanup_file(in_tmp.name)
        cleanup_file(out_tmp.name)
        raise HTTPException(status_code=500, detail=str(e))
