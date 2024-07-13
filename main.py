# # main.py
# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from models import Product as DBProduct, SessionLocal, engine, Base
# from mock_data import mock_data 
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from typing import Dict,List
# from fastapi.responses import JSONResponse
# from http import HTTPStatus
# from models import Item  
# from pydantic import BaseModel

# # import axios from 'react';

# # const  = 'http://localhost:3000'

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # Update with your React app's URL
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# class Product(BaseModel):
#     name: str
#     price: float
#     retailer: str

# class ProductIn(BaseModel):
#     name: str
#     price: float
#     retailer: str

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# items = [
#     Item(id=1, name="Item 1", description="Description 1", price=10.99),
#     Item(id=2, name="Item 2", description="Description 2", price=19.99),
# ]

# @app.get("/items", response_model=List[Item])
# async def read_items():
#     return items

# @app.get("/api/products")
# async def get_all_products():
#     return [
#         {"name": "Product A", "price": 100, "retailer": "store1"},
#         {"name": "Product B", "price": 150, "retailer": "store1"},
#         {"name": "Product A", "price": 110, "retailer": "store2"},
#         {"name": "Product B", "price": 140, "retailer": "store2"},
#         {"name": "Product A", "price": 105, "retailer": "store3"},
#         {"name": "Product B", "price": 145, "retailer": "store3"},
#     ]

# @app.get("/api/products", response_model=List[Product])
# async def get_all_products(db: Session = Depends(get_db)):
#     return db.query(DBProduct).all()

# @app.get("/api/products/search", response_model=List[Product])
# async def search_products(name: str, db: Session = Depends(get_db)):
#     return db.query(DBProduct).filter(DBProduct.name == name).all()

# @app.post("/api/products", response_model=Product)
# async def add_product(product: ProductIn, db: Session = Depends(get_db)):
#     db_product = DBProduct(name=product.name, price=product.price, retailer=product.retailer)
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# @app.put("/api/products/{product_id}", response_model=Product)
# async def update_product(product_id: int, product: ProductIn, db: Session = Depends(get_db)):
#     db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     db_product.name = product.name
#     db_product.price = product.price
#     db_product.retailer = product.retailer
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# @app.delete("/api/products/{product_id}")
# async def delete_product(product_id: int, db: Session = Depends(get_db)):
#     db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     db.delete(db_product)
#     db.commit()
#     return {"detail": "Product deleted"}

# @app.get("/api/products/mock", response_model=Dict[str, List[Product]])
# async def get_mock_products():
#     return mock_data

# # Initialize the products database with mock data for demonstration purposes
# with SessionLocal() as db:
#     for store, products in mock_data.items():
#         for product in products:
#             db_product = DBProduct(name=product["name"], price=product["price"], retailer=store)
#             db.add(db_product)
#     db.commit()


# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Allow CORS
origins = [
    "http://localhost:3000",  # React app default port
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    retailer = Column(String, index=True)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str
    retailer: str
    price: float

@app.post("/items/")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, retailer=item.retailer, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
