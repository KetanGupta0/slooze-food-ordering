from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.schemas.order_schema import OrderCreate
from app.models.user import User
from app.services.rbac import is_member
from fastapi import HTTPException
from app.models.restaurant import Restaurant

router = APIRouter(tags=["Orders"])


@router.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):

    new_order = Order(
        user_id=order.user_id, restaurant_id=order.restaurant_id, status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()

        if not menu_item:
            continue

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
        )

        db.add(order_item)

    db.commit()

    return {"message": "Order created", "order_id": new_order.id}


@router.post("/orders/{order_id}/checkout")
def checkout_order(order_id: int, user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # RBAC check
    if is_member(user):  # member
        raise HTTPException(
            status_code=403, detail="Members are not allowed to checkout orders"
        )

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "completed"

    db.commit()

    return {"message": "Order checked out successfully"}


@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # RBAC check
    if is_member(user):  # member
        raise HTTPException(
            status_code=403, detail="Members are not allowed to cancel orders"
        )

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "cancelled"

    db.commit()

    return {"message": "Order cancelled successfully"}

@router.get("/orders")
def list_orders(user_id: int, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Admin → all orders
    if user.role_id == 1:
        orders = db.query(Order).offset(offset).limit(limit).all()

    # Manager → orders from their country
    elif user.role_id == 2:

        orders = (db.query(Order).join(Restaurant, Order.restaurant_id == Restaurant.id).filter(Restaurant.country_id == user.country_id).offset(offset).limit(limit).all())

    # Member → only their own orders
    else:
        orders = db.query(Order).filter(Order.user_id == user.id).offset(offset).limit(limit).all()

    return orders
