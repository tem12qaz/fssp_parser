import traceback

from flask import Flask, request, render_template
from selenium import webdriver
import json
from main import get_base64_captcha, main_wrapper
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


@app.route("/parse_fssp", methods=['GET'])
def start_():
    return render_template('popup.html')


@app.route("/ugUV876gbvuybhBVfcjh9t6tv", methods=['POST'])
def start():
    global driver
    data = json.loads(request.data.decode('utf-8'))
    print(data)
    try:
        captcha = get_base64_captcha((data['fio'], data['date']))
    except:
        print(traceback.format_exc())
        return 'false'
    return captcha


@app.route("/jvvc67Vfcd6gy8vFJjv678v56f", methods=['POST'])
def process():
    global driver
    data = json.loads(request.data.decode('utf-8'))
    result = main_wrapper(data['captcha'])
    print(result)
    return result


if __name__ == '__main__':
    app.run()
