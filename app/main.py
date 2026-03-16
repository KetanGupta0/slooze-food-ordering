from fastapi import FastAPI
from app.database import engine, Base
from app.models import role, country, user, restaurant, menu_item, order, order_item, payment_method
from app.database import SessionLocal
from app.seed.seed_data import seed_data
from app.routers.restaurant_router import router as restaurant_router
from app.routers.order_router import router as order_router
from app.routers.payment_router import router as payment_router

app = FastAPI(
    title="Slooze Food Ordering System",
    description="""
Backend implementation of a role-based food ordering system.

Features implemented:
- Role Based Access Control (Admin, Manager, Member)
- Country-level access restriction
- Order management
- Payment method management
- Pagination support
- API versioning

This API was developed as part of the Slooze backend engineering challenge.
""",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

db = SessionLocal()
seed_data(db)
db.close()

@app.get("/", tags=["System"])
def home():
    return {"message": "Slooze Backend Running"}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

app.include_router(restaurant_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
