from sys import byteorder


def sbox(s):
    s = [s]
    i = 1
    while i < 256:
        s.insert(i, (37 * s[i-1] + 9) % 256)
        i += 1
    assert(s[0] == 170)
    assert(s[1] == 155)
    assert(s[2] == 112)
    assert(s[123] == 33)
    assert(s[255] == 205)
    return s

def keygen(key, rounds):
    if isinstance(key, str):
        key = int(key, 16)
    i = 0
    key = ((((key << ((7 * i) % 128)) | (key >> (128 - ((7 * i) % 128))))& ((1<<128)-1)) ^ 0xabcdef)
    keys = [key]
    i = 1
    while i < rounds:
        keys.append(((((keys[i-1] << ((7 * i) % 128)) | (keys[i - 1] >> (128 - ((7 * i) % 128))))& ((1<<128)-1)) ^ 0xabcdef))
        i += 1
    assert(f"{keys[0]:032x}" == "deadbeef000000000000000bad6b3201")
    assert(f"{keys[1]:032x}" == "56df778000000000000005d6b532cd00")
    assert(f"{keys[2]:032x}" == "dde00000000000000175ad4cb3ebd858")
    assert(f"{keys[31]:032x}" == "770feb4b3180dc3bc09870bd38e2cb5f")
    return keys


def schiffy(key, msg):

    if isinstance(msg, str):
        msg = int(msg, 2)
    key = keygen("deadbeef000000000000000badc0ffee", 32)
    box = sbox(170)
    i = 0
    while i < 32:
        print(f"msg: {hex(msg)}")
        roundkey = key[i]
        print(f"roundkey: {hex(roundkey)}")
        msb = (roundkey >> 64)
        print(f"msb: {hex(msb)}")
        lsb = roundkey & 0xFFFFFFFFFFFFFFFF
        print(f"lsb: {hex(lsb)}")
        msg = (msg ^ msb)
        print(f"msg nach msb: {hex(msg)}")
        smsg = 0
        for ii in range(8):
            tmp = (msg >> (8 * (7 - ii))) & 0xFF
            smsg = (smsg << 8 ) + box[tmp]
        msg = smsg ^ lsb
        print(f"msg nach runde {i + 1}: {hex(msg)}\n---------------------------")
        if i == 0:
            assert hex(msg)[2:] == "94dfb49607c198ab"
        if i == 1:
            assert hex(msg)[2:] == "b0aa7cca50e95fb1"
        if i == 2:
            assert hex(msg)[2:] == "1e9d6324e9783573"
        if i == 3:
            assert hex(msg)[2:] == "01a6283b0f33c8f0"
        if i == 29:
            assert hex(msg)[2:] == "f7ffea032144154a"
        if i == 30:
            assert hex(msg)[2:] == "7fac6b4146d4f4c6"
        if i == 31:
            assert hex(msg)[2:] == "2a66d3471f7cb499"
        i += 1
    return hex(msg)



print(schiffy("deadbeef000000000000000badc0ffee", "00000000000000000000000000000000"))
