import hashlib
from Aufgabe9 import multiply, inverse

## Curve Values obtained from https://neuromancer.sk/std/nist/P-256#:
G  = [0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5]
aGlobal          = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
bGlobal          = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
nGlobal          = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
pGlobal        = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
'''
Aufgabe 1
'''
def calcECDSA(d:int, m:bytes, k:int)->int:
    e = int.from_bytes(hashlib.sha256(m).digest(), 'big')               # Calculate H(m)
    Q = multiply(G, d, aGlobal, pGlobal)                            #
    R = multiply(G, k, aGlobal, pGlobal)
    r = R[0] % nGlobal
    assert r != 0
    kInv = inverse(k, nGlobal)

    s = (((e + r * d) % nGlobal) * kInv) % nGlobal
    assert s != 0

    return [r, s], Q
