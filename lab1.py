class LargeInteger:
    def __init__(self, value=0, bits=2048):
        self.bits = bits
        self.value = [(value >> i) & 1 for i in range(bits)]

    def long_add(self, A, B, C, carry=0):
        for i in range(A.bits):
            temp = A.value[i] + B.value[i] + carry
            C.value[i] = temp % 2
            carry = temp // 2
        if carry:
            raise ValueError("Overflow in addition")

    def long_sub(self, A, B, C, borrow=0):
        for i in range(A.bits):
            temp = A.value[i] - B.value[i] - borrow
            if temp < 0:
                C.value[i] = 1
                borrow = 1
            else:
                C.value[i] = temp % 2
                borrow = 0
        if borrow:
            raise ValueError("Underflow in subtraction")

    def long_mul_one_digit(self, A, b, C):
        carry = 0
        for i in range(A.bits):
            temp = A.value[i] * b + carry
            C.value[i] = temp % 2
            carry = temp // 2
        if carry:
            raise ValueError("Overflow in multiplication")

    def long_shift_digits_to_high(self, A, shift, C):
        C.value[shift:] = A.value[:-shift]

    def long_mul(self, A, B, C):
        C.value = [0] * (2 * A.bits)
        for i in range(A.bits):
            if B.value[i] == 1:
                temp = LargeInteger()
                self.long_mul_one_digit(A, 1 << i, temp)
                self.long_add(C, temp, C)

    def long_cmp(self, A, B):
        for i in range(A.bits - 1, -1, -1):
            if A.value[i] < B.value[i]:
                return -1
            elif A.value[i] > B.value[i]:
                return 1
        return 0

    def long_shift_bits_to_high(self, A, shift):
        A.value[shift:] = A.value[:-shift]

    def bit_length(self, A):
        return next((i + 1 for i, bit in enumerate(reversed(A.value)) if bit), 0)

    def long_div_mod(self, A, B, Q, R):
        Q.value = [0] * A.bits
        R.value = A.value[:]

        k = B.bit_length()

        while self.long_cmp(R, B) >= 0:
            t = self.bit_length(R)
            C = LargeInteger()
            self.long_shift_bits_to_high(C, t - k)

            if self.long_cmp(R, C) < 0:
                t -= 1
                self.long_shift_bits_to_high(C, t - k)

            self.long_sub(R, C, R)
            Q_bit = LargeInteger(2 ** (t - k))
            self.long_add(Q, Q_bit, Q)

        return Q, R

    def long_power_window(self, A, B, t):
        C = LargeInteger(1)
        D = [LargeInteger(1) if i == 1 else LargeInteger() for i in range(2, 2 * t)]
        D[1] = A

        m = B.bit_length()
        b_values = [B.value[i] for i in range(m - 1, -1, -1)]

        for i in range(m - 1, -1, -1):
            C.long_mul(C, C, C)
            if b_values[i] == 1:
                C.long_mul(D[i], C, C)

        return C

    @classmethod
    def from_string(cls, string, base=10):
        base_conversion = {2: 2, 10: 10, 16: 16}
        if base not in base_conversion:
            raise ValueError("Unsupported base")
        return cls(int(string, base_conversion[base]))

    def __add__(self, other):
        result = LargeInteger(bits=max(self.bits, other.bits))
        self.long_add(self, other, result)
        return result

    def __sub__(self, other):
        result = LargeInteger(bits=max(self.bits, other.bits))
        self.long_sub(self, other, result)
        return result

    def __mul__(self, other):
        result = LargeInteger(bits=self.bits + other.bits)
        self.long_mul(self, other, result)
        return result

    def __floordiv__(self, other):
        if isinstance(other, LargeInteger) and other != 0:
            quotient, remainder = LargeInteger(), LargeInteger()
            self.long_div_mod(self, other, quotient, remainder)
            return quotient
        raise ValueError("Division by zero or non-LargeInteger operand")

    def __mod__(self, other):
        if isinstance(other, LargeInteger) and other != 0:
            quotient, remainder = LargeInteger(), LargeInteger()
            self.long_div_mod(self, other, quotient, remainder)
            return remainder
        raise ValueError("Modulo by zero or non-LargeInteger operand")

    def __eq__(self, other):
        return isinstance(other, LargeInteger) and self.long_cmp(self, other) == 0

    def __lt__(self, other):
        return isinstance(other, LargeInteger) and self.long_cmp(self, other) == -1

    def __le__(self, other):
        return isinstance(other, LargeInteger) and self.long_cmp(self, other) <= 0

    def __gt__(self, other):
        return isinstance(other, LargeInteger) and self.long_cmp(self, other) == 1

    def __ge__(self, other):
        return isinstance(other, LargeInteger) and self.long_cmp(self, other) >= 0

    def __str__(self):
        first_nonzero = next((i for i, bit in enumerate(self.value) if bit), None)
        return "0" if first_nonzero is None else "".join(map(str, self.value[first_nonzero:]))


# Example usage
A = LargeInteger(1234567890)
B = LargeInteger(12345)
Q = LargeInteger()
R = LargeInteger()

print("A:", A)
print("B:", B)
print("A + B:", A + B)
print("A - B:", A - B)
print("A * B:", A * B)
print("A / B:", A // B)
print("A % B:", A % B)
print("A == B:", A == B)
print("A < B:", A < B)
print("A <= B:", A <= B)
print("A > B:", A > B)
print("A >= B:", A >= B)

D = LargeInteger(2)
t = 5
result_power_window = A.long_power_window(D, t)
print("Power Window Result:", result_power_window)

decimal_str = str(A)
binary_str = bin(A.to_small_integer())[2:]
hexadecimal_str = hex(A.to_small_integer())[2:]

print(f"Decimal: {decimal_str}")
print(f"Binary: {binary_str}")
print(f"Hexadecimal: {hexadecimal_str}")

new_A = LargeInteger.from_string(hexadecimal_str, base=16)
print("New A:", new_A)
