from fastapi import FastAPI
from settings.config import settings
from api.base import api_router
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = ["*"]


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    include_router(app)
    return app


app = start_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"msg": "Ok"}
