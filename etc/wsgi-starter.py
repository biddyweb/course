# wsgi applicationb starter for "course"

# production
course_dir  = '/var/local/course'
course_lib_dir  = '%s/pylib'%course_dir

import os, site; site.addsitedir(course_lib_dir)
from paste.deploy import loadapp

application = loadapp('config:%s/production.ini' % course_dir)
