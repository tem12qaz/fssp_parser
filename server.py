from flask import Flask, request
from selenium import webdriver

from main import get_base64_captcha, main
from logging.config import dictConfig
# from config_logger import config
#
#
# logging.config.dictConfig(config)
# logger = logging.getLogger('file_logger')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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
