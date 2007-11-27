# wsgi application starter for "course"

# production
course_dir  = '/var/local/course'
course_lib_dir  = '%s/pylib' % course_dir
config_file = '%s/production.ini' % course_dir

import sys
sys.path.insert(0, course_lib_dir)
from paste.script.util.logging_config import fileConfig
from paste.deploy import loadapp

fileConfig(config_file) 
application = loadapp('config:%s' % config_file)
