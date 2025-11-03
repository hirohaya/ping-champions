#!/usr/bin/env python
"""Start backend server without reloader"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn
from main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info')
