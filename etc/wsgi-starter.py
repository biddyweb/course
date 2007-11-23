# wsgi applicationb starter for mod_wsgi

course_dir  = '/var/local/course'
egg_dir     = '%s/pylib' % course_dir
config_file = 'config:%s/production.ini' % course_dir

import sys
sys.path.insert(0, egg_dir)
from paste.deploy import loadapp

application = loadapp(config_file)
