from flask import Flask, request
from selenium import webdriver

from main import get_base64_captcha, main

app = Flask(__name__)


@app.route("/ugUV876gbvuybhBVfcjh9t6tv")
def start():
    global driver
    data = request.data
    return get_base64_captcha(driver, data)


@app.route("/jvvc67Vfcd6gy8vFJjv678v56f")
def process():
    global driver
    data = request.data
    try:
        resp = main(driver, data)
        if resp:
            return resp
    except:
        driver.get(url)
        return False
    else:
        driver.get(url)
        return True


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    url = 'https://fssp.gov.ru/iss/iP'
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    app.run()
