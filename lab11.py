class LargeInteger:
    def __init__(self, value=0, bits=2048):
        self.bits = bits
        self.value = [0] * bits
        self.from_small_integer(value)

    def from_small_integer(self, n):
        for i in range(self.bits):
            self.value[i] = (n >> i) & 1

    def to_small_integer(self):
        result = 0
        for i in range(self.bits):
            result |= self.value[i] << i
        return result

    def LongAdd(self, A, B, C, carry=0):
        for i in range(self.bits):
            temp = A.value[i] + B.value[i] + carry
            C.value[i] = temp & 1
            carry = temp >> 1

    def LongSub(self, A, B, C, borrow=0):
        for i in range(self.bits):
            temp = A.value[i] - B.value[i] - borrow
            if temp < 0:
                C.value[i] = 1
                borrow = 1
            else:
                C.value[i] = temp & 1
                borrow = 0

    def LongMulOneDigit(self, A, b, C):
        carry = 0
        for i in range(self.bits):
            temp = A.value[i] * b + carry
            C.value[i] = temp & 1
            carry = temp >> 1

    def LongShiftDigitsToHigh(self, A, shift, C):
        for i in range(self.bits - shift):
            C.value[i + shift] = A.value[i]

    def LongMul(self, A, B, C):
        C.from_small_integer(0)
        for i in range(self.bits):
            if B.value[i] == 1:
                temp = LargeInteger()
                self.LongMulOneDigit(A, 1 << i, temp)
                self.LongAdd(C, temp, C)

    def LongCmp(self, A, B):
        for i in range(self.bits - 1, -1, -1):
            if A.value[i] < B.value[i]:
                return -1
            elif A.value[i] > B.value[i]:
                return 1
        return 0

    def LongShiftBitsToHigh(self, shift):
        self.value = [0] * shift + self.value

    def BitLength(self):
        for i in range(self.bits - 1, -1, -1):
            if self.value[i] != 0:
                return i + 1
        return 0

    def LongDivMod(self, B, Q, R):
        Q.from_small_integer(0)
        R.value = self.value[:]

        k = B.BitLength()

        while self.LongCmp(R, B) >= 0:
            t = R.BitLength()
            C = LargeInteger()
            C.LongShiftBitsToHigh(t - k)

            if self.LongCmp(R, C) < 0:
                t -= 1
                C = LargeInteger()
                C.LongShiftBitsToHigh(t - k)

            self.LongSub(R, C, R)
            Q_bit = LargeInteger(2 ** (t - k))
            self.LongAdd(Q, Q_bit, Q)

        return Q, R

    def LongPowerWindow(self, B, t):
        C = LargeInteger(1)
        D = [None] * (2 * t - 1)
        D[0] = LargeInteger(1)
        D[1] = self

        for i in range(2, 2 * t - 1):
            D[i] = LargeInteger()
            D[i].LongMul(D[1], D[i - 1], D[i])

        m = B.BitLength()
        b_values = [B.value[i] for i in range(m - 1, -1, -1)]

        for i in range(m - 1, -1, -1):
            C.LongMul(C, C, C)
            if b_values[i] == 1:
                C.LongMul(C, D[i], C)

        return C

    @classmethod
    def from_string(cls, string, base=10):
        if base == 10:
            return cls(int(string))
        elif base == 2:
            return cls(int(string, 2))
        elif base == 16:
            return cls(int(string, 16))
        else:
            raise ValueError("Unsupported base")

    def __eq__(self, other):
        return self.LongCmp(self, other) == 0

    def __lt__(self, other):
        return self.LongCmp(self, other) == -1

    def __le__(self, other):
        return self.LongCmp(self, other) <= 0

    def __gt__(self, other):
        return self.LongCmp(self, other) == 1

    def __ge__(self, other):
        return self.LongCmp(self, other) >= 0

    def __str__(self):
        first_nonzero = next((i for i, bit in enumerate(self.value) if bit), None)
        if first_nonzero is None:
            return "0"
        return "".join(str(bit) for bit in self.value[first_nonzero:])


# Приклад використання
A = LargeInteger(1234567890)
B = LargeInteger(12345)
Q = LargeInteger()
R = LargeInteger()

# Виведення результатів
print("A:", A)
print("B:", B)
print("A + B:", A + B)
print("A - B:", A - B)
print("A * B:", A * B)
print("A / B:", A / B)
print("A % B:", A % B)
print("A == B:", A == B)
print("A < B:", A < B)
print("A <= B:", A <= B)
print("A > B:", A > B)
print("A >= B:", A >= B)

# Використання методу LongPowerWindow
D = LargeInteger(2)
t = 5
result_power_window = A.LongPowerWindow(D, t)
print("Power Window Result:", result_power_window)

# Конвертування числа в символьну строку у різних системах числення
decimal_str = str(A)
binary_str = bin(A.to_small_integer())[2:]
hexadecimal_str = hex(A.to_small_integer())[2:]

print(f"Decimal: {decimal_str}")
print(f"Binary: {binary_str}")
print(f"Hexadecimal: {hexadecimal_str}")

# Обернене перетворення символьної строки у число
new_A = LargeInteger.from_string(hexadecimal_str, base=16)
print("New A:", new_A)
