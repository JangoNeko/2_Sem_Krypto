def q(b):
    return (b ^ (b << 17 | b >> 15) & 0xffffffff)               #linksrotation, bytes die vorne wegfallen werden hinten nachgeschoben
                                                                #beim xor wird darauf geachtet, dass b nicht größer als 32Bit wird

def h(data):
    state = 0x524f464c                                           # ROFL
    if isinstance(data, str):
        data = data.encode('utf-8')

    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]                                   # aufteilen in 32Bit-Blöcke

        if len(chunk) < 4:
             chunk = chunk.ljust(4, b'\xff')      # wenn block zu klein, mit ff auffüllen

        p = int.from_bytes(chunk, byteorder='big')
        state = q(state ^ p)                                 # finally, hashen
    return q(state).to_bytes(4, byteorder='big')

out1 = h("")
out2 = h("A")
out3 = h("AB")
out4 = h("ABC")
out5 = h("ABCD")
out6 = h("ABCDE")
print(hex(q(0x524f464c)))
print(hex(q(q(0x524f464c))))
print(hex(q(q(q(0x524f464c)))))
print(f"{out1.hex()}\n{out2.hex()}\n{out3.hex()}\n{out4.hex()}\n{out5.hex()}\n{out6.hex()}")

# Task 2
print("PART 2")
print(hex(int('11001100110100011101011111111111', 2)))

def h_ext(data):
    state = 0xccd1d7ff                                           # previous state von 'abcd'
    if isinstance(data, str):
        data = data.encode('utf-8')

    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]                                   # aufteilen in 32Bit-Blöcke

        if len(chunk) < 4:
             chunk = chunk.ljust(4, b'\xff')      # wenn block zu klein, mit ff auffüllen

        p = int.from_bytes(chunk, byteorder='big')
        state = q(state ^ p)                                 # finally, hashen
    return q(state).to_bytes(4, byteorder='big')

forge0 = h_ext("ef")
forge1 = h_ext("efghijk")
print(f"{forge0.hex()}\n{forge1.hex()}")