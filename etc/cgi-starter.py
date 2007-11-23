#!/usr/bin/python

course_dir  = '/var/local/course'
egg_dir     = '%s/pylib' % course_dir
config_file = 'config:%s/production.ini' % course_dir

import sys
sys.path.insert(0, egg_dir)
from paste.deploy import loadapp
import  wsgiref.handlers

wsgi_app = loadapp(config_file)
wsgiref.handlers.CGIHandler().run(wsgi_app)
