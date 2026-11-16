from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    category: str
    material_category: str
    base_price: Decimal
