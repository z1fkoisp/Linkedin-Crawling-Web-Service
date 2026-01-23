"""
LinkedIn Web Crawler Backend - FastAPI Application

This is the main entry point for the LinkedIn Web Crawler backend API.
It provides REST endpoints for crawling LinkedIn profile data using Selenium.
"""

import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routes import router
from app.crawler import LinkedInCrawler
from app.credentials import get_credentials

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/crawler.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager

    Handles startup and shutdown events for the FastAPI application.
    """
    # Startup
    logger.info("Starting LinkedIn Web Crawler Backend")
    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down LinkedIn Web Crawler Backend")
    logger.info("Application shutdown complete")


# Create FastAPI application with lifespan management
app = FastAPI(
    title="LinkedIn Web Crawler API",
    description="REST API for crawling publicly available LinkedIn profile data",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
    openapi_url="/openapi.json"  # OpenAPI schema
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(
    router,
    prefix="/api/v1",  # API versioning
    tags=["crawler"]   # OpenAPI tags
)


@app.get("/")
async def root():
    """
    Root endpoint - API information

    Returns basic API information and health status.
    """
    return {
        "message": "LinkedIn Web Crawler API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Used by load balancers and monitoring systems to check API status.
    """
    try:
        # Test credential availability (without exposing them)
        get_credentials()
        credential_status = "available"
    except Exception:
        credential_status = "unavailable"

    return {
        "status": "healthy",
        "timestamp": "2026-01-23T00:00:00Z",  # Would be dynamic in real app
        "credentials": credential_status,
        "version": "1.0.0"
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors

    Provides user-friendly error messages for invalid request data.
    """
    logger.warning(f"Validation error for {request.url}: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions

    Customizes error responses for HTTP exceptions.
    """
    logger.error(f"HTTP exception for {request.url}: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions

    Catches any unhandled exceptions and returns a generic error response.
    """
    logger.error(f"Unexpected error for {request.url}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "request_id": str(id(request))  # Simple request ID
        }
    )


def create_application() -> FastAPI:
    """
    Application factory function

    Creates and configures the FastAPI application.
    Useful for testing and deployment scenarios.

    Returns:
        Configured FastAPI application instance
    """
    return app


if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "main:create_application",  # Use factory function
        host="0.0.0.0",             # Listen on all interfaces
        port=8000,                  # Default port
        reload=True,                # Auto-reload on code changes
        log_level="info",           # Logging level
        access_log=True,            # Access logging
        server_header=False,        # Don't expose server info
        date_header=False           # Don't expose date header
    )
