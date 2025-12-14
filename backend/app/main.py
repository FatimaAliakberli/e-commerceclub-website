from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import User, Event, Registration, Announcement, PageContent
from app.routes import auth, events, registrations, admin_users, content, users

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
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://www.e-commerceclubada.xyz", "https://e-commerceclubada.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router, prefix="/api/auth") 
app.include_router(events.router, prefix="/api/events") # Recommended: Add prefixes for clarity/versioning
app.include_router(registrations.router, prefix="/api/registrations") # Recommended: Add prefixes for clarity/versioning
app.include_router(admin_users.router, prefix="/api/admin") # Recommended: Add prefixes for clarity/versioning
app.include_router(content.router, prefix="/api/content") # Recommended: Add prefixes for clarity/versioning
app.include_router(users.router, prefix="/api/users")

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
