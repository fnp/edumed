# -*- coding: utf-8 -*-
import os

CAS_SERVER_URL = os.environ.get('CAS_SERVER_URL')
CAS_VERSION = '3'

HONEYPOT_FIELD_NAME='miut'

SPONSORS_THUMB_WIDTH = 100
SPONSORS_THUMB_HEIGHT = 56

PYBB_TEMPLATE = "base_forum.html"
PYBB_SMILES = {}
PYBB_ENABLE_ANONYMOUS_POST = False

PYBB_DEFAULT_TITLE = u'Forum'
PYBB_DEFAULT_TIME_ZONE = 1
PYBB_PERMISSION_HANDLER = 'edumed.forum.ForumPermissionHandler'

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_CONVERT = 'convert -density 300 -background white -alpha off'
