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

router = APIRouter()


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
