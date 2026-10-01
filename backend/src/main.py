"""
ResumeMaker Backend — FastAPI application entry point.

Boot order:
  1. Configure structured logging
  2. Create FastAPI app with metadata
  3. Register CORS middleware
  4. Register request ID middleware
  5. Register global error handlers
  6. Mount API routers
  7. Register startup/shutdown lifecycle hooks
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.error_handlers import register_error_handlers
from src.core.logging import configure_logging, get_logger
from src.core.middleware import RequestIdMiddleware

# ── Bootstrap logging before anything else ───────────────────────────────────
configure_logging()
logger = get_logger(__name__)
settings = get_settings()


# ── Lifespan — startup + shutdown ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # ── Startup ──
    logger.info(
        "app_starting",
        app=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

    # Verify DB connectivity on startup
    try:
        from src.core.database import engine
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        logger.info("database_connected")
    except Exception as exc:
        logger.error("database_connection_failed", error=str(exc))
        # Don't crash — let the first request fail with a clear error

    # Warm up storage provider
    try:
        from src.storage.factory import get_storage_provider
        get_storage_provider()
        logger.info("storage_provider_ready", provider=settings.storage_provider)
    except Exception as exc:
        logger.warning("storage_provider_init_failed", error=str(exc))

    yield

    # ── Shutdown ──
    logger.info("app_shutting_down")
    from src.core.database import engine
    await engine.dispose()


# ── Application factory ───────────────────────────────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title="ResumeMaker API",
        description=(
            "AI-powered resume optimization platform. "
            "Every resume claim is grounded in verified user information."
        ),
        version=settings.app_version,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # ── Request ID (must be after CORS) ──────────────────────────────────────
    app.add_middleware(RequestIdMiddleware)

    # ── Global error handlers ─────────────────────────────────────────────────
    register_error_handlers(app)

    # ── Routers ───────────────────────────────────────────────────────────────
    from src.api.v1.auth import router as auth_router
    from src.api.v1.profile import router as profile_router
    from src.api.v1.storage import router as storage_router

    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(profile_router, prefix=api_prefix)
    app.include_router(storage_router, prefix=api_prefix)

    # ── Health check ─────────────────────────────────────────────────────────
    @app.get("/health", tags=["health"], summary="Health check")
    async def health() -> dict:
        return {
            "status": "ok",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }

    @app.get("/api/v1/health", tags=["health"], summary="API health check")
    async def api_health() -> dict:
        from src.core.database import engine
        from sqlalchemy import text

        db_ok = False
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            db_ok = True
        except Exception:
            pass

        return {
            "status": "ok" if db_ok else "degraded",
            "database": "connected" if db_ok else "unavailable",
            "version": settings.app_version,
        }

    logger.info("app_created", routes=len(app.routes))
    return app


app = create_app()
