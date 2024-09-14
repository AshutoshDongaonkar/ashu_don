# myapi.wsgi
import sys
import logging

sys.path.insert(0, '/var/www/flaskMSPS')
sys.path.insert(0, '/home/ashu/testenv/lib/python3.11/site-packages/')

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from app import app as application
