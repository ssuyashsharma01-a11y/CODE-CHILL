from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.db.init_db import init_db_matrix
import os

app = FastAPI(title='TrustMark Sovereign v50')

# Mount static files for CSS/JS
if os.path.exists('frontend/static'):
    app.mount('/static', StaticFiles(directory='frontend/static'), name='static')

init_db_matrix()
app.include_router(api_router, prefix='/api/v1')
