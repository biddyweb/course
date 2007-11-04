from pylons import config
import course_db

engine = config['pylons.g'].sa_engine
meta = course_db.meta_auto_load(engine)
