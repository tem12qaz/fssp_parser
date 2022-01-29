from flask import Flask, request
from selenium import webdriver

from main import get_base64_captcha, main

app = Flask(__name__)


@app.route("/ugUV876gbvuybhBVfcjh9t6tv")
def start():
    global driver
    data = request.data
    return get_base64_captcha(data)


@app.route("/jvvc67Vfcd6gy8vFJjv678v56f")
def process():
    global driver
    data = request.data
    try:
        resp = main(data)
        if resp:
            return resp
    except:
        pass


if __name__ == '__main__':
    app.run()
