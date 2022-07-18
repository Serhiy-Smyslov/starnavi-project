import logging
from logging import INFO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

logging.getLogger('root').setLevel('INFO')
logging.lastResort.setLevel(INFO)

app = FastAPI(
    title='StarnaviProject',
    description='Starnavi Project',
    version='1.0.0',
    openapi_url=settings.OPENAPI_URL,
)

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# FOR LOCAL USE ONLY
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
