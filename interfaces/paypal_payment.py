from interfaces.payment_method import PaymentMethod

class PayPalPayment(PaymentMethod):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        # Simulate successful PayPal transaction
        print(f"Processing PayPal payment of ${amount} from {self.email}")
        return True
