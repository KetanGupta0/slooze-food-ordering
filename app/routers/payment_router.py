from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment_method import PaymentMethod
from app.models.user import User

from app.schemas.payment_schema import PaymentMethodCreate
from app.services.rbac import is_admin

router = APIRouter(tags=["Payments"])

@router.post("/payment-methods")
def add_payment_method(
    payment: PaymentMethodCreate,
    admin_user_id: int,
    db: Session = Depends(get_db)
):

    admin_user = db.query(User).filter(User.id == admin_user_id).first()

    if not admin_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not is_admin(admin_user):
        raise HTTPException(
            status_code=403,
            detail="Only admins can add payment methods"
        )

    new_payment = PaymentMethod(
        user_id=payment.user_id,
        type=payment.type,
        details=payment.details
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {"message": "Payment method added"}
