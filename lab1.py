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
    if not num or num == [0]:
        return '0'
    num.reverse()
    hex_num = ''.join(f'{x:08x}' for x in num).lstrip('0').swapcase()
    num.reverse()
    return hex_num or '0'


def convert_from_hex(hex_num):
    n = math.ceil(len(hex_num) / 8)
    hex_num = hex_num.zfill(n * 8)
    hexs = [''.join(i) for i in parser(hex_num, 8)]
    decs = [int(hex_str, 16) for hex_str in hexs]
    decs.reverse()
    return decs


num_1_A = input('Enter the first number: ')
num_2_B = input('Enter the second number: ')
num_Module = input('Enter the module: ')

A = convert_from_hex(num_1_A)
B = convert_from_hex(num_2_B)
Module = convert_from_hex(num_Module)


'''Основні функції'''


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


'''Додаткові функції'''


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


'''Lab--2'''


def GCD(a, b):
    divisor = [1]
    compare = 0
    col_vo_sub = 0
    while a[0] % 2 == 0 and b[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
        b = LongShiftBitsToLow(b, 1)
        divisor = LongShiftBitsToHigh(divisor, 1)
    while a[0] % 2 == 0:
        a = LongShiftBitsToLow(a, 1)
    while LongCompare(b, [0]) != 0:
        compare += 1
        while b[0] % 2 == 0:
            b = LongShiftBitsToLow(b, 1)
        compare_of_number = LongCompare(a, b)
        compare += 1
        if compare_of_number == 1:
            min_ab = b
            sub = LongSubtraction(a, b)
        elif compare_of_number == -1:
            min_ab = a
            sub = LongSubtraction(b, a)
        else:
            min_ab = b
            sub = [0]
        col_vo_sub += 1
        a = min_ab
        b = sub
    divisor = LongMultiply(divisor, a)
    return divisor, compare, col_vo_sub


def EvklidGCD(a, b):
    compare = 0
    div = 0
    while LongCompare(a, [0]) != 0 and LongCompare(b, [0]) != 0:
        compare_of_number = LongCompare(a, b)
        compare += 3
        if compare_of_number == 1:
            a = LongDivideModule(a, b)[1]
        elif compare_of_number == -1:
            b = LongDivideModule(b, a)[1]
        else:
            b = [0]
        div += 1
    res = LongAddition(a, b)
    return res, compare, div


def LCM(a, b):
    gcd = GCD(a, b)[0]
    multiply = LongMultiply(a, b)
    result = LongDivideModule(multiply, gcd)[0]
    return result


def evaluateMu(module):
    k = len(module)
    ß = LongShiftDigitsToHigh([1], 2 * k)
    µ = LongDivideModule(ß, module)[0]
    return µ


def BarrettReduction(value, module, mu):
    k = len(module)
    q = LongShiftBitsToLow(value.copy(), (k - 1) * 32)
    q = LongMultiply(q, mu)
    q = LongShiftBitsToLow(q, (k + 1) * 32)
    reduction = LongSubtraction(value.copy(), LongMultiply(q, module))
    while LongCompare(reduction, module) >= 0:
        reduction = LongSubtraction(reduction, module)
    return reduction


def LongAdditionModule(a, b, mod):
    sum = LongAddition(a, b)
    return LongDivideModule(sum, mod)[1]


def LongSubtractionModule(a, b, mod):
    if LongCompare(a, b) == -1:
        while LongCompare(a, b) == -1:
            a = LongAddition(a, mod)
        sub = LongSubtraction(a, b)
    else:
        sub = LongSubtraction(a, b)
    return LongDivideModule(sub, mod)[1]


def LongMultiplyModule(a, b, mod):
    µ = evaluateMu(mod)
    mul = LongMultiply(a, b)
    return BarrettReduction(mul, mod, µ)


def LongSquareMod(a, mod):
    return LongMultiplyModule(a, a, mod)


def LongModulePower(a, b, mod):
    a_mod = LongDivideModule(a, mod)[1]
    b_mod = LongDivideModule(b, mod)[1]
    pow = [1]
    µ = evaluateMu(mod)
    for i in range(BitLength(b_mod)):
        if BitCheck(b_mod, i) == 1:
            pow = BarrettReduction(LongMultiply(pow, a_mod), mod, µ)
        a_mod = BarrettReduction(LongSquare(a_mod), mod, µ)
    return pow


gcd_result, gcd_time = measure_time(GCD, A, B, index=0)
print(f'GCD = {convert_to_hex(gcd_result)}')
print(f'Time taken for GCD: {gcd_time} seconds')

lcm_result, lcm_time = measure_time(LCM, A, B)
print(f'LCM = {convert_to_hex(lcm_result)}')
print(f'Time taken for LCM: {lcm_time} seconds')

mod_sum_result, mod_sum_time = measure_time(LongAdditionModule, A, B, Module)
print(f'(A+B)modModule = {convert_to_hex(mod_sum_result)}')
print(f'Time taken for (A+B)modModule: {mod_sum_time} seconds')

mod_sub_result, mod_sub_time = measure_time(LongSubtractionModule, A, B, Module)
print(f'(A-B)modModule = {convert_to_hex(mod_sub_result)}')
print(f'Time taken for (A-B)modModule: {mod_sub_time} seconds')

mod_mul_result, mod_mul_time = measure_time(LongMultiplyModule, A, B, Module)
print(f'(A*B)modModule = {convert_to_hex(mod_mul_result)}')
print(f'Time taken for (A*B)modModule: {mod_mul_time} seconds')

mod_sq_result, mod_sq_time = measure_time(LongSquareMod, A, Module)
print(f'(A**2)modModule = {convert_to_hex(mod_sq_result)}')
print(f'Time taken for (A**2)modModule: {mod_sq_time} seconds')

mod_pow_result, mod_pow_time = measure_time(LongModulePower, A, B, Module)
print(f'(A**B)modModule = {convert_to_hex(mod_pow_result)}')
print(f'Time taken for (A**B)modModule: {mod_pow_time} seconds')
