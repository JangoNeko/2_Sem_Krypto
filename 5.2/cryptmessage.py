import random
from random import randbytes
message = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible."
def cypher(message):
    msg = message
    length = 16 - len(msg) % 16
    msg += bytes([length]) * length
    plaintext = msg
    print(plaintext)
    return plaintext
cypher(message)