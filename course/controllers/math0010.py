import logging
import os.path

from course.lib.base import *
from course import model
import paste.fileapp

log = logging.getLogger(__name__)

class Math0010Controller(BaseController):

    # Actions # --------------------------------------------------------
    def index(self):
        if 'login_id' in session:
            c.logged_in = True
            c.login_id = session['login_id']
        else:
            c.logged_in = False
        return render('/math0010/index.mako')
    
    def login(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'id' in request.params:
            id = request.params['id']
            session['login_id'] = id
            session.save()
        elif 'login_id' in session:
            id = session['login_id']
        else:
            c.error_msg = 'Invalid use of login script'
            log.info('Invalid login page access from %s'%(ip_address))
            return render('/error.mako')
        if model.course_db.isSudo(id):
           redirect_to(action='teacher_area') 
        else:
           redirect_to(action='student_area')

    def student_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Invalid access attempt of student area from'\
               ' %s using no login_id'%ip_address
            log.info(log_message)
            return render('/nologin.mako')
        students = model.course_db.get_student( 
            model.meta, session['login_id'])
        if students == []:
            c.error_msg = 'Invalid Student ID'
            log_message = 'Invalid access attempt of student area from'\
               ' %s using login_id %s'%(ip_address, session['login_id'])
            log.info(log_message)
            del session['login_id']  
            session.save()
            return render('/error.mako')
        else:
            c.student_info = students[0]
            c.student_marks = model.course_db.get_results( 
                model.meta, session['login_id'])
            c.message = h.get_msg(g.msg_dir) 
            c.files = h.get_fnames(g.downloads_dir)
            log_message = 'Student area for %s accessed from %s'%(
                students[0], ip_address)
            log.info(log_message)
            return render('/math0010/student.mako')

    def teacher_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Invalid access attempt of teacher area from'\
               ' %s using no login_id'%ip_address
            log.info(log_message)
            return render('/nologin.mako')
        if not model.course_db.isSudo(session['login_id']):
            c.error_msg = 'Invalid Login ID'
            log_message = 'Illegal access attempt of teacher area from'\
               ' %s using login_id %s'%(ip_address, session['login_id'])
            log.info(log_message)
            del session['login_id']  
            session.save()
            return render('/error.mako')
        log_message = 'Teacher area for %s accessed from %s'%(
            session['login_id'], ip_address)
        log.info(log_message)
        students = model.course_db.get_class_list(model.meta)
        c.all_marks = []
        for x in students:
            row = [x]
            row += model.course_db.get_results(model.meta, x.id)
            c.all_marks.append(row)
        return render('/math0010/teacher.mako')

    def logout(self):
        del session['login_id']  
        session.save()
        redirect_to(action='index')

    def downloads(self, id=''):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Invalid access attempt of download area from'\
               ' %s using no login_id'%ip_address
            log.info(log_message)
            return render('/nologin.mako')
        elif id == '':
            log_message = 'Invalid access attempt of download area from'\
                ' %s using login_id %s, no file requested'%(
                ip_address, session['login_id'])
            log.info(log_message)
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        elif id not in h.get_fnames(g.downloads_dir):
            log_message = 'Invalid access attempt of download area from'\
                ' %s using login_id %s, file %s requested, not '\
                'available'%(ip_address, session['login_id'], id)
            log.info(log_message)
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        else:
            return self._serve_file(os.path.join(g.downloads_dir, id))

    def _serve_file(self, path):
        """ Private Function
        Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        fapp = paste.fileapp.FileApp(path)
        return fapp(request.environ, self.start_response)
