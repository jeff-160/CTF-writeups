import struct

def qword(x):
    return struct.pack("<q", x)

arr1 = (
    qword(636393207781367565) +
    qword(6815415887468846914) +
    qword(-5383483106719277089) +
    qword(5028962369058608476) +
    qword(-8412616730741848136) +
    qword(-4331540819873830742)
)

arr2 = (
    qword(7460122710030804078) +
    qword(2155843037158521917) +
    qword(-1280093367654730776) +
    qword(4320087681156377702) +
    qword(-2298767691485445932) +
    qword(-9026541190072180319)
)

arr1 = arr1.split(b"\x00")[0]
arr2 = arr2[:len(arr1)]

flag = bytearray()
for i in range(len(arr1)):
    c = arr1[i] ^ arr2[i] ^ i ^ 19
    flag.append(c)

print("Flag:", flag.decode())