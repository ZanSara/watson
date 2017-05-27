import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '3'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }


# __file__ refers to this file
APP_ROOT = os.path.join( os.path.dirname(os.path.abspath(__file__)), "app" )
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_TEMPLATE = os.path.join(APP_ROOT, 'templates')

UPLOAD_FILE_PATH = "app/static/uploads/"
UPLOAD_WEB_PATH = "../static/uploads/"

FASHION_BLOGGER_FPATH = "app/static/dataset/collections/fashion_blogger/"
FASHION_BLOGGER_WPATH = "../static/dataset/collections/fashion_blogger/"

LOWER_BODY_FPATH = "app/static/dataset/collections/lower_body/"
LOWER_BODY_WPATH = "../static/dataset/collections/lower_body/"

UPPER_BODY_FPATH = "app/static/dataset/collections/upper_body/"
UPPER_BODY_WPATH = "../static/dataset/collections/upper_body/"

FULL_BODY_FPATH = "app/static/dataset/collections/full_body/"
FULL_BODY_WPATH = "../static/dataset/collections/full_body/"
