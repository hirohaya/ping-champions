#!/usr/bin/env python
"""Minimal backend para testar se qualquer endpoint funciona"""
import sys
import os
import signal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("[STARTUP] Importando FastAPI...")
from fastapi import FastAPI
from database import Base, engine

print("[STARTUP] Criando tabelas...")
Base.metadata.create_all(bind=engine)

print("[STARTUP] Criando app FastAPI...")
app = FastAPI()

@app.get("/")
def root():
    print("[ENDPOINT] GET /")
    return {"message": "OK"}

@app.get("/events")
def list_events():
    print("[ENDPOINT] GET /events")
    from database import SessionLocal
    from models import Event
    db = SessionLocal()
    events = db.query(Event).all()
    db.close()
    return [{"id": e.id, "name": e.name} for e in events]

print("[STARTUP] App criado com sucesso")

if __name__ == "__main__":
    print("[MAIN] Iniciando uvicorn...")
    import uvicorn
    
    def handle_signal(signum, frame):
        print(f"[SIGNAL] Recebido signal {signum}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    print("[MAIN] Chamando uvicorn.run()")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("[MAIN] KeyboardInterrupt received")
    except Exception as e:
        print(f"[MAIN] Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("[MAIN] Encerrando...")

