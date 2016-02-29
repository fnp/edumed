from fnpdjango.deploy import *

env.project_name = 'edumed'
env.hosts = ['giewont.icm.edu.pl']
env.user = 'edumed'
env.app_path = '/srv/edukacjamedialna.edu.pl'
env.services = [
    Supervisord('edumed'),
]
