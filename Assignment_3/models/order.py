from models.cart import ShoppingCart
from models.payment import Payment

class Order:
    def __init__(self, customer, cart: ShoppingCart):
        self.customer = customer
        self.items = cart.items.copy()
        self.total = cart.calculate_total()
        self.status = "Pending"
        self.payment_method = None

    def process_payment(self, payment: Payment):
        success = payment.process(self.total)
        if success:
            self.status = "Paid"
            self.payment_method = payment.__class__.__name__
            return True
        else:
            self.status = "Payment Failed"
            return False

    def get_order_summary(self):
        return {
            "Customer": self.customer.username,
            "Total": self.total,
            "Status": self.status,
            "Payment Method": self.payment_method or "N/A",
            "Items": [item.to_dict() for item in self.items.values()]
        }
