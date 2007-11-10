INSTALL_DIR		= /var/local/course

LIB_DIR			= /usr/local/lib/python2.5/site-packages
SCRIPTS_DIR		= /usr/local/bin
EGGINS_LOG		= /tmp/course-eggins.log

DB_DIR			= ${INSTALL_DIR}/db
DOWNLOAD_DIR	= ${INSTALL_DIR}/downloads
MESSAGE_DIR		= ${INSTALL_DIR}/messages
RUN_DIR			= ${INSTALL_DIR}/run

usage:
	@echo 
	@echo Main targets: install, clean
	@echo
	@echo Subtargets: egg-install egg-info mk-dirs etc-install copy-files
	@echo

install: mk-dirs etc-install copy-files egg-install

test-install: mk-dirs ${INSTALL_DIR}/wsgi-starter.py

egg-install:
	easy_install -d ${LIB_DIR} -s ${SCRIPTS_DIR} --record ${EGGINS_LOG} .
	chmod -R a+rX ${LIB_DIR} ${SCRIPTS_DIR}/course-util

egg-info:
	python setup.py egg_info

mk-dirs:
	mkdir -p ${DB_DIR}
	mkdir -p ${DOWNLOAD_DIR}
	mkdir -p ${MESSAGE_DIR}
	rm -fr ${RUN_DIR}
	mkdir -p ${RUN_DIR}
	chmod -R a+rX ${INSTALL_DIR}
	chown www-data:www-data ${RUN_DIR}


etc-install: ${INSTALL_DIR}/production.ini \
             ${INSTALL_DIR}/wsgi-starter.py
${INSTALL_DIR}/production.ini: etc/production.ini
	install -m 644 etc/production.ini ${INSTALL_DIR}
${INSTALL_DIR}/wsgi-starter.py: etc/wsgi-starter.py
	install -m 644 etc/wsgi-starter.py ${INSTALL_DIR}

# coud we have these inside the egg?
copy-files:
	cp -a public ${INSTALL_DIR}
	chmod -R a+rX ${INSTALL_DIR}/public
	cp -a templates ${INSTALL_DIR}
	chmod -R a+rX ${INSTALL_DIR}/templates

clean:
	rm -fr build
	rm -fr temp
	rm -fr course.egg-info/

distclean: clean
