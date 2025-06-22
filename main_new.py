from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import asyncio
from pydantic import BaseModel
from summary import getSummary

from scrape import *
from get_features import *

app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    scrape_articles()
    return JSONResponse({"body": "Articles scraped"})

@app.get("/layoffs/{company_name}")
async def get_layoffs_by_company(company_name: str):
    features: Features = get_features(company_name)

    return JSONResponse(features.model_dump(mode="json"))

    # riskFactor = await model.run(features)
    # summary = await getSummary(company_name, features)
    # return {**features, "riskFactor": riskFactor}


# @app.get("/summary/{company_name}")
# async def get_summary(company_name: str):
#     features: Features = await getFeatures(company_name)
#     summary = await getSummary(company_name, features)
#     return summary
