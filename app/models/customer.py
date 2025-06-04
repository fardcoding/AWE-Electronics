from dataclasses import dataclass, field
from typing import List

@dataclass
class Customer:
    id: int
    name: str
    email: str
    password: str
    address: str
    role: str = "customer"  # can be "customer" or "admin"
    order_history: List[int] = field(default_factory=list)
    cart: List[int] = field(default_factory=list)

    def add_to_cart(self, product_id: int):
        self.cart.append(product_id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "role": self.role,
            "cart": self.cart,
            "order_history": self.order_history
        }
