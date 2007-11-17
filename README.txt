Course Web-Application
======================

You are currently in the top level directory of the course package. This
package contains the following directories:

    course/     - A Python Module that requires Pylons, that consists of
                  a web interface to the course system.
    util/       - Utilities ofr manipulating the course system and
                  underlying database.

Installation and Setup
======================

Bellow is an outline of a basic pylons installation. For more detailed
installation instructions and possible methods of deploying course read
docs/INSTALL.

Install ``course`` using easy_install::

    easy_install course

Make a config file as follows::

    paster make-config course config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.

