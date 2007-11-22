"""The application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.msg_dir = config['course.msg_dir']
        self.downloads_dir = config['course.downloads_dir']
        self.polynom = config['course.polynom_app']
        self.name = config['course.name']
