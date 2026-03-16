from pydantic import BaseModel
from typing import List


class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: List[OrderItemRequest]