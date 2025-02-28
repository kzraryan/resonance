from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from utils.constants import DATABASE_NAME

# SQLite connection string; creates 'database.db' in the current directory.
DATABASE_URL = f"sqlite:///db/web_app/{DATABASE_NAME}.db"

# Create an engine with SQLite-specific options for multithreading.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # Log SQL queries for debugging purposes.
)

# Configure a session factory that provides consistent session objects.
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def get_db():
    """
    Yield a database session for executing transactions.
    The session is closed once the operations are complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
