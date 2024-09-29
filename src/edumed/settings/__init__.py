# -*- coding: utf-8 -*-

from .paths import *
from .basic import *
from .apps import *
from .locale import *
from .search import *
from .auth import *
from .cache import *
from .context import *
from .logging import *
from .middleware import *
from .contrib import *
from .static import *
from .custom import *

# Load localsettings, if they exist
try:
    from edumed.localsettings import *
except ImportError:
    pass