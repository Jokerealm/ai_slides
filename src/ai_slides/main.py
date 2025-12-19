"""
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import asyncio
import logging
import os
import sys
from .api.openai_compat import router as openai_router
from .api.ai_slides_api import router as ai_slides_router
from .api.database_api import router as database_router
from .api.global_master_template_api import router as template_api_router
from .api.config_api import router as config_router
from .api.image_api import router as image_router

from .web import router as web_router
from .database.database import init_db
from .database.create_default_template import ensure_default_templates_exist_first_time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable SQLAlchemy verbose logging completely
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)

# Create FastAPI app
app = FastAPI(
    title="ai_slides API",
    description="AI-powered PPT generation platform with OpenAI-compatible API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Check if database file exists before initialization
        import os
        db_file_path = "ai_slides.db"  # 默认数据库文件路径
        db_exists = os.path.exists(db_file_path)

        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully")

        # Only import templates if database file didn't exist before (first time setup)
        if not db_exists:
            logger.info("First time setup detected - importing templates from examples...")
            template_ids = await ensure_default_templates_exist_first_time()
            logger.info(f"Template initialization completed. {len(template_ids)} templates available.")
        else:
            logger.info("Database already exists - skipping template import")

    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up database connections on shutdown"""
    try:
        logger.info("Shutting down application...")
        logger.info("Application shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(config_router, prefix="", tags=["Configuration Management"])
app.include_router(image_router, prefix="", tags=["Image Service"])

app.include_router(openai_router, prefix="/v1", tags=["OpenAI Compatible"])
app.include_router(ai_slides_router, prefix="/api", tags=["AI Slides API"])
app.include_router(template_api_router, tags=["Global Master Templates"])
app.include_router(database_router, tags=["Database Management"])
app.include_router(web_router, prefix="", tags=["Web Interface"])

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "web", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount temp directory for image cache
temp_dir = os.path.join(os.getcwd(), "temp")
if os.path.exists(temp_dir):
    app.mount("/temp", StaticFiles(directory=temp_dir), name="temp")
    logger.info(f"Mounted temp directory: {temp_dir}")
else:
    logger.warning(f"Temp directory not found: {temp_dir}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - redirect to dashboard"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    favicon_path = os.path.join(os.path.dirname(__file__), "web", "static", "images", "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai_slides API"}

if __name__ == "__main__":
    uvicorn.run(
        "src.ai_slides.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
