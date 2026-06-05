from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Simulates asynchronous chunk-streaming
    chunk_size = 1024 * 1024  # 1MB
    bytes_uploaded = 0
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        bytes_uploaded += len(chunk)
    return {"filename": file.filename, "size": bytes_uploaded, "status": "uploaded"}

@app.get("/progress")
async def progress_stream():
    async def event_generator():
        for progress in range(0, 101, 10):
            yield f"data: {{\"percent\": {progress}, \"status\": \"running\"}}\n\n"
            await asyncio.sleep(0.1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
