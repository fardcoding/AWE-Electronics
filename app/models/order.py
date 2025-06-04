from dataclasses import dataclass
from typing import List

@dataclass
class Order:
    id: int
    customer_id: int
    product_ids: List[int]
    total_amount: float
