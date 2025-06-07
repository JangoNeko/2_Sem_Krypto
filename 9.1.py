def inverse(a:int, n:int) -> int:
    return pow(a, n-2, n)

def double(point:list, a:int, n:int) ->list:
    denum =  inverse(2*point[1], n)
    num = (3*pow(point[0], 2, n)+a) % n

    m = (denum*num) % n
    print(f"m = {m}")
    u = (pow(m, 2, n) - 2 * point[0]) % n
    v = (m * (u-point[0]) + point[1]) % n
    return [u, -v % n]

def add(point1:list, point2:list, n:int) -> list:
    denum = inverse(point2[0] - point1[0], n)
    num = (point2[1] - point1[1]) % n

    m = (denum * num) % n
    print(f"m = {m}")
    r = (pow(m, 2, n) - point1[0] - point2[0]) % n
    s = (m*(r - point1[0]) + point1[1]) % n 
    return [r, -s % n]

def multiply(point:list, scalar:int, a:int, n:int) -> list:
    bscalar = bin(scalar)[2:]
    print(f"scalar: {scalar} = 0b{bscalar}\n")
    l = len(bscalar) - 1
    h = point
    print(f"i = l = {l}, h{l} = p = ({point[0]:02}, {point[1]:02})\n")
    for bit in range(1, l+1):
        current = bscalar[bit]
        hsnake = double(h, a, n)
        print(f"i = {l-bit}, b{l-bit} = {current}")
        print(f"hsnake = {hsnake}")
        if current == "1":
            h = add(hsnake, point, n)
            print(f"b{l-bit} = {current} -> h = hsnake + P = {hsnake} + ({point[0]:02}, {point[1]:02}) = ({h[0], h[1]})\n")
        else:
            h = hsnake
            print(f"b{l - bit} = {current} -> h = hsnake = {h}\n")
    print(f"{scalar} * ({point[0]:02}, {point[1]:02}) = ({h[0], h[1]})\n")
    return h

'''
    Berechnung der Aufgabe
'''
# Domain-Parameters
p0 = [12,17]
a = 16
b = 9
n = 41
print(f"Domain parameters: \nF[X, Y] = Y^2 - X^3 - {a}X - {b}\na = {a}, b = {b}, n = {n}\n")

# Alices Schlüsselberechnung
print("Task a)\n")
kprA = 17
kpubA = multiply(p0, kprA, a, n)

# Bobs Schlüsselberechnung
print("Task b)\n")
kprB = 19
kpubB = multiply(p0, kprB, a, n)

# Berechnug der gemeinsamen Schlüssel
print("Task c)\n")
kAB = multiply(kpubA, kprB, a, n)
kBA = multiply(kpubB, kprA, a, n)

print(f"Alices keypair: kprA = {kprA}, kpubA = {kpubA}\nAlices common Key kBA = {kBA}\n")
print(f"Bobs keypair: kprB = {kprB}, kpubB = {kpubB}\nBobs common Key kAB = {kAB}")
