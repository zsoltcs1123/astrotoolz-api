from fastapi import FastAPI

from astrotoolz_api.routers import timeline

app = FastAPI()

app.include_router(timeline.router)
