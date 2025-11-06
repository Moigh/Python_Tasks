def calculate_order_cost(quantity, price, discount=0, tax=0):
    
    base_cost = quantity * price
    cost_after_discount = base_cost * (1 - discount)
    final_cost = cost_after_discount * (1 + tax)

    return round(final_cost, 2)

calculate_order_cost(5, 10)
calculate_order_cost(5, 10, discount=0.1)
calculate_order_cost(5, 10, tax=0.2)
calculate_order_cost(quantity=5, price=10)