from fastapi import APIRouter

from app.api.api_v1.endpoints import user, post, analyst

api_router = APIRouter(redirect_slashes=True)
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(post.router, prefix='/post', tags=['post'])
api_router.include_router(analyst.router, prefix='/analyst', tags=['analyst'])
