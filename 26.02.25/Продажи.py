import sys
from collections import defaultdict

customers = defaultdict(lambda: defaultdict(lambda: 0))

lines = sys.stdin
for line in lines:
    buyer, product, quantity = line.split()
    quantity = int(quantity)
    customers[buyer][product] += quantity

sorted_buyers = sorted(customers.keys())

for buyer in sorted_buyers:
    print(buyer + ":")
    sorted_products = sorted(customers[buyer].items())
    for product, total_quantity in sorted_products:
        print(product, total_quantity)