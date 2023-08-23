from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SFreeRooms(SRooms):
    total_cost: int
    rooms_left: int
