from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from backend.config.settings import settings

# Configure SQLite parameter fallback for development/testing
connect_args = {}
pool_kwargs = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False, "timeout": 60}
    pool_kwargs = {"poolclass": NullPool}

# Initialize engine and sessionmaker
engine = create_engine(settings.database_url, connect_args=connect_args, **pool_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI dependency to retrieve database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes all database tables registered in the ORM metadata.
    """
    from backend.models import Base
    Base.metadata.create_all(bind=engine)
