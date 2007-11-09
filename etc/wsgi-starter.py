# wsgi applicationb starter for "course"

# production
course_dir  = '/var/local/course'
config      = '%s/etc/production.ini' % course_dir

from paste.deploy import loadapp

application = loadapp('config:%s' % config)
