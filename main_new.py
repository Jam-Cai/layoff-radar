from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List
import asyncio
from pydantic import BaseModel
from summary import get_summary

from scrape import *
from get_features import *
from predict import *

app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    scrape_articles()
    return JSONResponse({"body": "Articles scraped"})


@app.websocket("/layoffs/{company_name}")
async def layoffs(websocket: WebSocket, company_name: str):
    await websocket.accept()
    
    try:
        async def get_features(company_name):
            await websocket.send_text(f"Step 1: Finding information about {company_name}...")
            articles = get_articles_by_company(company_name)

            await websocket.send_text(f"Step 2: Extracting information...")
            with ThreadPoolExecutor(max_workers=30) as executor:
                features_list = list(executor.map(extract_features, [company_name] * len(articles), [a["content"] for a in articles]))

            await websocket.send_text(f"Step 3: Consolidating information...")
            summary = summarize_articles(articles, company_name)

            features_json = combine_features(features_list)
            features_json["company_name"] = company_name

            final_features = Features(**features_json)
            return final_features, summary

        features, context = get_features(company_name)

        await websocket.send_text(f"Step 4: Running model...")
        risk_level = predict(features)
        
        await websocket.send_text(f"Step 5: Summarizing results...")
        summary = get_summary(risk_level, features, context)

  
        await websocket.send_json({
            "risk_level": risk_level,
            "explanation": summary,
            "complete": True
        })

    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()

@app.post("/layoffs_test/{company_name}")
async def layoffs_test(company_name: str):
    features, context = get_features(company_name)

    summary = get_summary(50, features, context)

    risk_level = predict(features)


    return JSONResponse({"risk_level": risk_level,
                         "explaination": summary})


    

# @app.get("/summary/{company_name}")
# async def get_summary(company_name: str):
#     features: Features = await getFeatures(company_name)
#     summary = await getSummary(company_name, features)
#     return summary
