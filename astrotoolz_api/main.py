from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from astrotoolz_api.routers import dasa, horoscope, timeline

app = FastAPI()

# Define a list of allowed origins for CORS
# For development, you might allow all origins. For production, list your frontend's origin.
origins = [
    "http://localhost:3000",  # Assuming your React app runs on this origin
    "https://yourproductionfrontend.com",
]

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specified origins (use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(timeline.router)
app.include_router(horoscope.router)
app.include_router(dasa.router)
