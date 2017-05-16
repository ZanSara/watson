import os
from flask import Flask

import config as cf


app = Flask(__name__, static_folder = cf.APP_STATIC)


from app import views
