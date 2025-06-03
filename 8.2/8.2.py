'''
Aufgabenbestimmung: 241953 % 2 = 1
'''
import hashlib
# Hardcoded n und e, this feels illegal
rsa_modulus = 0xb8d8463e957ade9f8e8b66c18f1b00679c9c7cd6f54de3218c28cd6ef5033dda3431230d6b0b383d6512419edbf46c5bad8735e53fb8b64af9629ad82e3b9addad71b8b1923521e34c8786c4cffffefbf225fae736c166b885c8e39d78ea3ec85b2dfc8f3b42162cefe41e1e77e9189e339a9e5992759a1583cfd34bc769f34d
priv_exp = 78623796999251633338323312777140364726252697802134618368427573673092807514654446049976506370973352203762575389646273956621123649167743558804006203445056050183482856909796962592925703594229748024303724025485210445469550726592633531940551482598827406060505529447605487804799256641755595563852907252997613470973

def mgf(seed, length):
    T = b""
    counter = 0
    while len(T) < length:
        C = counter.to_bytes(4, 'big')
        T += hashlib.sha256(seed + C).digest()
        counter += 1
    return T[:length]

def rsa_decode(msg):                     #Enstschlüsselung mit RSA-Verfahren
    n = int(rsa_modulus)
    oaep = (pow(msg, priv_exp, n))
    return oaep.to_bytes(128, 'big')

def authenticate(hash, msg):             #gibt aus, ob der hash aus der verschlüsselten Message gleich dem hash des leeren Strings ist
    if hash == hashlib.sha1(msg).digest():
        return True
    else: return False

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def oaep_decode():

    with open("ciphertext-nik.bin", "rb") as f:
        encMsg = f.read()

    encMsg = int.from_bytes(encMsg, 'big')
    oaep = rsa_decode(encMsg)

    if oaep[0] != 0:
        print("error: no leading 0")
    assert oaep[0] == 0

    mskSeed = oaep[1:21]
    mskData = oaep[21:]

    seed = xor_bytes(mskSeed, mgf(mskData, len(mskSeed)))
    data = xor_bytes(mskData, mgf(seed, len(mskData)))

    hash = data[:20]
    rest = data[20:]

    Z = 0
    while Z < len(rest) and rest[Z] == 0:
        Z += 1
    if Z == len(rest) or rest[Z] != 0x01:
        print("error: no 01")
    assert Z == len(rest) or rest[Z] == 0x01

    msg = rest[Z + 1:]
    assert authenticate(hash, msg)
    print(msg)
#    with open("plaintext_self.bin", "wb") as f:
#        f.write(msg)
    return

oaep_decode()