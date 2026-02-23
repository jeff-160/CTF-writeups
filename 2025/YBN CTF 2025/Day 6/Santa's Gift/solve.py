from bs4 import BeautifulSoup
import requests
import re

base = 'https://ybnctf.ybn.sg/'

res = requests.get(base)

soup = BeautifulSoup(res.text, 'html.parser')
urls = set() 

for tag in soup.find_all(['a', 'link', 'script', 'img']):
    for attr in ['href', 'src']:
        url = tag.get(attr)

        if not url:
            continue

        if url.startswith("/"):
            url = base + url

        urls.add(url)

for url in urls:
    print("Searching:", url)
    res = requests.get(url)
    
    if "ybn25" in res.text.lower():
        print("Flag:", re.findall(r'(YBN25\{.+?\})', res.text)[0])
        exit()