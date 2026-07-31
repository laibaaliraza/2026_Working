from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import generate_latest,CONTENT_TYPE_LATEST
import asyncio
from scrapper import run_scrapper


app=FastAPI()

@app.get("/")
async def home():
    return{"Message":"Monitoring enabled"}

@app.get("/error")
async def error():
    raise Exception("Error Message")

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(),media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup():
    print("Starting scraper")
    asyncio.create_task(run_scrapper())

