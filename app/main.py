from fastapi import FastAPI
from app.database import engine, Base
from app.models import role, country, user, restaurant, menu_item, order, order_item, payment_method
from app.database import SessionLocal
from app.seed.seed_data import seed_data
from app.routers.restaurant_router import router as restaurant_router
from app.routers.order_router import router as order_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

db = SessionLocal()
seed_data(db)
db.close()

@app.get("/")
def home():
    return {"message": "Slooze Backend Running"}

app.include_router(restaurant_router)
app.include_router(order_router)
