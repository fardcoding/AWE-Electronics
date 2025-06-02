# models/cart.py

from models.cart_item import CartItem
from models.product import Product

class ShoppingCart:
    def __init__(self):
        self.items = {}  # key = product_id, value = CartItem

    def add_item(self, product: Product, quantity: int):
        if product.product_id in self.items:
            self.items[product.product_id].quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product, quantity)

    def update_item(self, product_id: str, quantity: int):
        if product_id in self.items:
            if quantity <= 0:
                del self.items[product_id]
            else:
                self.items[product_id].update_quantity(quantity)
        else:
            raise ValueError("Item not in cart.")

    def remove_item(self, product_id: str):
        if product_id in self.items:
            del self.items[product_id]

    def view_cart(self):
        return [item.to_dict() for item in self.items.values()]

    def calculate_total(self):
        return sum(item.get_subtotal() for item in self.items.values())

    def is_empty(self):
        return len(self.items) == 0
