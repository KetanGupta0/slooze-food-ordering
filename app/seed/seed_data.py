from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.country import Country
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem


def seed_data(db: Session):

    # Roles
    roles = ["admin", "manager", "member"]

    for role_name in roles:
        existing = db.query(Role).filter(Role.name == role_name).first()
        if not existing:
            db.add(Role(name=role_name))

    db.commit()

    # Countries
    countries = ["India", "America"]

    for country_name in countries:
        existing = db.query(Country).filter(Country.name == country_name).first()
        if not existing:
            db.add(Country(name=country_name))

    db.commit()
    
    # Fetch roles
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    manager_role = db.query(Role).filter(Role.name == "manager").first()
    member_role = db.query(Role).filter(Role.name == "member").first()

    # Fetch countries
    india = db.query(Country).filter(Country.name == "India").first()
    america = db.query(Country).filter(Country.name == "America").first()

    users = [
        ("Nick Fury", "nick@slooze.com", admin_role.id, india.id),
        ("Captain Marvel", "marvel@slooze.com", manager_role.id, india.id),
        ("Captain America", "america@slooze.com", manager_role.id, america.id),
        ("Thanos", "thanos@slooze.com", member_role.id, india.id),
        ("Thor", "thor@slooze.com", member_role.id, india.id),
        ("Travis", "travis@slooze.com", member_role.id, america.id),
    ]

    for name, email, role_id, country_id in users:
        existing = db.query(User).filter(User.email == email).first()
        if not existing:
            db.add(
                User(
                    name=name,
                    email=email,
                    role_id=role_id,
                    country_id=country_id
                )
            )

    db.commit()
    
    # Restaurants
    india = db.query(Country).filter(Country.name == "India").first()
    america = db.query(Country).filter(Country.name == "America").first()

    restaurants = [
        ("Spice Garden", india.id),
        ("Bombay Bites", india.id),
        ("Texas Grill", america.id),
        ("NYC Diner", america.id),
    ]

    for name, country_id in restaurants:
        existing = db.query(Restaurant).filter(Restaurant.name == name).first()
        if not existing:
            db.add(Restaurant(name=name, country_id=country_id))

    db.commit()
    
    # Fetch restaurants
    spice_garden = db.query(Restaurant).filter(Restaurant.name == "Spice Garden").first()
    bombay_bites = db.query(Restaurant).filter(Restaurant.name == "Bombay Bites").first()
    texas_grill = db.query(Restaurant).filter(Restaurant.name == "Texas Grill").first()
    nyc_diner = db.query(Restaurant).filter(Restaurant.name == "NYC Diner").first()

    menu_items = [
        ("Paneer Butter Masala", 12.5, spice_garden.id),
        ("Chicken Biryani", 10.0, spice_garden.id),

        ("Vada Pav", 5.0, bombay_bites.id),
        ("Pav Bhaji", 6.5, bombay_bites.id),

        ("BBQ Ribs", 18.0, texas_grill.id),
        ("Steak", 22.0, texas_grill.id),

        ("Burger", 9.0, nyc_diner.id),
        ("Fries", 4.0, nyc_diner.id),
    ]

    for name, price, restaurant_id in menu_items:
        existing = db.query(MenuItem).filter(MenuItem.name == name).first()
        if not existing:
            db.add(MenuItem(
                name=name,
                price=price,
                restaurant_id=restaurant_id
            ))

    db.commit()