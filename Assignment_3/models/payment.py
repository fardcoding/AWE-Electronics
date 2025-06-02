# models/payment.py

from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CardPayment(Payment):
    def process(self, amount: float) -> bool:
        print(f"💳 Processing card payment for ${amount:.2f}")
        # Simulate card payment logic
        return True

class PayPalPayment(Payment):
    def process(self, amount: float) -> bool:
        print(f"🅿️ Processing PayPal payment for ${amount:.2f}")
        # Simulate PayPal logic
        return True
