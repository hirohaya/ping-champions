#!/usr/bin/env python
"""Test uvicorn startup issue"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("[1] Starting imports...", flush=True)
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

print("[2] Creating app...", flush=True)
app = FastAPI()

@app.get("/")
async def root():
    print("[ENDPOINT] GET /", flush=True)
    return {"status": "ok"}

print("[3] App created, starting server...", flush=True)

if __name__ == "__main__":
    import uvicorn
    
    print("[4] About to call uvicorn.run()...", flush=True)
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    print("[5] About to call server.run()...", flush=True)
    try:
        import asyncio
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("[SERVER] KeyboardInterrupt", flush=True)
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        print("[DONE]", flush=True)
