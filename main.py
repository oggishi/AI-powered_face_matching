import os
import sys

# Fix for SQLAlchemy + Python 3.11 + Windows multiprocessing issue
# Must be set before importing SQLAlchemy
if sys.platform == "win32":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import get_settings
from app.core.database import init_db
from app.api.routes import router

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered face detection and matching system using deep learning",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="templates")

# Include API router
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"✅ Database initialized")
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started")
    print(f"📝 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    # Disable reload on Windows to avoid multiprocessing issues with SQLAlchemy
    # For development with auto-reload, use: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    use_reload = settings.DEBUG and sys.platform != "win32"
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=use_reload,
        log_level="info"
    )
