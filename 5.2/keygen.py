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
keys = keygen("deadbeef000000000000000badc0ffee", 32)
for i in range(len(keys)):
    print(f"{keys[i]:032X}")