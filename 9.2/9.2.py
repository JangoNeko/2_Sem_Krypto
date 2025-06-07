import hashlib
import random



## Curve Values obtained from https://neuromancer.sk/std/nist/P-256#:
G  = [0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5]
aGlobal          = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
bGlobal          = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
nGlobal          = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
pGlobal        = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
'''
Aufgabe 1
'''
def multiply(point:list, scalar:int, a:int, n:int) -> list:
    bscalar = bin(scalar)[2:]

    l = len(bscalar) - 1
    h = point

    for bit in range(1, l+1):
        current = bscalar[bit]
        hsnake = double(h, a, n)

        if current == "1":
            h = add(hsnake, point, n)
        else:
            h = hsnake

    return h
def double(point:list, a:int, n:int) ->list:
    denum =  inverse(2*point[1], n)
    num = (3*pow(point[0], 2, n)+a) % n

    m = (denum*num) % n
    u = (pow(m, 2, n) - 2 * point[0]) % n
    v = (m * (u-point[0]) + point[1]) % n
    return [u, -v % n]

def add(point1:list, point2:list, n:int) -> list:
    denum = inverse(point2[0] - point1[0], n)
    num = (point2[1] - point1[1]) % n
    m = (denum * num) % n

    r = (pow(m, 2, n) - point1[0] - point2[0]) % n
    s = (m*(r - point1[0]) + point1[1]) % n
    return [r, -s % n]

def inverse(a:int, n:int) -> int:
    return pow(a, n-2, n)

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

def signature(fileIn:str, privKey:int, fileOut:str):
    with open(fileIn, 'rb') as inFile:
        message = bytes(inFile.read())

    k = random.randint(1, nGlobal)

    ecdsaSig = calcECDSA(privKey, message, k)[0]

    startSequence = b"\x30"
    intSequence = b"\x02"

    r = ecdsaSig[0]
    rLen = (r.bit_length() + 7) // 8
    rBytes = r.to_bytes(rLen, 'big')
    if rBytes[0] >= 0x80:
        rBytes = bytes(1) + rBytes
        rLen += 1

    s = ecdsaSig[1]
    sLen = (s.bit_length() + 7) // 8
    sBytes = s.to_bytes(sLen, 'big')
    if sBytes[0] >= 0x80:
        sBytes = bytes(1) + sBytes
        sLen += 1
    '''
    Aufgabe 2
    '''
    sig = bytearray()
    sig += intSequence + rLen.to_bytes(1, 'big') + rBytes
    sig += intSequence + sLen.to_bytes(1, 'big') + sBytes
    sig = startSequence + len(sig).to_bytes(1, 'big') + sig

    with open(fileOut, "wb") as sigFile:
        sigFile.write(sig)

    print(f"Message: {message}")
    print(f"Signature:\nr = {ecdsaSig[0]:x} \ns = {ecdsaSig[1]:x}")
    return[r, s]

'''
Aufgabe 3
'''
def getSig(fileIn:str):
    with open(fileIn, 'rb') as inFile:
        data = bytes(inFile.read())

    assert data[2] == 2
    rLen = data[3]
    r = int.from_bytes(data[4:4 + rLen], 'big')

    assert data[4 + rLen] == 2
    s = int.from_bytes(data[4 + rLen+2:], 'big')
    print(f"Got signature: \nr = {r:x} \ns = {s:x}")
    return [r, s]

def breakingBadECDSA(fileIn1:str, fileIn2:str, sigIn1:str, sigIn2:str):
        sig1 = getSig(sigIn1)
        sig2 = getSig(sigIn2)

        with open(fileIn1, 'rb') as inFile1:
            msg1 = bytes(inFile1.read())
        with open(fileIn2, 'rb') as inFile2:
            msg2 = bytes(inFile2.read())

        e1 = int.from_bytes(hashlib.sha256(msg1).digest(), 'big')
        e2 = int.from_bytes(hashlib.sha256(msg2).digest(), 'big')

        denum   = inverse(((sig1[1] * sig1[0] - sig2[1] * sig1[0]) % nGlobal), nGlobal)
        num = (sig2[1] * e1 - sig1[1] * e2) % nGlobal

        d = (num * denum) % nGlobal

        print(f"Found private Key d = {d:x}")
        return d

bauerKey1 = breakingBadECDSA("packages/1/message1.bin", "packages/1/message2.bin", "packages/1/signature1.bin", "packages/1/signature2.bin")
bauerKey2 = breakingBadECDSA("packages/2/message1.bin", "packages/2/message2.bin", "packages/2/signature1.bin", "packages/2/signature2.bin")

print(f"{bauerKey1:x}\n{bauerKey2:x}")

'''
Aufgabe 4
'''

privKey = 0x68747470733a2f2f74696e7975726c2e636f6d2f6d72336b357a667520202020

assert privKey < nGlobal

signature("message1.bin", privKey, "signature1.bin")
signature("message2.bin", privKey, "signature2.bin")