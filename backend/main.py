from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from config import settings
from database import init_db

# Import routers
from routers import auth, homework, quiz, notes, tutor, subscription, progress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered homework helper and study assistant for students"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )


# Include routers
app.include_router(auth.router)
app.include_router(homework.router)
app.include_router(quiz.router)
app.include_router(notes.router)
app.include_router(tutor.router)
app.include_router(subscription.router)
app.include_router(progress.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "features": [
            "OCR homework scanning",
            "Step-by-step solutions",
            "AI tutor chat",
            "Quiz generation",
            "Study notes builder",
            "Progress tracking",
            "Flashcards",
            "Multiple subjects (Math, Science, History, English)",
            "Premium subscriptions"
        ],
        "supported_subjects": [
            "Math (Algebra, Geometry, Calculus)",
            "Science (Physics, Chemistry, Biology)",
            "History",
            "English",
            "General"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
