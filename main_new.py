from fastapi import FastAPI, Depends, HTTPException
from typing import List
import asyncio
from pydantic import BaseModel
from server.summaryLLM.summary import getSummary

app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    await scrape()

@app.get("/layoffs/{company_name}")
async def get_layoff_by_company(company_name: str):
    features: Features = { "layoff_count": 100, "funding_raised": 1000000, "type_of_company": "startup", "country": "USA", "industry": "technology", "company_name": company_name }#getFeatures(company_name)
    riskFactor =  69 #await model(features)
    summary = getSummary(riskFactor, features)

    return {**features, "riskFactor": riskFactor, "summary": summary}

class Features(BaseModel):
    layoff_count: int
    funding_raised: int
    type_of_company: str
    country: str
    industry: str
    company_name: str