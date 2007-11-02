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
        log_flag = True
        if 'id' in request.params and request.params['id'] != '':
            id = request.params['id']
        elif 'login_id' in session:
            id = session['login_id']
            log_flag = False
        else:
            c.error_msg = 'Go to the main page to login.'
            log.info(
                'Login attempted without login info.'
                ,extra = {'clientip': ip_address}
            )
            return render('/error.mako')
        

        students = model.course_db.get_student(model.meta, id)
        if students == []:
            c.error_msg = 'No Student with ID=%s'%id
            log_message = 'Student ID %s not found in DB'%id
            log.info(log_message, extra={'clientip': ip_address})
            del session['login_id']  
            session.save()
            return render('/error.mako')
        else:
            session['login_id'] = id
            session['login_info'] = dict(students[0])
            session.save() 
        
        if model.course_db.isSudo(model.meta, id):
            if log_flag:
                log_message = 'Login as teacher by %(surname)s,'\
                              ' %(given_names)s (%(id)s)'%students[0]
                log.info(log_message, extra={'clientip': ip_address})
            redirect_to(action='teacher_area') 
        else:
            if log_flag:
                log_message = 'Login by %(surname)s, %(given_names)s'\
                              ' (%(id)s)'%students[0] 
                log.info(log_message, extra={'clientip': ip_address})
            redirect_to(action='student_area')

    def student_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Student area access using no login_id'
            log.info(log_message, extra={'clientip': ip_address})
            return render('/nologin.mako')
        c.student_info = session['login_info']
        c.student_marks = model.course_db.get_results( 
            model.meta, session['login_id'])
        c.message = h.get_msg(g.msg_dir) 
        c.files = h.get_fnames(g.downloads_dir)
        return render('/math0010/student.mako')

    def teacher_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Teacher area access attempt with no login_id'
            log.info(log_message, extra={'clientip':  ip_address})
            return render('/nologin.mako')
        if not model.course_db.isSudo(model.meta, session['login_id']):
            c.error_msg = 'Invalid Login ID'
            log_message = 'Illegal access attempt of teacher area by'\
                          ' %(surname)s, %(given_names)s'\
                          ' (%(id)s)'%session['login_info']
            log.info(log_message, extra={'clientip': ip_address})
            return render('/error.mako')
        students = model.course_db.get_class_list(model.meta)
        c.all_marks = []
        for x in students:
            row = [x]
            row += model.course_db.get_results(model.meta, x.id)
            c.all_marks.append(row)
        c.teacher_info = session['login_info']
        return render('/math0010/teacher.mako')

    def logout(self):
        ip_address = request.environ['REMOTE_ADDR']
        log_message = 'Logout by %(surname)s, %(given_names)s'\
                      ' (%(id)s)'%session['login_info'] 
        log.info(log_message, extra={'clientip': ip_address})
        del session['login_id']  
        del session['login_info']  
        session.save()
        redirect_to(action='index')

    def downloads(self, id=''):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log_message = 'Download "%s" requested without login'%id
            log.info(log_message, extra={'clientip': ip_address})
            return render('/nologin.mako')
        elif id == '':
            log_message = 'Listing of download area requested by'\
                          ' %(surname)s, %(given_names)s (%(id)s)'%(
                          session['login_info'])
            log.info(log_message, extra={'clientip': ip_address})
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        elif id not in h.get_fnames(g.downloads_dir):
            log_message = 'File %s requested by'%id
            log_message2 = ' %(surname)s, %(given_names)s (%(id)s)'\
                          ' but unavailable'%( session['login_info'])
            log.info("%s%s"%(log_message, log_message2),
                extra={'clientip': ip_address})
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        else:
            log_message = 'File %s downloaded by'%id
            log_message2 = ' %(surname)s, %(given_names)s (%(id)s)'\
                          ' but unavailable'%( session['login_info'])
            log.info("%s%s"%(log_message, log_message2),
                extra={'clientip': ip_address})
            return self._serve_file(os.path.join(g.downloads_dir, id))

    def _serve_file(self, path):
        """ Private Function
        Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        fapp = paste.fileapp.FileApp(path)
        return fapp(request.environ, self.start_response)
