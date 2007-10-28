import logging

from course.lib.base import *

log = logging.getLogger(__name__)

class Math0010Controller(BaseController):

    # Actions # --------------------------------------------------------
    def index(self):
        return render('/math0010/index.mako')
    
    def login(self):
        id = request.params['id']
        session['login_id'] = id
        session.save()
        if self.isSudo():
           redirect_to(action='teacher_area') 
        else:
           redirect_to(action='student_area')

    def student_area(self):
        return render('/math0010/student.mako')

    def teacher_area(self):
        if not self.isSudo():
            log.info('Illegal access attempt of teacher area')
            return "This incident will be reported!"
        return  "<b>You Are logged in as %s </b><br/>" \
                "ALL! Students Details To Be Shown Here" % \
                session['login_id']
 
    def logout(self):
        id = request.params['id']
        session['login_id'] = id
        session.save()
        if self.isSudo(id):
           redirect_to(action='teacher_area') 
        else:
           redirect_to(action='student_area')

   
    # Helper functions # -----------------------------------------------
    def isSudo(self):
        if session['login_id'] == 'PETER':
            return True
        return False

    def isStudent(self):
        return True
