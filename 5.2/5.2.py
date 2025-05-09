def sbox(s):                                                                     # generierung der S-Box als Liste
    s = [s]
    i = 1
    while i < 256:
        s.insert(i, (37 * s[i-1] + 9) % 256)
        i += 1
#---------------------------------------------------------------------------------- Assertions
    assert(s[0] == 170)
    assert(s[1] == 155)
    assert(s[2] == 112)
    assert(s[123] == 33)
    assert(s[255] == 205)
    return s

def keygen(key, rounds):                                                          # Generierung aller keys, die im Feistel-Netzwerk benötigt werden
    if isinstance(key, str):
        key = int(key, 16)
    keys = [((((key << ((7 * 0) % 128)) | (key >> (128 - ((7 * 0) % 128))))& ((1<<128)-1)) ^ 0xabcdef)] # Hier wird der erste Key berechnet und als Index 0 in der Ausgabeliste gespeichert
    i = 1
    while i < rounds:                                                                                   # Berechnung der restlichen 32 Keys
        keys.append(((((keys[i-1] << ((7 * i) % 128)) | (keys[i - 1] >> (128 - ((7 * i) % 128))))& ((1<<128)-1)) ^ 0xabcdef))
        i += 1
#----------------------------------------------------------------------------------- Assertions
    assert(f"{keys[0]:032x}" == "deadbeef000000000000000bad6b3201")
    assert(f"{keys[1]:032x}" == "56df778000000000000005d6b532cd00")
    assert(f"{keys[2]:032x}" == "dde00000000000000175ad4cb3ebd858")
    assert(f"{keys[31]:032x}" == "770feb4b3180dc3bc09870bd38e2cb5f")
    return keys


def schiffy(key, msg):                                                               # Schiffre
    if isinstance(msg, str):
        msg = int(msg, 16)                                                           # Umwandeln des Plaintext-Strings
    keys = keygen(key, 32)                                                    # Generierung der Schlüsselliste
    box = sbox(170)                                                                  # Generierung der S-Box
    L = (msg >> 64) & 0xFFFFFFFFFFFFFFFF                                             # Aufteilen des Plaintexts
    R = msg & 0xFFFFFFFFFFFFFFFF
    i = 0
    while i < 32:                                                                    # Rundenfunktion
        roundkey = keys[i]
        msb = (roundkey >> 64)                                                       # Aufteilen des Rundenkeys
        lsb = roundkey & 0xFFFFFFFFFFFFFFFF
        tmp_R = (R ^ msb)                                                            # Erstes XOR vor der S-Box
        smsg = 0
        for ii in range(8):                                                          # Aplizieren der S-Box
            tmp = (tmp_R >> (8 * (7 - ii))) & 0xFF
            smsg = (smsg << 8 ) + box[tmp]
        msg = smsg ^ lsb                                                             # Zweites XOR nach der S-Box
        temp_L = R                                                                   # Berechnung der Eingaben für die nächste Runde
        temp_R = L ^ msg
        L = temp_L
        R = temp_R
#------------------------------------------------------------------------------------ Assertions des Feistel-Netzwerks
        if i == 0:
            assert f"{msg:016x}" == "94dfb49607c198ab"

        if i == 1:
            assert f"{msg:016x}" == "b0aa7cca50e95fb1"

        if i == 2:
            assert f"{msg:016x}" == "1e9d6324e9783573"

        if i == 3:
            assert f"{msg:016x}" == "01a6283b0f33c8f0"

        if i == 29:
            assert f"{msg:016x}" == "f7ffea032144154a"

        if i == 30:
            assert f"{msg:016x}" == "7fac6b4146d4f4c6"

        if i == 31:
            assert f"{msg:016x}" == "2a66d3471f7cb499"
#------------------------------------------------------------------------------------ Ende der Assertions
        i += 1
    msg = L << 64 | R                                                                # Merge der Ausgabe nach dem Feistel-Netzwerks
    return f"{msg:016x}"
#------------------------------------------------------------------------------------ Assertion der schiffy-Funktion
assert schiffy("deadbeef000000000000000badc0ffee", "00000000000000000000000000000000") == "b743f2fb342c51bfab950797083f61e9"