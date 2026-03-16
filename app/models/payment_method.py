from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    type = Column(String(50), nullable=False)

    details = Column(String(255))