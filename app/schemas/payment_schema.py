from pydantic import BaseModel


class PaymentMethodCreate(BaseModel):

    user_id: int
    type: str
    details: str