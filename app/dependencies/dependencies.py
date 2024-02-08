from app.db.database import SessionLocal
from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)


def get_db():
    """Context manager to ensure database connection is closed after request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
