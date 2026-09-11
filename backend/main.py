"""Main FastAPI application for GeoParcel AI."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uuid
import os

from backend.api.projects import router as projects_router
from backend.api.assets import router as assets_router
from backend.api.jobs import router as jobs_router
from backend.api.extraction import router as extraction_router
from backend.api.features import router as features_router
from backend.api.validation import router as validation_router
from backend.api.export import router as export_router

app = FastAPI(
    title="GeoParcel AI API",
    description="AI-Assisted Urban Cadastral Mapping & Field Verification API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "*"  # Prototype mode
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"]
)

# Observability Middleware: Request ID tracing
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", f"req-{uuid.uuid4().hex[:8]}")
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Global Exception Handler matching API_CONTRACT.md
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", "req-unknown")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred during processing.",
                "details": {
                    "requestId": req_id,
                    "errorType": exc.__class__.__name__
                }
            }
        },
        headers={"X-Request-ID": req_id}
    )

# Static file serving for fixtures & imagery
fixtures_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
if os.path.exists(fixtures_dir):
    app.mount("/fixtures", StaticFiles(directory=fixtures_dir), name="fixtures")

# Health Check Endpoint matching OBSERVABILITY.md
@app.get("/api/health", tags=["system"])
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "api": "up",
            "gis_engine": "available",
            "cv_pipeline": "available",
            "fixture_store": "ready"
        }
    }

# Register Routers
app.include_router(projects_router)
app.include_router(assets_router)
app.include_router(jobs_router)
app.include_router(extraction_router)
app.include_router(features_router)
app.include_router(validation_router)
app.include_router(export_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
