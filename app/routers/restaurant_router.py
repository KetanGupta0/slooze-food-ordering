from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.user import User
from typing import List
from app.schemas.restaurant_schema import RestaurantResponse
from app.schemas.menu_schema import MenuItemResponse

router = APIRouter()

@router.get("/restaurants", response_model=List[RestaurantResponse])
def get_restaurants(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    # Admin can see everything
    if user.role_id == 1:
        restaurants = db.query(Restaurant).all()

    else:
        restaurants = db.query(Restaurant).filter(
            Restaurant.country_id == user.country_id
        ).all()

    return restaurants

@router.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItemResponse])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):

    menu_items = db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id
    ).all()

    return menu_items