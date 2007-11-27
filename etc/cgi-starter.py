#!/usr/bin/python

course_dir  = '/var/local/course'
egg_dir     = '%s/pylib' % course_dir
config_file = '%s/production.ini' % course_dir

import sys
sys.path.insert(0, egg_dir)
from paste.deploy import loadapp
from paste.script.util.logging_config import fileConfig
import  wsgiref.handlers

fileConfig(config_file) 
wsgi_app = loadapp('config:%s'%config_file)
wsgiref.handlers.CGIHandler().run(wsgi_app)
