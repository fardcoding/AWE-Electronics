import json
from app.globals import users, products

def save_all_users():
    data = [user.to_dict() for user in users]
    with open('data/users.json', 'w') as f:
        json.dump(data, f, indent=4)

def save_all_products():
    data = [product.to_dict() for product in products]
    with open('data/products.json', 'w') as f:
        json.dump(data, f, indent=4)
