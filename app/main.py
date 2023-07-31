from fastapi import FastAPI

from app.hotels.router import router as router_hotels
from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_hotels)
app.include_router(router_bookings)
