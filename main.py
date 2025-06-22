from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
import asyncio

from database import engine, Base, get_database_session, Layover as DBLayover, AsyncSessionLocal
from models import Layover, addLayover

app = FastAPI(title="FastAPI with SQLite", description="A FastAPI application with SQLite database")

# Create database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "FastAPI with SQLite Database", "docs": "/docs"}    

# Layover endpoints
@app.get("/layovers", response_model=List[Layover])
async def get_layovers(db: AsyncSession = Depends(get_database_session)):
    """Get all layovers from the database"""
    result = await db.execute(select(DBLayover))
    layovers = result.scalars().all()
    return layovers

@app.get("/layovers/{company_name}", response_model=List[Layover])
async def get_layover_by_company(company_name: str, db: AsyncSession = Depends(get_database_session)):
    """Get layovers by company name"""
    result = await db.execute(select(DBLayover).where(DBLayover.company_name == company_name))
    layovers = result.scalars().all()
    if not layovers:
        raise HTTPException(status_code=404, detail="No layoffs found for this company")
    return layovers

@app.post("/layovers", response_model=Layover)
async def create_layover(layover: addLayover, db: AsyncSession = Depends(get_database_session)):
    """Create a new layover record in the database"""
    db_layover = DBLayover(**layover.model_dump())
    db.add(db_layover)
    await db.commit()
    await db.refresh(db_layover)
    return db_layover

# Get layovers by industry
@app.get("/layovers/industry/{industry}", response_model=List[Layover])
async def get_layovers_by_industry(industry: str, db: AsyncSession = Depends(get_database_session)):
    """Get all layovers by industry"""
    result = await db.execute(select(DBLayover).where(DBLayover.industry == industry))
    layovers = result.scalars().all()
    if not layovers:
        raise HTTPException(status_code=404, detail="No layoffs found for this industry")
    return layovers

# Get layovers by country
@app.get("/layovers/country/{country}", response_model=List[Layover])
async def get_layovers_by_country(country: str, db: AsyncSession = Depends(get_database_session)):
    """Get all layovers by country"""
    result = await db.execute(select(DBLayover).where(DBLayover.country == country))
    layovers = result.scalars().all()
    if not layovers:
        raise HTTPException(status_code=404, detail="No layoffs found for this country")
    return layovers

# Database stats endpoint
@app.get("/stats")
async def get_database_stats(db: AsyncSession = Depends(get_database_session)):
    """Get database statistics"""
    layovers_result = await db.execute(select(DBLayover))
    layovers_count = len(layovers_result.scalars().all())
    
    return {
        "total_layovers": layovers_count,
        "database_file": "app.db"
    }


@app.delete("/layovers")
async def deleteAllLayovers(db: AsyncSession = Depends(get_database_session)):
    """Delete all layovers from the database"""
    await db.execute(delete(DBLayover))
    await db.commit()
    return {"message": "All layovers deleted"}

@app.delete("/layovers/{company_name}")
async def deleteLayoverByCompany(company_name: str, db: AsyncSession = Depends(get_database_session)):
    """Delete a layover by company name"""
    await db.execute(delete(DBLayover).where(DBLayover.company_name == company_name))
    await db.commit()
    return {"message": "Layover deleted"}