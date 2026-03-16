# Slooze Backend Challenge – Role Based Food Ordering System

Backend implementation of a role-based food ordering system built with **FastAPI, SQLAlchemy, and MySQL**.

This project implements RBAC (Role-Based Access Control) and country-level data restrictions as described in the Slooze backend challenge.

## Tech Stack

- FastAPI
- Python
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn

## Features

- View restaurants and menu items
- Create orders with multiple food items
- Checkout orders
- Cancel orders
- Role-Based Access Control (RBAC)
- Country-based access restrictions
- Clean API responses using Pydantic schemas
- Proper REST error handling

## Role Permissions

| Feature | Admin | Manager | Member |
|------|------|------|------|
View Restaurants | ✅ | ✅ | ✅ |
Create Order | ✅ | ✅ | ✅ |
Checkout Order | ✅ | ✅ | ❌ |
Cancel Order | ✅ | ✅ | ❌ |
Modify Payment Methods | ✅ | ❌ | ❌ |

## Country Based Access

Managers and Members can only access restaurants within their assigned country.

Example:

- India Manager → Indian restaurants only
- America Manager → American restaurants only
- Admin → Access to all countries

## Project Structure

app/
 ├── routers
 ├── models
 ├── schemas
 ├── services
 ├── seed
 ├── config
 ├── database.py
 └── main.py

 ## Setup Instructions

1. Clone the repository

git clone <repository_url>

2. Navigate to project

cd slooze-food-ordering

3. Create virtual environment

python -m venv venv

4. Activate environment

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

6. Create MySQL database

CREATE DATABASE slooze_db;

7. Configure .env file

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=slooze_db

8. Start server

uvicorn app.main:app --reload

## API Documentation

After starting the server, open:

http://127.0.0.1:8000/docs

This provides Swagger API documentation for testing endpoints.