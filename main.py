#!/usr/bin/python3
import uvicorn
from app.services.services import app
from fastapi.staticfiles import StaticFiles

"""Mount static folder for the web API to serve"""
app.mount("/static", StaticFiles(
    directory="static"), 
    name="static"
    )


if __name__ == "__main__":
    """Run the server"""
    uvicorn.run(
        "main:app",
        host = "127.0.0.1",
        port = 1337
    )