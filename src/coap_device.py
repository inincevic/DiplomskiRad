import fastapi, time, httpx, sys, json, os, subprocess, asyncio

app = fastapi.FastAPI()

@app.get("/")
def test_get():
    return "The worker code works."

@app.get("/temperature")
def test_get():
    return "Current temperature is 34 degrees celsius."

