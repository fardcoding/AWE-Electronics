# models/product.py

class Product:
    def __init__(self, product_id, name, description, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.stock = quantity

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock available.")
        self.stock -= quantity

    def is_available(self):
        return self.stock > 0

    def to_dict(self):
        return {
            "Product ID": self.product_id,
            "Name": self.name,
            "Description": self.description,
            "Category": self.category,
            "Price": self.price,
            "Stock": self.stock
        }
