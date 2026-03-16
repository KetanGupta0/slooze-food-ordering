from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    country_id = Column(Integer, ForeignKey("countries.id"))