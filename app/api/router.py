from fastapi import APIRouter

from app.modules.audit.router import router as audit_router
from app.modules.auth.router import router as auth_router
from app.modules.queries.router import router as queries_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(queries_router)
api_router.include_router(audit_router)
