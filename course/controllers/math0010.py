import logging
import logging.handlers
import os.path

from course.lib.base import *
from course import model
import paste.fileapp

logging.basicConfig(level=logging.INFO,
                    format='%(module)s[%(process)d]:%(message)s')
log = logging.getLogger(__name__)
log.addHandler( logging.handlers.SysLogHandler('/dev/log',
                logging.handlers.SysLogHandler.LOG_USER))


class Math0010Controller(BaseController):

    # Actions # --------------------------------------------------------
    def index(self):
        if 'login_id' in session:
            c.logged_in = True
            c.login_name = "%(given_names)s %(surname)s"%session['login_info']
        else:
            c.logged_in = False
        return render('/math0010/index.mako')
    
    def login(self):
        '''
        login page
        '''
        ip_address = request.environ['REMOTE_ADDR']
        log_flag = True
        if 'id' in request.params and request.params['id'] != '':
            id = request.params['id']
        elif 'login_id' in session:
            id = session['login_id']
            log_flag = False
        else:
            c.error_msg = 'No login id given <br/> Go to the main page'\
                          ' to login.'
            log.info('[LOGIN]: [%s]: : No Login ID Given.'%ip_address)
            return render('/error.mako')

        students = model.course_db.get_student(model.meta, id)
        if students == []:
            c.error_msg = 'No Student with ID=%s <br/> Go to main page to'\
                          ' login'%id
            log.info('[LOGIN]: [%s]: [%s]: Student ID Not Found.'\
                     %(ip_address, id))
            return render('/error.mako')
        elif model.course_db.isCancelled(model.meta, id):
            c.error_msg = \
                'You are not registered for this course any more.<br/>'\
                'If that is not correct, please contact your professor'\
                ' or the administration.'
            log_message = '[%(id)s] %(surname)s,%(given_names)s: '\
                          'De-registered student attempted login.'\
                          %students[0]
            log_message = '[LOGIN]: [%s]: %s'%(ip_address, log_message)
            log.info(log_message)
            return render('/error.mako')
        else:
            session['login_id'] = id
            session['login_info'] = dict(students[0])
            session.save() 
        
        if model.course_db.isSudo(model.meta, id):
            if log_flag:
                log_message = '[%(id)s] %(surname)s,%(given_names)s: '\
                              'Teacher Logged in.'%students[0]
                log_message = '[LOGIN]: [%s]: %s'%(ip_address, log_message)
                log.info(log_message)
            redirect_to(action='teacher_area') 
        else:
            if log_flag:
                log_message = '[%(id)s] %(surname)s, %(given_names)s: '\
                              'Student Logged in.'%students[0]
                log.info('[LOGIN]: [%s]: %s'%(ip_address, log_message))
            redirect_to(action='student_area')

    def student_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log.info('[STUDENT-AREA]: [%s]: : NO Student ID Found!'\
                     %(ip_address))
            return render('/nologin.mako')
        c.student_info = session['login_info']
        c.student_marks = model.course_db.get_results( 
            model.meta, session['login_id'])
        c.message = h.get_msg(g.msg_dir).strip() 
        c.files = h.get_fnames(g.downloads_dir)
        return render('/math0010/student.mako')

    def teacher_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log.info('[TEACHER-AREA]: [%s]: : NO ID Found!'\
                     %(ip_address))
            return render('/nologin.mako')
        if not model.course_db.isSudo(model.meta, session['login_id']):
            c.error_msg = 'Invalid Login ID'
            log_message = '[%(id)s] %(surname)s, %(given_names)s: '\
                          'NOT A Teacher!'%session['login_info']
            log.info('[TEACHER-AREA]: [%s]: %s'%(ip_address,log_message))
            return render('/error.mako')
        students = model.course_db.get_class_list(model.meta)
        c.all_marks = []
        for x in students:
            row = [x]
            row += model.course_db.get_results(model.meta, x.id)
            c.all_marks.append(row)
        c.message = h.get_msg(g.msg_dir).strip() 
        c.files = h.get_fnames(g.downloads_dir)
        c.teacher_info = session['login_info']
        return render('/math0010/teacher.mako')

    def logout(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_info' in session:
            log_message = '[%(id)s] %(surname)s, %(given_names)s:'\
                          'Logout.'%session['login_info']
        else:
            log_message = ': Logout requested but not logged in.'\
                          %session['login_info']
        log.info('[LOGOUT]: [%s]: %s'%(ip_address,log_message))
        del session['login_id']  
        del session['login_info']  
        session.save()
        redirect_to(action='index')

    def downloads(self, id=''):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log.info( '[DOWNLOADS]: [%s]: : File "%s" requested '\
                      'without login'%(ip_address, id))
            return render('/nologin.mako')
        elif id == '':
            log_message = '[%(id)s] %(surname)s, %(given_names)s:'\
                          'Attempted list of downloads.'\
                          %session['login_info']
            log.info('[DOWNLOADS]: [%s]: %s'%(ip_address, log_message))
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        elif id not in h.get_fnames(g.downloads_dir):
            log_message = '[%(id)s] %(surname)s, %(given_names)s'\
                          %session['login_info']
            log.info('[DOWNLOADS]: [%s]: %s: "%s" requested but '\
                     'unavailable.'%(ip_address, log_message, id))
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        else:
            log_message = '[%(id)s] %(surname)s, %(given_names)s'\
                          %session['login_info']
            log.info('[DOWNLOADS]: [%s]: %s: "%s" downloaded.'\
                     %(ip_address, log_message, id))
            return self._serve_file(os.path.join(g.downloads_dir, id))

    def synthetic_division(self):
#        ip_address = request.environ['REMOTE_ADDR']
#        if 'login_id' not in session:
#            log.info('[synthetic_division]:[%s]::User not logged in.'\
#                     %(ip_address))
#            return render('/nologin.mako')
        return render('/math0010/synthetic.mako')

    def synthetic_calc(self):
#        ip_address = request.environ['REMOTE_ADDR']
#        if 'login_id' not in session:
#            log.info('[synthetic_division]:[%s]::User not logged in.'\
#                     %(ip_address))
#            return render('/nologin.mako')
        if 'degree' in request.params and request.params['degree'] != '':
            cs = []
            for x in range(int(request.params['degree'])+1):
                cs.append(request.params['c%s'%x])
        else:
            c.error_msg = 'Invalid parameters to synthetic calculator.'
            log.info('[synthetic_division]: [%s]: : '%(ip_address))
            return render('/error.mako')
        c.msg = ", ".join(cs)
        return render('/math0010/synthetic_res.mako')



    def _serve_file(self, path):
        """ Private Function
        Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        fapp = paste.fileapp.FileApp(path)
        return fapp(request.environ, self.start_response)
