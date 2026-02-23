from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import os
import urllib.parse
WEBSITE_URL = os.environ.get('WEBSITE_URL', 'http://localhost:5000')
print(WEBSITE_URL)
app = Flask(__name__)

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary for running in a container
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (may not be needed for headless mode)
    return chrome_options

class AdminBot:
    def __init__(self, base_url, flag):
        self.base_url = base_url
        self.flag = flag
        self.driver = webdriver.Chrome(options=set_chrome_options())
        self.lock = threading.Lock()
        
    def authenticate_and_visit_admin(self,userId):
        userId = urllib.parse.quote_plus(userId)
        
        self.driver.get(f"{self.base_url}/admin?userId={userId}")
        self.driver.add_cookie({
            'name': 'flag',
            'value': self.flag,
            'path': '/',
            'httpOnly': False 
        })
        print("Flag given to admin bot for userId {}".format(userId))

    def visit_profile(self,userId):
        with self.lock:
            self.driver.delete_all_cookies()
            self.authenticate_and_visit_admin(userId)
            self.driver.get(f"{self.base_url}/profile")
            self.driver.implicitly_wait(10)
            return self.driver.title, self.driver.page_source

    def close(self):
        self.driver.quit()

bot = AdminBot(WEBSITE_URL, os.environ.get('FLAG','flag{}'))
@app.route('/visit', methods=['POST'])
def visit():
    # Get the Admin Bot to visit the requested page
    userId = request.form.get('userId')
    if not userId:
        return jsonify({"error": "No userId provided"}), 400
    try:
        title, page_source = bot.visit_profile(userId)
        return jsonify({"title": title, "page_source": page_source}), 200
    except Exception as e:
        print(f"Error during Admin Bot visit: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run( port = 420, host = "0.0.0.0")
