from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="File Management System API",
        description="File Management System with FastAPI and SQLAlchemy",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    def root():
        return {
            "service": "FileManagementSystem",
            "status": "running",
            "docs": "/docs",
            "api_version": "v1"
        }
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app