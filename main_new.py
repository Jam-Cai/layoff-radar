from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
from summary import get_summary

from scrape import *
from get_features import *
from predict import *

# Create FastAPI app
app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

# Create Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    scrape_articles()
    return JSONResponse({"body": "Articles scraped"})

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def analyze_company(sid, data):
    try:
        company_name = data.get('company_name')
        if not company_name:
            await sio.emit('error', {'message': 'Company name is required'}, room=sid)
            return

        await sio.emit('status', {'message': f"Step 1: Finding information about {company_name}..."}, room=sid)
        articles = get_articles_by_company(company_name)

        await sio.emit('status', {'message': f"Step 2: Extracting information..."}, room=sid)
        with ThreadPoolExecutor(max_workers=30) as executor:
            features_list = list(executor.map(extract_features, [company_name] * len(articles), [a["content"] for a in articles]))

        await sio.emit('status', {'message': f"Step 3: Consolidating information..."}, room=sid)
        summary_json = summarize_articles(articles, company_name)
        summary = summary_json["summary"]
        key_points = summary_json["key_points"]
        impacts = summary_json["impact"]
        combined_key_factors = [[kp, imp] for kp, imp in zip(key_points, impacts)]

        features_json = combine_features(features_list)
        features_json["company_name"] = company_name

        final_features = Features(**features_json)

        await sio.emit('status', {'message': f"Step 4: Running model..."}, room=sid)
        risk_level = predict(final_features)
        
        await sio.emit('status', {'message': f"Step 5: Summarizing results..."}, room=sid)
        result_summary = get_summary(risk_level, final_features, summary, combined_key_factors)

        await sio.emit('analysis_complete', {
            "risk_level": risk_level,
            "explanation": result_summary,
            "key_points": combined_key_factors,
            "complete": True
        }, room=sid)

    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)

@app.post("/layoffs_test/{company_name}")
async def layoffs_test(company_name: str):
    features, context, key_points = get_features(company_name)
    print(features)
    print(context)
    print(key_points)

    risk_level = predict(features)

    summary = get_summary(risk_level, features, context, key_points)

    return JSONResponse({"risk_level": risk_level,
                         "explaination": summary,
                         "key_points": key_points})

# Export the Socket.IO app for ASGI
app = socket_app
