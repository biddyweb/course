INSTALL_DIR		= /var/local/course

LIB_DIR			= $(INSTALL_DIR)/pylib
SCRIPTS_DIR		= $(INSTALL_DIR)/bin
EGGINS_LOG		= /tmp/course-eggins.log

DB_DIR			= ${INSTALL_DIR}/db
DOWNLOAD_DIR	= ${INSTALL_DIR}/downloads
MESSAGE_DIR		= ${INSTALL_DIR}/messages
RUN_DIR			= ${INSTALL_DIR}/run

# UTIL_SCRIPT_DIR = /usr/local/bin
UTIL_SCRIPT_DIR = ${HOME}/bin/script

# for mod_wsgi running as course:course
COURSE_USER		= course
COURSE_GROUP	= course

# cgi running out of the webserver
WEBSERVER_USER		= www-data
WEBSERVER_GROUP		= www-data

usage:
	@echo 
	@echo Main targets: install, clean, util
	@echo
	@echo \"install\" installs the course-egg, init file
	@echo and deployment method dependent files
	@echo
	@echo \"utils\" install course-util
	@echo


# install: egg init mod_wsgi
install: egg init cgi
	chmod -R a+rX ${INSTALL_DIR}

egg: mk-dirs
	export PYTHONPATH=${LIB_DIR}; easy_install -d ${LIB_DIR} \
	-s ${SCRIPTS_DIR} \
	--record ${EGGINS_LOG} .

egg-info:
	python setup.py egg_info

mk-dirs:
	mkdir -p ${LIB_DIR}
	mkdir -p ${SCRIPTS_DIR}
	mkdir -p ${DB_DIR}
	mkdir -p ${DOWNLOAD_DIR}
	mkdir -p ${MESSAGE_DIR}
	rm -fr ${RUN_DIR}
	mkdir -p ${RUN_DIR}

# init
#
init: ${INSTALL_DIR}/production.ini

${INSTALL_DIR}/production.ini: etc/production.ini
	install -m 644 etc/production.ini ${INSTALL_DIR}

# CGI
#
cgi: ${INSTALL_DIR}/bin/cgi-starter.py
	chown -R ${WEBSERVER_USER}:${WEBSERVER_GROUP} ${RUN_DIR}

${INSTALL_DIR}/bin/cgi-starter.py: etc/cgi-starter.py
	install etc/cgi-starter.py ${INSTALL_DIR}/bin

# mod_wsgi
#
mod_wsgi: ${INSTALL_DIR}/wsgi-starter.py
	chown -R ${COURSE_USER}:${COURSE_GROUP} ${RUN_DIR}

${INSTALL_DIR}/wsgi-starter.py: etc/wsgi-starter.py
	install -m 644 etc/wsgi-starter.py ${INSTALL_DIR}

# course-util
#
util: ${UTIL_SCRIPT_DIR}/course-util 
${UTIL_SCRIPT_DIR}/course-util: utils/course-util 
	install -m 755 utils/course-util ${UTIL_SCRIPT_DIR}/course-util 

clean:
	rm -fr build
	rm -fr temp
	rm -fr course.egg-info/

distclean: clean
