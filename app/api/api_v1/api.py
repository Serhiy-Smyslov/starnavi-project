from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, post

api_router = APIRouter(redirect_slashes=True)
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(post.router, prefix='/post', tags=['post'])
