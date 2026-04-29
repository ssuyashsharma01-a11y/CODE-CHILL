import os
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

router = APIRouter()

# 🛡️ Bulletproof pathing for Docker Environment
templates = Jinja2Templates(directory="/app/frontend/templates")

@router.get('/login-page')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/index')
async def index_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})