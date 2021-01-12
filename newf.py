from decimal import Decimal
TWOPLACES = Decimal(10) ** -2
id_weight = Decimal('41.20').quantize(TWOPLACES)
print(id_weight)
