def square_and_multiply(base, exp, mod):
    binary_exp = bin(exp)[2:]
    res = 1
    temp = base % mod
    for i, bit in enumerate(reversed(binary_exp)):
        print(f"Bit {i}: {bit}")
        if bit == '1':
            res = (res * temp) % mod
            print(f"Zwischenergebnis: {res}")
        temp = (temp ** 2) % mod
        print(f"aktuelle Potenz: {temp}")
    return res

a = 2282
k = 1762
N = 4703
print(f"ergebnis: {a} ^ {k} mod {N} = {square_and_multiply(a, k, N)}")