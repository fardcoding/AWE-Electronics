from views.cli import CLI
from models.account import Account
from models.customer import Customer
from models.product import Product
from models.catalogue import ProductCatalogue
from models.order import Order
from models.payment import CardPayment, PayPalPayment
from models.cart import ShoppingCart

# Simulated customer "database"
customer_db = {}

def load_products():
    catalogue = ProductCatalogue.get_instance()
    catalogue.load_from_file()

    if not catalogue.products:  # Only add if empty
        catalogue.add_product(Product("P1001", "Wireless Mouse", "Ergonomic and battery-powered", "Accessories", 19.99, 20))
        catalogue.add_product(Product("P1002", "Mechanical Keyboard", "RGB backlit and fast typing", "Accessories", 59.99, 15))
        catalogue.add_product(Product("P2001", "1080p Monitor", "24-inch Full HD screen", "Displays", 129.99, 10))
        catalogue.add_product(Product("P3001", "Laptop", "14-inch, 16GB RAM, 512GB SSD", "Computers", 799.99, 5))



def browse_products():
    catalogue = ProductCatalogue.get_instance()
    print("\n🛒 Available Products:")
    for product in catalogue.list_all_products():
        print("-" * 40)
        for key, value in product.to_dict().items():
            print(f"{key}: {value}")

def register_user():
    print("\n--- Register ---")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    email = input("Enter your email: ")

    try:
        Account.register(username, password, email)
        print("✅ Registration successful!")
    except ValueError as e:
        print(f"❌ Registration failed: {e}")

def login_user():
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")

    user = Account.authenticate(username, password)
    if user:
        print(f"✅ Welcome back, {user.username}!")

        if username not in customer_db:
            customer = Customer(username, full_name="New User", email=user.email, address="Unknown")
            customer_db[username] = customer
        else:
            customer = customer_db[username]

        customer_dashboard(customer)
    else:
        print("❌ Invalid username or password.")

def customer_dashboard(customer: Customer):
    while True:
        print("\n--- Customer Dashboard ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Browse Products")
        print("4. Add Product to Cart")
        print("5. View Cart")
        print("6. Checkout")
        print("7. Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            profile = customer.view_profile()
            for key, value in profile.items():
                print(f"{key}: {value}")
        elif choice == '2':
            print("Leave blank to keep current value.")
            full_name = input("Full Name: ") or None
            email = input("Email: ") or None
            address = input("Address: ") or None
            customer.update_profile(full_name, email, address)
            print("✅ Profile updated.")
        elif choice == '3':
            browse_products()
        elif choice == '4':
            add_product_to_cart(customer)
        elif choice == '5':
            view_cart(customer)
        elif choice == '6':
            checkout(customer)
        elif choice == '7':
            print("👋 Logged out.")
            break
        else:
            print("❌ Invalid option.")

def add_product_to_cart(customer: Customer):
    catalogue = ProductCatalogue.get_instance()
    product_id = input("Enter Product ID to add to cart: ")
    product = catalogue.get_product_by_id(product_id)

    if product:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            if quantity > product.stock:
                print("❌ Not enough stock available.")
                return
            customer.cart.add_item(product, quantity)
            print("✅ Product added to cart.")
        except ValueError as ve:
            print(f"❌ {ve}")
    else:
        print("❌ Product not found.")

def view_cart(customer: Customer):
    print("\n🧺 Your Cart:")
    if customer.cart.is_empty():
        print("Cart is empty.")
        return

    for item in customer.cart.view_cart():
        print("-" * 40)
        for key, value in item.items():
            print(f"{key}: {value}")
    print("-" * 40)
    print(f"🧾 Total: ${customer.cart.calculate_total():.2f}")

def checkout(customer: Customer):
    if customer.cart.is_empty():
        print("❌ Your cart is empty.")
        return

    print("\n--- Checkout ---")
    print(f"Total amount: ${customer.cart.calculate_total():.2f}")
    print("Select payment method:")
    print("1. Card")
    print("2. PayPal")

    method = input("Enter choice (1 or 2): ")

    if method == '1':
        payment = CardPayment()
    elif method == '2':
        payment = PayPalPayment()
    else:
        print("❌ Invalid payment method.")
        return

    order = Order(customer, customer.cart)
    success = order.process_payment(payment)

    if success:
        customer.order_history.append(order)
        customer.cart = ShoppingCart()  # clear cart
        print("✅ Payment successful! Order placed.")
    else:
        print("❌ Payment failed.")

def main():
    while True:
        CLI.display_main_menu()
        choice = CLI.get_user_choice()

        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

# ✅ Entry point
if __name__ == "__main__":
    Account.load_users()
    load_products()  # ✅ Load products from JSON
    main()

