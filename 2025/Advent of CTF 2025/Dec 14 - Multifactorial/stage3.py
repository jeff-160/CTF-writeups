import base64
import hashlib

def get_handle(name):
    name_bytes = name.encode('utf-8')
    hash_bytes = hashlib.sha256(name_bytes).digest()[:16]
    
    b64 = base64.urlsafe_b64encode(hash_bytes).decode('ascii')
    return b64.rstrip("=")

payload = f'localStorage.np_userHandle = "{get_handle('santa')}"'
print(payload)