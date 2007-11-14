try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os, sys
import course

_course_version = '0.1.2'

# NICE HACK by P. Dobcsanyi
def course_egg_path():
    x = 'course-%s'%_course_version
    for p in sys.path:
        if x in p: return p
    return ''

def course_dist_egg():
    x = 'course-%s'%_course_version
    for p in os.listdir('dist'):
        if x in p: return 'dist/'+p
    return ''

if len(sys.argv) > 1 and sys.argv[1] == '--course-egg-path':
    print course_egg_path()
    raise SystemExit(0)

if len(sys.argv) > 1 and sys.argv[1] == '--course-dist-egg-path':
    print course_dist_egg()
    raise SystemExit(0)

setup(
    name='course',
    version=_course_version,
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=["Pylons>=0.9.6.1"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={
    #   'course': ['i18n/*/LC_MESSAGES/*.mo']
        'course': ['public/graphics/*', 
                   'templates/*.mako', 'templates/*/*.mako'], 
    },
    #message_extractors = {'course': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = course.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
