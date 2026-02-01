import struct

code = open("code.pascal","rb").read()
ip = 0

while True:
    op = code[ip]
    if op == 0:
        print(f"{ip:04x}: HALT")
        break

    if op in [1,2,3,4]:
        addr = struct.unpack("<I", code[ip+1:ip+5])[0]
        imm = code[ip+5]
        print(f"{ip:04x}: OP{op} mem[{addr}] imm={imm}")
        ip += 6

    elif op == 5:
        addr = struct.unpack("<I", code[ip+1:ip+5])[0]
        print(f"{ip:04x}: INPUT mem[{addr}]")
        ip += 5

    elif op == 6:
        addr = struct.unpack("<I", code[ip+1:ip+5])[0]
        off = code[ip+5]
        print(f"{ip:04x}: JZ mem[{addr}] +{off}")
        ip += 6

    else:
        print("Unknown opcode", op)
        break