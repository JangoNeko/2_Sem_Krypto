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
        msg = msg.encode("utf-8")
    msg = int.from_bytes(msg, "big")
    key = keygen("deadbeef000000000000000badc0ffee", 32)
    box = sbox(170)
    i = 0
    while i < 32:
        roundkey = key[i]
        msb = (roundkey >> 64) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        lsb = roundkey & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        msg = (msg ^ msb) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        chunk = msg.to_bytes(16, byteorder= 'big')
        smsg = bytes([box[b] for b in chunk])
        msg = int.from_bytes(smsg, byteorder = 'big' ) ^ lsb
        i += 1
    return hex(msg)


print(schiffy("deadbeef000000000000000badc0ffee", "00000000000000000000000000000000"))
