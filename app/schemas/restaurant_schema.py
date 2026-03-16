from pydantic import BaseModel


class RestaurantResponse(BaseModel):

    id: int
    name: str
    country_id: int

    class Config:
        orm_mode = True