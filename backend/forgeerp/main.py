"""Main FastAPI application"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from forgeerp.core.database.database import create_db_and_tables
from forgeerp.core.api.routes import (
    auth_router,
    clients_router,
    modules_router,
    configurations_router,
    github_router,
    environments_router,
)

app = FastAPI(
    title="ForgeERP API",
    description="Sistema de infraestrutura para parceiros Odoo",
    version="0.1.0",
)

# CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (API routes first)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(environments_router, prefix="/api/v1")
app.include_router(modules_router, prefix="/api/v1")
app.include_router(configurations_router, prefix="/api/v1")
app.include_router(github_router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "forgeerp"}


# Serve static files (frontend build) - must be after API routes
# When running from /app/backend, static is at /app/static
static_dir = Path("/app/static") if Path("/app/static").exists() else Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    # Mount static assets (JS, CSS, images) from dist/static/
    static_assets_dir = static_dir / "static"
    if static_assets_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_assets_dir)), name="static")
    
    # Serve index.html for SPA routing (catch-all, must be last)
    from fastapi.responses import FileResponse
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve SPA for all non-API routes"""
        # Don't interfere with API, docs, or health routes
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path == "health":
            return JSONResponse(status_code=404, content={"detail": "Not found"})
        
        # Serve index.html for SPA routing
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return JSONResponse(status_code=404, content={"detail": "Frontend not found"})
else:
    # Fallback if static files don't exist (development)
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "ForgeERP API",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health",
            "note": "Frontend not built. Run 'npm run build' in frontend/"
        }


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
