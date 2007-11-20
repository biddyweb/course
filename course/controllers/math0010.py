import logging
import logging.handlers
import os.path 
from subprocess import Popen, PIPE

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
            log.info('[login]: [%s]: : No Login ID Given.'%ip_address)
            return render('/error.mako')

        students = model.course_db.get_student(model.meta, id)
        if students == []:
            c.error_msg = 'No Student with ID=%s <br/> Go to main page to'\
                          ' login'%id
            log.info('[login]: [%s]: [%s]: Student ID Not Found.'\
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
            log_message = '[login]: [%s]: %s'%(ip_address, log_message)
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
                log_message = '[login]: [%s]: %s'%(ip_address, log_message)
                log.info(log_message)
            redirect_to(action='teacher_area') 
        else:
            if log_flag:
                log_message = '[%(id)s] %(surname)s, %(given_names)s: '\
                              'Student Logged in.'%students[0]
                log.info('[login]: [%s]: %s'%(ip_address, log_message))
            redirect_to(action='student_area')

    def student_area(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log.info('[student-area]: [%s]: : NO Student ID Found!'\
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
            log.info('[teacher-area]: [%s]: : NO ID Found!'\
                     %(ip_address))
            return render('/nologin.mako')
        if not model.course_db.isSudo(model.meta, session['login_id']):
            c.error_msg = 'Invalid Login ID'
            log_message = '[%(id)s] %(surname)s, %(given_names)s: '\
                          'NOT A Teacher!'%session['login_info']
            log.info('[teacher-area]: [%s]: %s'%(ip_address,log_message))
            return render('/error.mako')
        students = model.course_db.get_class_list(model.meta)
        c.all_marks = []
        for x in students:
            row = [x]
            row += model.course_db.get_results(model.meta, x.id)
            c.all_marks.append(row)
        c.student_count = len(students)
        c.message = h.get_msg(g.msg_dir).strip() 
        c.files = h.get_fnames(g.downloads_dir)
        c.teacher_info = session['login_info']
        return render('/math0010/teacher.mako')

    def logout(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_info' in session:
            log_message = '[%(id)s] %(surname)s, %(given_names)s:'\
                          ' Logout.'%session['login_info']
            del session['login_info']  
        else:
            log_message = ': Logout requested but not logged in.'
        log.info('[logout]: [%s]: %s'%(ip_address,log_message))
        if 'login_id' in session:
            del session['login_id']  
        session.save()
        redirect_to(action='index')

    def downloads(self, id=''):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session:
            log.info( '[downloads]: [%s]: : File "%s" requested '\
                      'without login'%(ip_address, id))
            return render('/nologin.mako')
        elif id == '':
            log_message = '[%(id)s] %(surname)s, %(given_names)s:'\
                          'Attempted list of downloads.'\
                          %session['login_info']
            log.info('[downloads]: [%s]: %s'%(ip_address, log_message))
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        elif id not in h.get_fnames(g.downloads_dir):
            log_message = '[%(id)s] %(surname)s, %(given_names)s'\
                          %session['login_info']
            log.info('[downloads]: [%s]: %s: "%s" requested but '\
                     'unavailable.'%(ip_address, log_message, id))
            c.error_msg = 'Invalid use of download area'
            return render('/error.mako')
        else:
            log_message = '[%(id)s] %(surname)s, %(given_names)s'\
                          %session['login_info']
            log.info('[downloads]: [%s]: %s: "%s" downloaded.'\
                     %(ip_address, log_message, id))
            return self._serve_file(os.path.join(g.downloads_dir, id))

    def polynom(self):
        ip_address = request.environ['REMOTE_ADDR']
        if 'login_id' not in session or \
            not model.course_db.isSudo(model.meta, session['login_id']):
            log.info('[synthetic_division]: [%s]: : User not logged in.'\
                     %(ip_address))
            return render('/nologin.mako')
        c.error = ""
        try:
            if 'degree' in request.params and request.params['degree'] != '':
                cs = []
                for x in range(int(request.params['degree'])+1):
                    cs.append(request.params['c%s'%x])
                cmd = [g.polynom]+cs
                c.polynom_q = []
                for x in cs:
                    c.polynom_q.append(int(x))
                if not cs:
                    raise Exception("No parameters passed")
                if not c.error:
                    polynom= Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
                    c.polynom_result = polynom[0]
                    errors = polynom[1].strip()
                    if errors:
                        raise Exception(errors)
        except TypeError, KeyError:
            log.info('[polynom]: [%s]: : Invalid Use'%(ip_address))
            c.error = 'Invalid parameters to polynom'
        except OSError, inst:
            log.info('[polynom]: %s'%inst)
            c.error = 'Internal error occured'
        except Exception, inst:
            log.info('[polynom]: %s'%inst)
            c.error = 'Internal error occured'
        return render('/math0010/polynom.mako')

    def _serve_file(self, path):
        """ Private Function
        Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        fapp = paste.fileapp.FileApp(path)
        return fapp(request.environ, self.start_response)
