import os

## General Configuration
DEBUG = True
SERVER_NAME = 'dev.localhost:5000'

## E-Mail Configuration
SMTP_ADDRESS = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USE_ENCRYPTION = True
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_SENDER = ''

## Database Configuration
IDL_DB_URI =   'postgresql://<username>:<password>@<server>/<database>'
FORUM_DB_URI = 'postgresql://<username>:<password>@<server>/<database>'

## URL Configuration
STATIC_URL = '/static'
IMAGES_URL = '/'.join((STATIC_URL, 'images'))
MAP_SCREENSHOTS_URL = '/'.join((STATIC_URL, 'map_screenshots'))
DEMO_FILES_URL = 'http://s3.amazonaws.com/idldemos'
LOG_FILES_URL = '/'.join((STATIC_URL, 'logs'))
LOGOS_URL = '/'.join((STATIC_URL, 'images', 'logos'))
NO_SCREENSHOT_URL = '/'.join((MAP_SCREENSHOTS_URL, 'no_screenshot.gif'))
LOGO_URL = '/'.join((IMAGES_URL, 'newlogo43.png'))
FORUMS_URL = 'http://forums.intldoomleague.org'
WIKI_URL = 'http://wiki.intldoomleague.org'

## Path Configuration
HOME = 'E:\\Code\\idl.org'
DEMO_FILE_PATH = os.path.join(HOME, 'idl', 'public', 'uploads')
LOG_FILE_PATH = os.path.join(HOME, 'idl', 'public', 'logs')

## Template Configuration
MAKO_DIR = os.path.join(HOME, 'idl', 'templates')
MAKO_CACHEDIR = os.path.join(HOME, 'idl', 'mako_cache')

## Secret Stuff
ADMIN_PASSWORD = 'wookie'
ADMINS = [ 'Ladna' ]
S3_ACCESS_KEY = 'XXX'
S3_PRIVATE_KEY = 'XXX'

## Cookie Stuff
SECRET_KEY = 'XXX'
SESSION_COOKIE_NAME = 'idl'
# SESSION_COOKIE_DOMAIN = 'dev.localhost'
# SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = 31536000 # A year's worth of seconds

## Cache Stuff; disabled if Kyoto Tycoon is not running
KYOTO_TYCOON_KEY_PREFIX = 'idl'
KYOTO_TYCOON_ADDRESS = 'localhost'
KYOTO_TYCOON_PORT = 1978
KYOTO_TYCOON_TIMEOUT = 30
SQLITE_DB_FILE = os.path.join(HOME, 'idl.sqlite')

## Miscellaneous
NEWS_FORUM_BOARD_ID = 18

