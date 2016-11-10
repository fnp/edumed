# -*- coding: utf-8 -*-
from fnpdjango.deploy import *

env.project_name = 'edumed'
env.hosts = ['giewont.icm.edu.pl']
env.user = 'edumed'
env.app_path = '/srv/olimpiadacyfrowa.pl'
env.services = [
    Supervisord('olimpiada'),
]
