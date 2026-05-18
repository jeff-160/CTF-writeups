#!/usr/bin/env python3
import os
import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By

def start():
    options = webdriver.ChromeOptions()
    for _ in [
        'headless',
        'window-size=1920x1080',
        'disable-gpu',
        'no-sandbox',
        'disable-dev-shm-usage',
    ]:
        options.add_argument(_)
    driver = webdriver.Chrome('/chromedriver', options=options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    return driver

def login(pw):
    time.sleep(5)
    driver.get('http://127.0.0.1:8000/')
    driver.implicitly_wait(10)
    driver.find_element(By.NAME, 'username').send_keys('admin')
    driver.find_element(By.NAME, 'password').send_keys(pw.decode())

    driver.find_element(By.XPATH, '//*[contains(text(), "sign in")]').click()

def get_applications():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user=os.environ['MYSQL_USER'],
                         passwd=os.environ['MYSQL_PASSWORD'],
                         db='dream_lectures_db',
                         charset='utf8')
    cursor = db.cursor()

    ret = []
    try:
        query = 'SELECT idx, lecture_idx, lecture_name, applicant_name ' \
                'FROM applications WHERE is_checked = false'
        cursor.execute(query)
        ret = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

    return ret

def read_applications():
    applications = get_applications()
    for application in applications:
        application_id = application[0]
        driver.get('http://127.0.0.1:8000/applications/{0}'.format(application_id))
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(10)

driver = start()
