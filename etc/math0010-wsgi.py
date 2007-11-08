# wsgi applicationb starter for "course"

course_dir  = '/var/local/course'

from paste.deploy import loadapp

application = loadapp('config:%s/production.ini' % course_dir)
