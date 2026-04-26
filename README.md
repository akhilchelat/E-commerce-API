# 🛒 E-commerce Backend API

## 📌 Overview

This project is a backend system for an e-commerce platform built using FastAPI. It handles product management, cart operations, and order workflows with a clean service-layer architecture.

## 🚀 Features

* Product management (CRUD operations)
* Cart system (add, update, remove items)
* Selective checkout (order specific items from cart)
* Stock validation to prevent overselling
* Service-layer architecture for clean and scalable code

## 🏗️ Tech Stack

* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Git & GitHub

## 📦 Project Structure

```
app/
 ├── models/
 ├── schemas/
 ├── services/
 ├── routes/
 ├── db/
 └── main.py
```

## ⚙️ Setup Instructions

1. Clone the repository
2. Create virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Run the server:
   uvicorn app.main:app --reload

## 🚧 Status

Project is currently under development (Order system in progress)

## 🔮 Future Improvements

* Complete order processing workflow
* Payment integration (simulation)
* Order status tracking

## 👤 Author

Akhil Chelat
