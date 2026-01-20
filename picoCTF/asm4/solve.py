s = "picoCTF_e53f9"
var = 0x267

for i in range(1, len(s)-1):
    var += ord(s[i+1]) - ord(s[i-1])

print("Flag:", hex(var & 0xffffffff))