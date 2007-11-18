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

EXEC_USER		= course
EXEC_GROUP		= course

usage:
	@echo 
	@echo Main targets: install, clean
	@echo
	@echo Subtargets: egg-install egg-info mk-dirs etc-install util-install copy-files
	@echo

install: mk-dirs etc-install egg-install util-install chg-perm

test-install: mk-dirs ${INSTALL_DIR}/wsgi-starter.py

egg-install:
	export PYTHONPATH=${LIB_DIR}; easy_install -d ${LIB_DIR} -s ${SCRIPTS_DIR} --record ${EGGINS_LOG} .

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

etc-install: ${INSTALL_DIR}/production.ini \
             ${INSTALL_DIR}/wsgi-starter.py
${INSTALL_DIR}/production.ini: etc/production.ini
	install -m 644 etc/production.ini ${INSTALL_DIR}
${INSTALL_DIR}/wsgi-starter.py: etc/wsgi-starter.py
	install -m 644 etc/wsgi-starter.py ${INSTALL_DIR}

util-install: ${UTIL_SCRIPT_DIR}/course-util 
${UTIL_SCRIPT_DIR}/course-util: utils/course-util 
	install -m 755 utils/course-util ${UTIL_SCRIPT_DIR}/course-util 

chg-perm:
	chmod -R a+rX ${INSTALL_DIR}
	chown -R ${EXEC_USER}:${EXEC_GROUP} ${RUN_DIR}

clean:
	rm -fr build
	rm -fr temp
	rm -fr course.egg-info/

distclean: clean
