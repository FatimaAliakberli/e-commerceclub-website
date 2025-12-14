from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import User, Event, Registration, Announcement, PageContent
from app.routes import auth, events, registrations, admin_users, content, users

# --- New Imports for Static File Serving (make sure these are present) ---
from fastapi.staticfiles import StaticFiles 
from starlette.responses import FileResponse 
import os

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
    # ⚠️ TEMPORARY FOR TESTING ONLY ⚠️
    allow_origins=["https://www.e-commerceclubada.xyz"], 
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

# 1. Define the BASE_DIR (one level up from 'backend')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Define the path to your frontend build directory ('frontend/dist')
# We now KNOW the folder name is 'dist' because you use Vite.
FRONTEND_BUILD_DIR = os.path.join(BASE_DIR, "frontend", "dist") 

# 3. Implement the Static File Serving and Catch-All
if os.path.exists(FRONTEND_BUILD_DIR):
    # Mount the 'dist' directory.
    # We serve the static files from the root of the path: /static/main.js -> frontend/dist/main.js
    # The `html=True` argument helps serve index.html by default if the path is not found in the mount, 
    # but we will use the catch-all for more control.
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="static_site")

    # The original catch-all route is often necessary to explicitly tell the server
    # to serve index.html for specific SPA paths like /admin.
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        index_file_path = os.path.join(FRONTEND_BUILD_DIR, "index.html")
        
        # Return index.html for any path that hasn't hit an API endpoint
        if os.path.exists(index_file_path):
            return FileResponse(index_file_path)
        
        return {"message": "Frontend Index not found"}, 404
else:
    print(f"WARNING: Frontend build directory not found at {FRONTEND_BUILD_DIR}. Only API routes will be available.")


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
