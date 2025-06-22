from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime

# SQLite database URL
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Sample User model
class Layover(Base):
    __tablename__ = "layovers"
    
    id = Column(Integer, primary_key=True, index=True)
    layoff_count = Column(Integer)
    funding_raised = Column(Integer)
    type_of_company = Column(String)
    country = Column(String)
    industry = Column(String)
    company_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get database session
async def get_database_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session 