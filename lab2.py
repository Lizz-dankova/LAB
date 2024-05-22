import math
import time


def parcer(obj, n):
    args = [iter(obj)] * n
    return zip(*args)


def convert_to_hex(num):
    if num == [0]:
        return '0'
    i = len(num) - 1
    while num[i] == 0:
        i -= 1
        if i == -1:
            return '0'
    num.reverse()
    hex_num = ''
    for i in range(len(num)):
        hex_el = hex(num[i])[2:]
        if len(hex_el) != 8:
            zeros = (8 - len(hex_el)) * '0'
            hex_str = zeros + hex_el
            hex_num += hex_str
        else:
            hex_num += hex_el
        hex_num = hex_num.lstrip('0')
    num.reverse()
    return hex_num.swapcase()


def convert_from_hex(hex_num):
    n = math.ceil(len(hex_num) / 8)
    hexs = []
    decs = []
    if len(hex_num) % 8 == 0:
        hexs = [''.join(i) for i in parcer(hex_num, 8)]
    else:
        zeros = 8 * n - len(hex_num)
        str_zeros = zeros * '0'
        final_hex = str_zeros + hex_num
        hexs = [''.join(i) for i in parcer(final_hex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs


num_1_A = str(input('Enter the first number: '))
num_2_B = str(input('Enter the second number: '))

A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)


def LongAddition(a, b):
    max_len = max(len(a), len(b))
    carry = 0
    sum = []
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A + temp_B + carry
        sum.append(temp & (2 ** 32 - 1))
        carry = temp >> 32
    if carry > 0:
        sum.append(carry)
    return sum


def LongSubstraction(a, b):
    borrow = 0
    sub = []
    max_len = max(len(a), len(b))
    for i in range(max_len):
        temp_A = int(a[i]) if i < len(a) else 0
        temp_B = int(b[i]) if i < len(b) else 0
        temp = temp_A - temp_B - borrow
        if temp >= 0:
            sub.append(temp)
            borrow = 0
        else:
            sub.append((2 ** 32 + temp))
            borrow = 1
    if borrow != 0:
        return None
    else:
        return sub


def LongMultiply(a, b):
    if LongCompare(a, b) == -1:
        return LongMultiply(b, a)

    max_len = max(len(a), len(b))
    mul = [0] * (len(a) + len(b))

    for i in range(len(b)):
        carry = 0
        for j in range(len(a)):
            temp = mul[i + j] + a[j] * b[i] + carry
            mul[i + j] = temp & (2 ** 32 - 1)
            carry = temp >> 32

        if carry > 0:
            mul[i + len(a)] += carry

    while len(mul) > 1 and mul[-1] == 0:
        mul.pop()

    return mul


def LongDivideModule(a, b):
    k = BitLength(b)
    remainder = a
    div = []
    while LongCompare(remainder, b) != -1:
        t = BitLength(remainder)
        c = LongShiftBitsToHigh(b, t - k)
        if LongCompare(remainder, c) == -1:
            t -= 1
            while b[0] == 0:
                b = b[1:]
            c = LongShiftBitsToHigh(b, t - k)
        remainder = LongSubstraction(remainder, c)
        div = LongAddition(div, LongShiftBitsToHigh([1], t - k))
        while b[0] == 0:
            b = b[1:]
    return [div, remainder]


def LongSquare(a):
    return LongMultiply(a, a)


def LongPower(a, b):
    pow = [1]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            pow = LongMultiply(pow, a)
        a = LongMultiply(a, a)
        while len(a) < len(pow):
            a.append(0)
    return pow


def LongCompare(a, b):
    if a != [0]:
        while a[len(a) - 1] == 0:
            del a[len(a) - 1]
    if b != [0]:
        while b[len(b) - 1] == 0:
            del b[len(b) - 1]
    if len(a) == len(b):
        i = max(len(a), len(b)) - 1
        while a[i] == b[i]:
            i -= 1
            if i == -1:
                return 0
        else:
            if a[i] > b[i]:
                return 1
            else:
                return -1
    elif len(a) > len(b):
        return 1
    else:
        return -1


def LongShiftDigitsToHigh(n, l):
    for i in range(l):
        n.insert(0, 0)
    return n


def LongShiftBitsToLow(n, amount):
    if amount // 32 >= len(n):
        return convert_from_hex('0')
    if amount % 32 == 0:
        return LongShiftDigitsToLow(n, amount // 32)
    b = 32 - amount % 32
    k = 0 if n[len(n) - 1] >> 32 - b != 0 else 1
    result = [0] * (len(n) - k - amount // 32)
    if k == 0:
        result[len(n) - 1] = n[len(n) - 1] >> 32 - b
        i = len(result) - 2
    else:
        i = len(result) - 1
    for j in reversed(range(amount // 32 + 1, len(n))):
        result[i] = (n[j] << b) & (2 ** 32 - 1) | n[j - 1] >> 32 - b
        i -= 1
    return result


def LongShiftDigitsToLow(n, amount):
    if len(n) - amount <= 0:
        return [0]
    i = amount - 1
    while i > -1:
        del n[i]
        i -= 1
    return n


def LongShiftBitsToHigh(n, amount):
    if amount % 32 == 0:
        return LongShiftDigitsToHigh(n, amount // 32)
    b = 32 - amount % 32
    k = 1 if n[len(n) - 1] >> b != 0 else 0
    result = [0] * (len(n) + k + amount // 32)
    if k == 1:
        result[len(n) - 1] = n[len(n) - 1] >> b
        i = len(result) - 2
    else:
        i = len(result) - 1
    for j in reversed(range(1, len(n))):
        result[i] = (n[j] << 32 - b) & (2 ** 32 - 1) | n[j - 1] >> b
        i -= 1
    result[i] = (n[0] << 32 - b) & (2 ** 32 - 1)
    return result


def BitCheck(a, i):
    c = i % 32
    j = i // 32
    return (a[j] >> c) & 1


def BitLength(a):
    return (len(a) - 1) * 32 + a[len(a) - 1].bit_length()


def measure_time(func, *args, index=None):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time


# Time measurement and results calculation
sum_result, sum_time = measure_time(LongAddition, A, B)
sub_result, sub_time = measure_time(LongSubstraction, A, B)
mul_result, mul_time = measure_time(LongMultiply, A, B)
divide_result, div_time = measure_time(LongDivideModule, A, B)
square_result, square_time = measure_time(LongSquare, A)
pow_result, pow_time = measure_time(LongPower, A, B)

# Convert results to hex
sum_hex = convert_to_hex(sum_result) if sum_result is not None else "Error"
sub_hex = convert_to_hex(sub_result) if sub_result is not None else "Error"
mul_hex = convert_to_hex(mul_result) if mul_result is not None else "Error"

div_hex = convert_to_hex(divide_result[0]) if divide_result[0] != [] else '0'
div_mod_hex = convert_to_hex(divide_result[1])

square_hex = convert_to_hex(square_result) if square_result is not None else "Error"
pow_hex = convert_to_hex(pow_result) if pow_result is not None else "Error"

# Print results
print(f'The result of addition: {sum_hex}')
print(f'Time taken for addition: {sum_time} seconds')

print(f'The result of substraction: {sub_hex}')
print(f'Time taken for substraction: {sub_time} seconds')

print(f'The result of multiplication: {mul_hex}')
print(f'Time taken for multiplication: {mul_time} seconds')

print(f'The result of dividing: {div_hex}')
print(f'Time taken for dividing: {div_time} seconds')

print(f'The result of remainder of dividing: {div_mod_hex}')

print(f'The result of elevation to the square: {square_hex}')
print(f'Time taken for square: {square_time} seconds')

print(f'The result of elevation: {pow_hex}')
print(f'Time taken for power: {pow_time} seconds')
