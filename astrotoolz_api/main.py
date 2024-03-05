from fastapi import FastAPI

from astrotoolz_api.routers import horoscope, timeline

app = FastAPI()

app.include_router(timeline.router)
app.include_router(horoscope.router)
