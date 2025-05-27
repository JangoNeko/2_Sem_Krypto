import hashlib
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

def rsa_decode(msg):
    n = int(rsa_modulus)
    oaep = (pow(msg, priv_exp, n))
    return oaep.to_bytes(128, 'big')

def authenticate(hash, msg):
    if hash == hashlib.sha1(msg).digest():
        return True
    else: return False

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def oaep_decode():
    '''
    with open("test.bin", "rb") as f:
        encMsg = f.read()
    '''
    encMsg = 0x70E40522221907D40B09A48E5E64F20B867479B484CDE3B713CC309F9152A19C12850D83759888045B52D36D59E6AC4316A96C5035DBB78443F27F1452FAF38CA25EA8414F13AF48CBFE1506E706EE2896A3236616EA0897B6E994B094680F5835D8CF3CF7FB470F527450E07BAD7D173FE668EEAC8944D8B666A3A5AEC7CA92
    print(encMsg)
    #encMsg = int.from_bytes(encMsg, 'big')
    oaep = rsa_decode(encMsg)

    print(oaep.hex())

    if oaep[0] != 0:
        print("error: no leading 0")
        return

    mskSeed = oaep[1:21]
    mskData = oaep[21:]

    seed = xor_bytes(mskSeed, mgf(mskData, len(mskSeed)))
    data = xor_bytes(mskData, mgf(seed, len(mskData)))

    hash = data[:20]
    rest = data[20:]
    print(data.hex())
    print(hash.hex())
    print(rest.hex())
    Z = 0
    while Z < len(rest) and rest[Z] == 0:
        Z += 1
    if Z == len(rest) or rest[Z] != 0x01:
        print("error: no 01")
        return

    msg = rest[Z + 1:]

    assert authenticate(hash, msg)
    return msg.decode('utf-8')

print(oaep_decode())