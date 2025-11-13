#!/usr/bin/env python
"""Backend server runner with proper path setup and increased request size limits"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

if __name__ == '__main__':
    import uvicorn
    
    # Importar configurações do backend
    sys.path.insert(0, backend_path)
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", os.path.join(backend_path, "config.py"))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    print(f"Starting Ping Champions Backend...")
    print(f"  Host: {config.HOST}")
    print(f"  Port: {config.PORT}")
    print(f"  Max Request Body Size: {config.MAX_REQUEST_BODY_SIZE / (1024*1024):.0f}MB")
    print(f"  Auto-reload: {config.RELOAD}")
    print(f"  API Docs: http://{config.HOST}:{config.PORT}/docs")
    
    uvicorn.run(
        'main:app',
        host=config.HOST,
        port=config.PORT,
        reload=False,  # Disable reload to prevent shutdown issues
    )

