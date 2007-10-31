"""Pylons environment configuration"""
import os

from pylons import config

import course.lib.app_globals as app_globals
import course.lib.helpers
from course.config.routing import make_map
from sqlalchemy import engine_from_config

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(app_conf['static_files']),
                 templates=[os.path.join(app_conf['mako_templates'])])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='course',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.g'].sa_engine = \
        engine_from_config(config, 'sqlalchemy.')
    config['pylons.h'] = course.lib.helpers
    
    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
