# models/customer.py
from models.cart import ShoppingCart


class Customer:
    def __init__(self, username, full_name, email, address):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.address = address
        self.order_history = []
        self.cart = ShoppingCart()

    def update_profile(self, full_name=None, email=None, address=None):
        if full_name:
            self.full_name = full_name
        if email:
            self.email = email
        if address:
            self.address = address

    def view_profile(self):
        return {
            "Username": self.username,
            "Full Name": self.full_name,
            "Email": self.email,
            "Address": self.address
        }

    def add_order_to_history(self, order):
        self.order_history.append(order)
