from fastapi import APIRouter
from .endpoints import admin, attendance, pages, auth, features as sovereign

api_router = APIRouter()

api_router.include_router(auth, prefix='/auth')
api_router.include_router(pages, prefix='/pages')
api_router.include_router(admin, prefix='/admin')
api_router.include_router(attendance, prefix='/attendance')
api_router.include_router(sovereign, prefix='/sovereign')