#!/bin/bash

INSTALL_DIR=/var/local/teaching/math0010
DB_PATH=/var/tmp
DB_FILE=math0010.sqlite

usage:
	@echo 
	@echo Possible targets: install, uninstall, purge, clean, distclean
	@echo

install:
	python setup.py bdist_egg
	easy_install --record installed-files.log `python setup.py --course-dist-egg-path` 
	mkdir -p ${INSTALL_DIR}/db
	mkdir -p ${INSTALL_DIR}/private/messages
	mkdir -p ${INSTALL_DIR}/private/downloads
	cp -a  ${DB_PATH}/${DB_FILE} ${INSTALL_DIR}/db/${DB_FILE}
	cp -a  production.ini ${INSTALL_DIR}/
	cp -ar public ${INSTALL_DIR}/public
	cp -ar templates ${INSTALL_DIR}/templates

uninstall:
	easy_install -m `python setup.py --course-dist-egg-path` 
	xargs <installed-files.log  rm -f
	rm -fr `python setup.py --course-egg-path`

purge: uninstall
	rm -fr ${INSTALL_DIR}

clean:
	rm -fr dist

distclean: clean
	rm -f installed-files.log
