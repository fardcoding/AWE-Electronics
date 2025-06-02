# models/cart_item.py

from models.product import Product

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def update_quantity(self, new_quantity: int):
        if new_quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.quantity = new_quantity

    def get_subtotal(self):
        return self.product.price * self.quantity

    def to_dict(self):
        return {
            "Product ID": self.product.product_id,
            "Name": self.product.name,
            "Quantity": self.quantity,
            "Unit Price": self.product.price,
            "Subtotal": self.get_subtotal()
        }
