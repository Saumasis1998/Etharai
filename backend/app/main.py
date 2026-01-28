from fastapi import FastAPI
from app.api.v1.router import api_router
from app.common.rate_limiter import limiter, rate_limit_exception_handler
from app.core.logging import setup_logging
from slowapi.errors import RateLimitExceeded

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="HRMS Lite API")

    app.state.limiter = limiter
    
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()
