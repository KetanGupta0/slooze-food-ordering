from pydantic import BaseModel


class MenuItemResponse(BaseModel):

    id: int
    name: str
    price: float
    restaurant_id: int

    class Config:
        orm_mode = True