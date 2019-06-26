from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import gettext
from importlib import import_module
from constants import ConfigKeys, DEFAULT_LOCALE, DEFAULT_CHARSET

load_dotenv()

app = Flask(__name__)
CORS(app)

DefaultLocale = os.getenv(ConfigKeys.DefaultLocale) or DEFAULT_LOCALE
DefaultCharset = os.getenv(ConfigKeys.DefaultCharset) or DEFAULT_CHARSET

app.config.update({key: int(os.getenv(key)) if os.getenv(key).isdecimal() else os.getenv(key) for key in os.environ})

fa = gettext.translation(DefaultLocale.replace('-', '_'), localedir='locale', languages=['fa'])
fa.install()


for f, g, h in os.walk(os.getcwd()):
    if 'handler.py' in h:
        import_module('.handler', os.path.relpath(f, os.getcwd()).replace('/', '.'))

module = import_module('infrastructure.repository')
module.create_schema()
