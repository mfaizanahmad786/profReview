"""
FastAPI Application Entry Point
Run with: uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.professors import router as professors_router
from app.routers.reviews import router as reviews_router
from app.routers.dashboard import router as dashboard_router
from app.routers.professor_claims import router as professor_claims_router
from app.routers.admin import router as admin_router

# Create the FastAPI application instance
app = FastAPI(
    title="ProfReview API",
    description="Backend API for professor review platform",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(professors_router)
app.include_router(reviews_router)
app.include_router(dashboard_router)
app.include_router(professor_claims_router)
app.include_router(admin_router)


@app.get("/")
def root():
    """Health check endpoint"""
    return {"message": "ProfReview API is running"}


@app.get("/health")
def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}
