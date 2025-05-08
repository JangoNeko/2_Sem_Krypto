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
    key = ((((key << ((7 * 0) % 128)) | (key >> (128 - ((7 * 0) % 128))))& ((1<<128)-1)) ^ 0xabcdef)
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
    keys = keygen(key, 32)
    box = sbox(170)
    L = (msg >> 64) & 0xFFFFFFFFFFFFFFFF
    R = msg & 0xFFFFFFFFFFFFFFFF
    i = 0
    while i < 32:
        roundkey = keys[i]
        msb = (roundkey >> 64)
        lsb = roundkey & 0xFFFFFFFFFFFFFFFF
        tmp_R = (R ^ msb)
        smsg = 0
        for ii in range(8):
            tmp = (tmp_R >> (8 * (7 - ii))) & 0xFF
            smsg = (smsg << 8 ) + box[tmp]
        msg = smsg ^ lsb
        temp_L = R
        temp_R = L ^ msg
        L = temp_L
        R = temp_R
        i += 1
    msg = L << 64 | R
    return hex(msg)




