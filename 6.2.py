""" 6.2.1
Die SBox ist eine multiplikation über einen Galois-Körper.
Dies ist gegeben, da unser Körper mit F2^8 als Basis eine Primzahlpotenz hat und mit 256 Elementen endlich ist.
In Galois-Körpern haben alle Elemente ein inverses Element bis auf die 0.
Demnach kann die SBox invertiert werden, mit : Si^-1 = Si * {ab}^-1
"""
def gM(a, b):
    result = 0
    for index in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x1C3
        a &= 0xFF
        b >>= 1
    return result

def sbox():
    sbox = []
    i = 0
    while i < 256:
        sbox.insert(i, gM(i,0xAB))
        i += 1
    return sbox


def search(f, value):
    for i in range(len(f)):
        if f[i] == value:
            return i

lol = sbox()
# 6.2.2
print (f"{search(lol, 0x7b):02X}")                              # Gesucht ist das Inverse von 123, in Hexadezimal 0x7b. Das Inverse kann nach "Understanding Cryptology" über die Indizes der Lookup-Tabelle gefunden werden. Da meine Lookup-tabelle ein einziger String ist, muss ich nur den Index von 123 finden.
                                                                      # Das Inverse von 123 ist 0x72 oder 114
# 6.2.3
M = [
    0x59, 0x4f,
    0x4c, 0x4f,
]
B = [
    0xa3, 0xab,
    0xca, 0x05
]

def bes_mix_columns(B, M):                                          #Holzhammer FTW
    result = []
    result.append(f"{(gM(M[0], B[0]) ^ gM(M[2], B[2])):02X}")
    result.append(f"{(gM(M[1], B[0]) ^ gM(M[3], B[2])):02X}")
    result.append(f"{(gM(M[0], B[1]) ^ gM(M[2], B[3])):02X}")
    result.append(f"{(gM(M[1], B[1]) ^ gM(M[3], B[3])):02X}")
    return result

poorMonkey = ''.join(bes_mix_columns(B, M))
print(poorMonkey)

"""
A6.2.4
4BES ist anfällig für einen Meet-In-The-Middle-Angriff. 
Durch die 4 Rundenkeys wird nicht die theoretische Komplexität von 128B erreicht, denn wir können mit einem gegebenen C und P die Chiffre aufteilen. 
Im ersten Schritt verschlüsseln wir P mit allen möglichen Schlüsseln für K3 und K4 und legen die verschlüsselten Texte und Schlüssel in einer Liste ab. 
Im zweiten Schritt  entschlüsseln wir C mit allen möglichen Schlüsseln für K1 und K2 und gleichen sie mit der Liste aus dem erste Schritt ab.
So müssen wir nur 2 * 2^64 Schlüssel ausprobieren, daher erhalten wir eine Komplexität von 2^65 was eine Komplexität von maximal 65 Bit ergibt.
"""