import requests
import os

url = "https://bad-apple.tamuctf.com/"

dir = 'browse/admin/1be0aebf801ff68a176f188987c3eae9-flag'

res = requests.get(f'{url}/{dir}')

os.makedirs('frames')

for i in range(1, 155 + 1):
    path = f"frame_{i:0>4}.png"
    
    res = requests.get(f"{url}/{dir}/{path}")
    
    with open(f'frames/{path}', "wb") as f:
        f.write(res.content)