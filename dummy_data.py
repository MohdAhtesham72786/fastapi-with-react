# from app import models, database

# def get_dummy_data():
#     return [
#         {"name": "Laptop", "price": 999.99, "retailer": "Store A"},
#         {"name": "Laptop", "price": 950.00, "retailer": "Store B"},
#         {"name": "Laptop", "price": 1100.00, "retailer": "Store C"},
#         {"name": "Phone", "price": 499.99, "retailer": "Store A"},
#         {"name": "Phone", "price": 450.00, "retailer": "Store B"},
#         {"name": "Phone", "price": 600.00, "retailer": "Store C"},
#     ]

# def populate_dummy_data():
#     db = next(database.get_db())
#     for product in get_dummy_data():
#         db_product = models.Product(name=product["name"], price=product["price"], retailer=product["retailer"])
#         db.add(db_product)
#     db.commit()

# populate_dummy_data()
