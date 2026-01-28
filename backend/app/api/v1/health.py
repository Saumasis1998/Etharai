from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Simple health check: reports service status and database connectivity."""
    db_ok = False
    try:
        # simple lightweight check
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {"status": "ok", "db": "ok" if db_ok else "unavailable"}
