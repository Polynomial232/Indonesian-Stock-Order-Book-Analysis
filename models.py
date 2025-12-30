from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    price: int
    freq: int
    lot: int


@dataclass
class OrderBook:
    bid: List[Order]
    ask: List[Order]
    last_price: int
    volume: int
