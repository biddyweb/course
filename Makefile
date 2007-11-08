INSTALL_DIR=/var/local/course
DB_PATH=/var/tmp
DB_FILE=math0010.sqlite
LIB_DIR=/usr/local/lib/python2.5/site-packages
SCRIPTS_DIR=/usr/local/bin

usage:
	@echo 
	@echo Possible targets: install, uninstall, purge, clean, distclean
	@echo

install:
	python setup.py bdist_egg
	easy_install -d ${LIB_DIR} -s ${SCRIPTS_DIR} --record installed-files.log `python setup.py --course-dist-egg-path` 
	mkdir -p ${INSTALL_DIR}/db
	mkdir -p ${INSTALL_DIR}/private/messages
	mkdir -p ${INSTALL_DIR}/private/downloads
	mkdir -p ${INSTALL_DIR}/data/paster
#	cp -a  ${DB_PATH}/${DB_FILE} ${INSTALL_DIR}/db/${DB_FILE}
	cp -a etc/production.ini ${INSTALL_DIR}/
	cp -a public ${INSTALL_DIR}/public
	cp -a templates ${INSTALL_DIR}/templates

uninstall: installed-files.log
	python setup.py --course-egg-path >tmp.path_to_egg
	echo $$TMP_ENV_VAR 
	python setup.py --course-egg-path
	easy_install -m `python setup.py --course-dist-egg-path` 
	xargs <installed-files.log  rm -f
	xargs <tmp.path_to_egg  rm -fr
	rm -f tmp.path_to_egg

purge: uninstall
	rm -fr ${INSTALL_DIR}

clean:
	rm -fr dist

distclean: clean
	rm -f installed-files.log
