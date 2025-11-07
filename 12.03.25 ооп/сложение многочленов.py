class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs
    
    def __call__(self, x):
        l = len(self.coeffs)
        return sum(coeff * x ** (i) 
                    for i, coeff in enumerate(self.coeffs))
    
    def __add__(self, other):
        min_len = min(len(self.coeffs), len(other.coeffs))
    
        new_coeffs = []
        for i in range(min_len):
            new_coeffs.append(self.coeffs[i] + other.coeffs[i])
        if len(self.coeffs) > len(other.coeffs):
            new_coeffs.extend(self.coeffs[min_len:])
        else:
            new_coeffs.extend(other.coeffs[min_len:])
        return Polynomial(new_coeffs)
    
poly1 = Polynomial([0, 1])
poly2 = Polynomial([10])
poly3 = poly1 + poly2
poly4 = poly2 + poly1
print(poly3.coeffs, poly4.coeffs)
print(poly3(-2), poly4(-2))
print(poly3(-1), poly4(-1))
print(poly3(0), poly4(0))
print(poly3(1), poly4(1))
print(poly3(2), poly4(2))