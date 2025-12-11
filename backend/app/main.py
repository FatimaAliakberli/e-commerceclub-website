from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import User, Event, Registration, Announcement, PageContent
from app.routes import auth, events, registrations

# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce Club API",
    description="API for University E-Commerce Club Website",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router)
app.include_router(events.router)  
app.include_router(registrations.router)

@app.get("/")
async def root():
    return {
        "message": "E-Commerce Club API is running",
        "version": "1.0.0",
        "docs": "/docs"
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
        }

@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "title": "E-Commerce Club API",
        "version": "1.0.0",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }