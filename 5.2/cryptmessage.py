import os


def sbox(s):
    s = [s]
    i = 1
    while i < 256:
        s.insert(i, (37 * s[i-1] + 9) % 256)
        i += 1
    return s

def keygen(key, rounds):
    if isinstance(key, str):
        key = int(key, 16)
    keys = [((((key << ((7 * 0) % 128)) | (key >> (128 - ((7 * 0) % 128))))& ((1<<128)-1)) ^ 0xabcdef)]
    i = 1
    while i < rounds:
        keys.append(((((keys[i-1] << ((7 * i) % 128)) | (keys[i - 1] >> (128 - ((7 * i) % 128))))& ((1<<128)-1)) ^ 0xabcdef))
        i += 1
    return keys


def schiffy(key, msg):
    if isinstance(msg, str):
        msg = int(msg, 16)
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
    return f"{msg:032x}"

def schiffy_cbc_enc(key, msg):
    pad_length = 16 -(len(msg) % 16)                                    # Padding, damit msg % 16 = 0
    msg_padded = msg + bytes([pad_length]*pad_length)
    chunk = [msg_padded[i:i+16] for i in range(0, len(msg_padded), 16)] # Aufteilen der msg in 16b chunks, fürs xor
    iv = os.urandom(16)                                                 # IV randomisiert übers OS
    print(f"{iv.hex()}")                                                # Für doku
    ciphertext_chunks = []
    prev = iv                                                           # bringt iv in schleife

    for i in chunk:                                                     # cbc-modus
        chunk_xored = int.from_bytes(i, 'big') ^ int.from_bytes(prev, 'big') # xored chunks
        cipher = schiffy(key, f"{chunk_xored:032x}")                                      # verschlüsseln mit schiffy
        cipher_bytes = bytes.fromhex(cipher)                                                   # umwandeln in bit
        ciphertext_chunks.append(cipher_bytes)                                                 # zusammenkleben der chunks
        prev = cipher_bytes                                                                    # nächster schlüssel fürs cbc-xor

    return iv + b"".join(ciphertext_chunks)                                                    # ankleben des schiffrats an den IV

key = "08150000000000000000000000004711"
messages = b"According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible."
with open("nik.txt", "rb") as f:
    message = f.read()
cypher = schiffy_cbc_enc(key, message)
with open("nik.bin", "wb") as f:                                                        # direkt in file schreiben weil ich bin faul
    f.write(cypher)