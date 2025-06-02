import json
import os
from models.product import Product

class ProductCatalogue:
    _instance = None

    def __init__(self):
        self.products = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ProductCatalogue()
        return cls._instance

    def add_product(self, product: Product):
        self.products[product.product_id] = product
        self.save_to_file()  # auto-save on add

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_to_file()
        else:
            raise ValueError("Product not found.")

    def get_product_by_id(self, product_id):
        return self.products.get(product_id, None)

    def list_all_products(self):
        return list(self.products.values())

    def filter_by_category(self, category):
        return [p for p in self.products.values() if p.category.lower() == category.lower()]

    def save_to_file(self, filepath="data/products.json"):
        data = {
            pid: {
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "price": p.price,
                "stock": p.stock
            }
            for pid, p in self.products.items()
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filepath="data/products.json"):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                for pid, info in data.items():
                    self.products[pid] = Product(
                        pid,
                        info["name"],
                        info["description"],
                        info["category"],
                        info["price"],
                        info["stock"]
                    )
