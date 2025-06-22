from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
from summary import get_summary

from scrape import *
from get_features import *
from predict import *

print("=== Starting FastAPI application ===")

# Create FastAPI app
app = FastAPI(title="Layoff Risk Factor", description="A FastAPI application to predict layoff risk factor")

# Create Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', )
socket_app = socketio.ASGIApp(sio, app)

print("=== Socket.IO server created ===")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("=== CORS middleware added ===")

@app.get("/")
async def root():
    print("=== Root endpoint called ===")
    return {"message": "Hello World"}

@app.get("/scrape")
async def run_scrape():
    print("=== Scrape endpoint called ===")
    scrape_articles()
    print("=== Articles scraped successfully ===")
    return JSONResponse({"body": "Articles scraped"})

@sio.event
async def connect(sid, environ):
    print(f"=== Client connected: {sid} ===")

@sio.event
async def disconnect(sid):
    print(f"=== Client disconnected: {sid} ===")

@sio.event
async def analyze_company(sid, data):
    print(f"=== analyze_company called with data: {data} ===")
    try:
        company_name = data.get('company_name')
        print(f"=== Company name: {company_name} ===")
        
        if not company_name:
            print("=== Error: Company name is required ===")
            await sio.emit('error', {'message': 'Company name is required'}, room=sid)
            return

        print(f"=== Step 1: Finding information about {company_name}... ===")
        await sio.emit('status', {'message': f"Step 1: Finding information about {company_name}..."}, room=sid)
        articles = get_articles_by_company(company_name)[:600000]
        joined_articles = "\n\n".join(article["content"] for article in articles)
        articles = joined_articles[:300000]  

        print(f"=== Found {len(articles)} articles ===")
        
        print(f"=== Step 2: Extracting information... ===")
        await sio.emit('status', {'message': f"Step 2: Extracting information..."}, room=sid)
        features_list = extract_features(company_name, articles)

        print(f"=== Extracted features from {len(features_list)} articles ===")

        print(f"=== Step 3: Consolidating information... ===")
        await sio.emit('status', {'message': f"Step 3: Consolidating information..."}, room=sid)
        summary_json = summarize_articles(articles, company_name)
        print(f"=== Summary JSON: {summary_json} ===")
        
        summary = summary_json["summary"]
        key_points = summary_json["key_points"]
        impacts = summary_json["impact"]
        
        combined_key_factors = [[kp, imp] for kp, imp in zip(key_points, impacts)]
        print(f"=== Combined key factors: {combined_key_factors} ===")

        features_json = combine_features(features_list)
        features_json["company_name"] = company_name
        print(f"=== Combined features JSON: {features_json} ===")

        final_features = Features(**features_json)
        print(f"=== Final features object created ===")

        print(f"=== Step 4: Running model... ===")
        await sio.emit('status', {'message': f"Step 4: Running model..."}, room=sid)
        risk_level = predict(final_features)
        print(f"=== Risk level predicted: {risk_level} ===")
        
        print(f"=== Step 5: Summarizing results... ===")
        await sio.emit('status', {'message': f"Step 5: Summarizing results..."}, room=sid)
        result_summary = get_summary(risk_level, final_features, summary, combined_key_factors)
        print(f"=== Result summary generated ===")

        result_data = {
            "risk_level": risk_level,
            "explanation": result_summary,
            "key_points": combined_key_factors,
            "complete": True
        }
        print(f"=== Sending result data: {result_data} ===")
        
        await sio.emit('analysis_complete', result_data, room=sid)
        print(f"=== Analysis complete for {company_name} ===")

    except Exception as e:
        print(f"=== Error in analyze_company: {str(e)} ===")
        print(f"=== Exception type: {type(e)} ===")
        import traceback
        print(f"=== Traceback: {traceback.format_exc()} ===")
        await sio.emit('error', {'message': str(e)}, room=sid)

@app.post("/layoffs_test/{company_name}")
async def layoffs_test(company_name: str):
    print(f"=== layoffs_test called for company: {company_name} ===")
    
    features, context, key_points = get_features(company_name)
    print(f"=== Features: {features} ===")
    print(f"=== Context: {context} ===")
    print(f"=== Key points: {key_points} ===")

    risk_level = predict(features)
    print(f"=== Risk level: {risk_level} ===")

    summary = get_summary(risk_level, features, context, key_points)
    print(f"=== Summary: {summary} ===")

    result = {
        "risk_level": risk_level,
        "explaination": summary,
        "key_points": key_points
    }
    print(f"=== Returning result: {result} ===")
    
    return JSONResponse(result)

print("=== All endpoints and event handlers defined ===")

# Export the Socket.IO app for ASGI
app = socket_app

print("=== Application setup complete ===")
