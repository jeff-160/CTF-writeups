from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from flask import Flask, request
from time import sleep
app = Flask(__name__)

flag = "DH{fake_flag}"

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        file = request.form['filename']
        result = read_url(f'http://web:8000/load-file?filename={file}')
        message = "report success" if result else "report failed ..."
        return message
    else:
        return "hi im bot"


def read_url(url):
    global flag
    driver = None
    print('here')
    try:
        service = Service(executable_path="/chromedriver-linux64/chromedriver")
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get("http://web:8000/")
        driver.add_cookie({'name':'flag','value':flag, 'domain':'web'})
        driver.get(url)
        sleep(1)
        driver.quit()
    except Exception as e:
        return False
    return True

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9999,debug=True)