from fastapi import FastAPI, Depends, HTTPException
from typing import List
import asyncio
from pydantic import BaseModel

app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    await scrape()

@app.get("/layovers/{company_name}")
async def get_layover_by_company(company_name: str):
    features: Features = await getFeatures(company_name)
    riskFactor = await model.run(features)
    summary = await getSummary(company_name, features)

    return {**features, "riskFactor": riskFactor}

class Features(BaseModel):
    layoff_count: int
    funding_raised: int
    type_of_company: str
    country: str
    industry: str
    company_name: str