import math
import time


def measure_time(func, *args, index=None):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    if index is not None:
        result = result[index]
    return result, execution_time


def parser(obj, n):
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
        hexs = [''.join(i) for i in parser(hex_num, 8)]
    else:
        zeros = 8 * n - len(hex_num)
        str_zeros = zeros * '0'
        final_hex = str_zeros + hex_num
        hexs = [''.join(i) for i in parser(final_hex, 8)]
    for i in range(len(hexs)):
        decs.append(int(hexs[i], 16))
    decs.reverse()
    return decs


def convert_result_to_hex(result):
    return convert_to_hex(result)

num_1_A = input('Перше число: ')
num_2_B = input('Друге число: ')


A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)

def LongAddition(a, b):
    max_len = max(len(a), len(b))
    carry = 0
    sum = []
    for i in range(max_len):
        temp_A = a[i] if i < len(a) else 0
        temp_B = b[i] if i < len(b) else 0
        temp = temp_A + temp_B + carry
        sum.append(temp & (2 ** 32 - 1))
        carry = temp >> 32
    if carry > 0:
        sum.append(carry)
    return sum


def LongSubtraction(a, b):
    borrow = 0
    sub = []
    max_len = max(len(a), len(b))
    for i in range(max_len):
        temp_A = a[i] if i < len(a) else 0
        temp_B = b[i] if i < len(b) else 0
        temp = temp_A - temp_B - borrow
        if temp >= 0:
            sub.append(temp)
            borrow = 0
        else:
            sub.append(temp + (2 ** 32))
            borrow = 1
    if borrow:
        return None
    while len(sub) > 1 and sub[-1] == 0:
        sub.pop()
    return sub


def LongMultiply(a, b):
    if LongCompare(a, b) == -1:
        a, b = b, a

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
    if a == b:
        return [1], [0]
    k = BitLength(b)
    remainder = a.copy()
    quotient = [0]
    while LongCompare(remainder, b) != -1:
        t = BitLength(remainder)
        c = LongShiftBitsToHigh(b, t - k)
        if LongCompare(remainder, c) < 0:
            t -= 1
            c = LongShiftBitsToHigh(b, t - k)
        remainder = LongSubtraction(remainder, c)
        temp = LongShiftBitsToHigh([1], t - k)
        quotient = LongAddition(quotient, temp)
    return quotient, remainder


def LongSquare(a):
    return LongMultiply(a, a)


def LongPower(a, b):
    pow = [1]
    for i in range(BitLength(b)):
        if BitCheck(b, i) == 1:
            pow = LongMultiply(pow, a)
        a = LongMultiply(a, a)
    return pow


def LongCompare(a, b):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    if len(a) == len(b):
        for i in range(len(a) - 1, -1, -1):
            if a[i] != b[i]:
                return 1 if a[i] > b[i] else -1
        return 0
    return 1 if len(a) > len(b) else -1


def LongShiftDigitsToHigh(n, l):
    return [0] * l + n


def LongShiftDigitsToLow(n, amount):
    return n[amount:] if len(n) > amount else [0]


def LongShiftBitsToHigh(number, width_shift):
    if width_shift <= 0:
        return number.copy()
    remainder = width_shift % 32
    width_shift //= 32
    result = LongShiftDigitsToHigh(number.copy(), width_shift)
    if remainder > 0:
        for _ in range(remainder):
            last_bit = (result[-1] >> 31) & 1
            for j in range(len(result) - 1, 0, -1):
                result[j] = ((result[j] << 1) | ((result[j - 1] >> 31) & 1)) & 0xFFFFFFFF
            result[0] = (result[0] << 1) & 0xFFFFFFFF
            if last_bit != 0:
                result.append(last_bit)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def LongShiftBitsToLow(number, width_shift):
    if width_shift <= 0:
        return number
    remainder = width_shift % 32
    width_shift //= 32
    result = number[width_shift:] if width_shift < len(number) else [0]
    if remainder > 0:
        for _ in range(remainder):
            last_bit = (result[0] & 1) << 31
            for j in range(len(result) - 1):
                result[j] = ((result[j] >> 1) | ((result[j + 1] & 1) << 31)) & 0xFFFFFFFF
            result[-1] = ((result[-1] >> 1) | last_bit) & 0xFFFFFFFF
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def BitCheck(a, i):
    return (a[i // 32] >> (i % 32)) & 1


def BitLength(a):
    return (len(a) - 1) * 32 + a[-1].bit_length()

sum_result = LongAddition(A, B)
sum_hex = convert_result_to_hex(sum_result)
sub_result = LongSubtraction(A, B)
sub_hex = convert_result_to_hex(sub_result)
mul_result = LongMultiply(A, B)
mul_hex = convert_result_to_hex(mul_result)
divide_result = LongDivideModule(A, B)
div = convert_result_to_hex(divide_result[0]) if divide_result[0] != [] else '0'
div_mod = convert_result_to_hex(divide_result[1])
pow_result = LongPower(A, B)
pow_hex = convert_result_to_hex(pow_result)
square_result = LongSquare(A)
square = convert_result_to_hex(square_result)
#pow = convert_to_hex(LongPower(A, B))

#Time
pow_result, pow_time = measure_time(LongPower, A, B)
sum_result, sum_time = measure_time(LongAddition, A, B)
sub_result, sub_time = measure_time(LongSubtraction, A, B)
mul_result, mul_time = measure_time(LongMultiply, A, B)
divide_result, div_time = measure_time(LongDivideModule, A, B)
square_result, square_time = measure_time(LongSquare, A)
pow_result, pow_time = measure_time(LongPower, A, B)


print(f'Додавання: {sum_hex}, Час виконання: {sum_time} секунд')
print(f'Віднімання: {sub_hex}, Час виконання: {sub_time} секунд')
print(f'Множення: {mul_hex}, Час виконання: {mul_time} секунд')
print(f'Ділення: {div}, Час виконання: {div_time} секунд' )
print(f'Остача: {div_mod}')
print(f'Піднесення до квадрату: {square}, Час виконання: {square_time} секунд')
print(f'Піднесення у степінь: {pow_hex}, Час виконання: {pow_time} секунд')

