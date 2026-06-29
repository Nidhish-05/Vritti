"""
main.py — FastAPI application entry point

TODO (Phase 5): Initialize FastAPI app with:
  - Lifespan context manager to create/close DB connection pool at startup/shutdown
  - Include routers from routes/ subpackage
  - CORS middleware (allow dashboard origin)
  - Root route redirects to /docs
  - GET /health endpoint (required for cloud deployment health checks)

Read lifespan pattern before implementing:
  https://fastapi.tiangolo.com/advanced/events/
"""
