import json
from typing import List, Any

from django.db import models

# Create your models here.
class Product:
    def __init__(self, product_name: str, product_cost: str):
        self.product_name = product_name
        self.product_cost = product_cost
    def __repr__(self):
        return f"product(name='{self.product_name}', cost='{self.product_cost}'"
class Order:
    def __init__(self, total_cost: int, products: List[Product], state: str):
        self.total_cost = total_cost
        self.products = products
        self.state = state
        # self.destination = destination
    def __repr__(self):
        return f"order(total_cost='{self.total_cost}', state='{self.state}', destination='{self.destination}'"
class Customer:
    def __init__(self, customer_id: str, customer_name: str, gender: str, orders: List[Order]):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.gender = gender
        self.orders = orders

    def __repr__(self):
        return f"customer(name='{self.customer_name}', gender='{self.gender}'"
class SessionData:
    def __init__(self, type: str, header: Any, data: Any):
        self.type = type
        self.header = header
        self.data = data
    def __repr__(self):
        return json.dumps(self)