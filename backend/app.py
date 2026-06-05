import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import init_db

# Monkeypatch httpx to map 'proxies' to 'proxy' for openai compatibility
import httpx
original_client_init = httpx.Client.__init__
def patched_client_init(self, *args, **kwargs):
    if 'proxies' in kwargs:
        kwargs['proxy'] = kwargs.pop('proxies')
    original_client_init(self, *args, **kwargs)
httpx.Client.__init__ = patched_client_init

original_async_init = httpx.AsyncClient.__init__
def patched_async_init(self, *args, **kwargs):
    if 'proxies' in kwargs:
        kwargs['proxy'] = kwargs.pop('proxies')
    original_async_init(self, *args, **kwargs)
httpx.AsyncClient.__init__ = patched_async_init
from backend.api.upload import router as upload_router
from backend.api.jobs import router as jobs_router
from backend.api.reports import router as reports_router
from backend.api.settings import router as settings_router
from backend.api.auth import router as auth_router
from backend.api.pubmed import router as pubmed_router

app = FastAPI(title="PathoScope AI API", version="3.0.0")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
init_db()

# Mount API routers
app.include_router(upload_router, prefix="/api", tags=["upload"])
app.include_router(jobs_router, prefix="/api", tags=["jobs"])
app.include_router(reports_router, prefix="/api", tags=["reports"])
app.include_router(settings_router, prefix="/api", tags=["settings"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(pubmed_router, prefix="/api", tags=["pubmed"])

# Mount storage directory to serve reports and visualizations
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["backend"])
