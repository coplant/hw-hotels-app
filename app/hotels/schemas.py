from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class SFreeHotels(SHotels):
    rooms_left: int
