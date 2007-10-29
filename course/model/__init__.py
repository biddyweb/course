from pylons import config
from utils import course_cgi

engine = config['pylons.g'].sa_engine
meta = course_cgi.meta_auto_load(engine)

