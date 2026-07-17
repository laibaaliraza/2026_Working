# Creates the main FastAPI application with a custom title(Demo of FastAPI).
# Includes user and item routers to register their API endpoints.
# Defines a root endpoint that returns a welcome message.

from fastapi import FastAPI
from routers import items,users

app=FastAPI(title="Demo of FastAPI")

app.include_router(users.router)
app.include_router(items.routers)

@app.get("/")
async def main():
    return {"Message: Welcome to FastAPI demo."}
