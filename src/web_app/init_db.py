from models.models import Base
from services.db_service import engine

# Create all tables defined in your models
Base.metadata.create_all(engine)
print("Database tables created.")
