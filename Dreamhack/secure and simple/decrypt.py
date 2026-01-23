from Crypto.Util.number import long_to_bytes, bytes_to_long

class Polynomial:
    def __init__(self, coeffs, n):
        self.coeffs = [c % n for c in coeffs]
        self.n = n
        self._remove_leading_zeros()
    
    def _remove_leading_zeros(self):
        while len(self.coeffs) > 1 and self.coeffs[0] == 0:
            self.coeffs = self.coeffs[1:]
    
    def degree(self):
        return len(self.coeffs) - 1
    
    def __mod__(self, other):
        if other.degree() < 0:
            raise ValueError("Division by zero polynomial")
        
        dividend = self.coeffs[:]
        divisor = other.coeffs
        n = self.n
        
        while len(dividend) >= len(divisor) and dividend[0] != 0:
            lead = dividend[0]
            div_lead = divisor[0]
            
            try:
                div_lead_inv = pow(div_lead, -1, n)
            except:
                from math import gcd
                g = gcd(div_lead, n)
                if g > 1 and g < n:
                    print(f"\n[!] Found factor during polynomial division: {g}")
                raise
            
            coeff = (lead * div_lead_inv) % n
            
            for i in range(len(divisor)):
                dividend[i] = (dividend[i] - coeff * divisor[i]) % n
            
            dividend = dividend[1:]
        
        return Polynomial(dividend if dividend else [0], n)
    
    def gcd(self, other):
        a = self
        b = other
        
        while b.degree() >= 0 and any(c != 0 for c in b.coeffs):
            a, b = b, a % b
        
        return a

def expand_binomial_power(a, b, e, n):
    from math import comb
    
    coeffs = []
    for i in range(e, -1, -1):
        coeff = comb(e, i) * pow(a, i, n) * pow(b, e - i, n)
        coeffs.append(coeff % n)
    
    return coeffs

def solve(N, e, admin_hash, guest_hash):
    admin_hash = bytes_to_long(bytes.fromhex(admin_hash))
    guest_hash = bytes_to_long(bytes.fromhex(guest_hash))

    f1_coeffs = [1] + [0] * (e - 1) + [(-admin_hash) % N]
    f1 = Polynomial(f1_coeffs, N)

    f2_coeffs = expand_binomial_power(365, 1337, e, N)
    f2_coeffs[-1] = (f2_coeffs[-1] - guest_hash) % N
    f2 = Polynomial(f2_coeffs, N)

    try:
        gcd_poly = f1.gcd(f2)
        
        if gcd_poly.degree() == 1:
            a_coeff = gcd_poly.coeffs[0]
            b_coeff = gcd_poly.coeffs[1]
            
            a_inv = pow(a_coeff, -1, N)
            root = (-b_coeff * a_inv) % N
            
            check_admin = pow(root, e, N)
            check_guest = pow((365 * root + 1337) % N, e, N)
            
            admin_match = check_admin == admin_hash
            guest_match = check_guest == guest_hash
            
            if admin_match and guest_match:
                password = long_to_bytes(root)

                return password.decode()
            else:
                print("\n[-] Verification failed. Solution incorrect.")
        else:
            print(f"[-] GCD is not linear (degree = {gcd_poly.degree()})")
            print(f"    GCD coefficients: {gcd_poly.coeffs[:5]}...")
            
    except Exception as ex:
        print(f"\n[!] Error during computation: {ex}")