from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sys
import base64

if len(sys.argv) < 2:
    exit(-1)

if len(sys.argv[1]) == 0:
    exit(-1)

path = base64.b64decode(sys.argv[1]).decode('latin-1')

try:
    FLAG = open('/flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

def read_url(url, cookie={'name': 'name', 'value': 'value'}):
    cookie.update({'domain':'127.0.0.1'})
    try:
        service = Service(executable_path="/chromedriver")
        options = webdriver.ChromeOptions()
        for _ in ['headless', 'window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage']:
            options.add_argument(_)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get('http://127.0.0.1/')
        driver.add_cookie(cookie)
        driver.get(url)

    except Exception as e:
        driver.quit()
        return False
    driver.quit()
    return True

def check_xss(path, cookie={'name': 'name', 'value': 'value'}):
    url = f'http://127.0.0.1/{path}'
    return read_url(url, cookie)

if not check_xss(path, {'name': 'flag', 'value': FLAG.strip()}):
    print('<script>alert("wrong??");history.go(-1);</script>')
else:
    print('<script>alert("good");history.go(-1);</script>')
