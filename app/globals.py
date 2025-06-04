from app.utils.storage import load_data, save_data
from app.models.product import Product
from app.models.customer import Customer
from app.models.review import Review
from app.models.order import Order

# 🔗 File paths
PRODUCTS_FILE = 'data/products.json'
USERS_FILE = 'data/users.json'
ORDERS_FILE = 'data/orders.json'
REVIEWS_FILE = 'data/reviews.json'

# 📥 Load data from disk
products = [Product(**p) for p in load_data(PRODUCTS_FILE)]
users = [Customer(**u) for u in load_data(USERS_FILE)]
reviews = [Review(**r) for r in load_data(REVIEWS_FILE)]
orders = [Order(**o) for o in load_data(ORDERS_FILE)]  # ✅ Orders loaded persistently

# 💾 Save data helpers
def save_all_products():
    save_data([p.to_dict() for p in products], PRODUCTS_FILE)

def save_all_users():
    save_data([u.to_dict() for u in users], USERS_FILE)

def save_all_reviews():
    save_data([r.to_dict() for r in reviews], REVIEWS_FILE)

def save_all_orders():
    save_data([o.__dict__ for o in orders], ORDERS_FILE)  # ✅ Save orders to disk
