#!/usr/bin/env python
"""Debug script to test backend startup"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    print("[1/5] Importando database...")
    from database import Base, engine, SessionLocal
    print("      ✓ Database OK")
    
    print("[2/5] Importando routers...")
    from routers import events, players, matches, ranking, i18n, membership
    print("      ✓ Routers OK")
    
    print("[3/5] Criando aplicação...")
    from main import app
    print("      ✓ App OK")
    
    print("[4/5] Listando rotas...")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"      - {route.path}")
    
    print("[5/5] Iniciando servidor...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"\n❌ ERRO: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
