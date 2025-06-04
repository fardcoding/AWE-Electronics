from dataclasses import dataclass

@dataclass
class Review:
    def __init__(self, id, product_id, customer_id, rating, comment):
        self.id = id
        self.product_id = product_id
        self.customer_id = customer_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "rating": self.rating,
            "comment": self.comment
        }

