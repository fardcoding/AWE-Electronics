from interfaces.payment_method import PaymentMethod

class CardPayment(PaymentMethod):
    def __init__(self, card_number: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount: float) -> bool:
        # For now, simulate successful card transaction
        print(f"Processing card payment of ${amount} with card {self.card_number}")
        return True
