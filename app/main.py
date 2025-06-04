from app.models.customer import Customer
from app.models.product import Product
from app.globals import users, products, save_all_users, save_all_products

# ✅ Only add sample products if the product list is empty
if not products:
    sample_products = [
        Product(id=1, name="Laptop", description="15-inch gaming laptop", category="Electronics", price=1500.00, stock=10),
        Product(id=2, name="Headphones", description="Noise-cancelling over-ear headphones", category="Audio", price=299.99, stock=25),
        Product(id=3, name="Smartphone", description="Latest Android smartphone", category="Mobile", price=999.99, stock=15)
    ]
    products.extend(sample_products)
    save_all_products()

# ✅ Add test customer if no users exist
if not users:
    test_customer = Customer(
        id=1,
        name="John Doe",
        email="john@example.com",
        password="password123",
        address="123 Test St",
        role="customer"
    )
    users.append(test_customer)

# ✅ Add admin user if not already present
if not any(u.email == "admin@awestore.com" for u in users):
    admin_user = Customer(
        id=len(users) + 1,
        name="Admin",
        email="admin@awestore.com",
        password="admin123",
        address="Admin HQ",
        role="admin"
    )
    users.append(admin_user)

# ✅ Save all users
save_all_users()

# ✅ Flask app init
from app import create_app
app = create_app()
