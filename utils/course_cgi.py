'''
A CGI/SCGI module for the Course system
'''

import sqlalchemy as sa
from os import listdir

###  Course database  ---------------------------------------------------------

def meta_auto_load(engine):
    meta = sa.MetaData()
    meta.bind = engine
    meta.reflect()
    return meta


#  queries  -------------------------------------------------------------------

def get_marks(meta, id):
    '''
    return [(test_id, marks, max_marks), ...] for the given student id
    '''
    st = meta.tables['students']
    tt = meta.tables['tests']
    rt = meta.tables['results']
    s = sa.select(
        [tt.c.test_id, rt.c.marks, tt.c.max_marks],
        (id == st.c.id) &
        (st.c.id == rt.c.id) &
        (tt.c.test_id == rt.c.test_id)
        )
    rs = s.execute()
    return list(rs)
 

def get_results(meta, id):
    '''
    return [(test_id, percentage), ...] for the given student id
    '''
    st = meta.tables['students']
    tt = meta.tables['tests']
    rt = meta.tables['results']
    s = sa.select(
        [tt.c.test_id, rt.c.marks, tt.c.max_marks],
        (id == st.c.id) &
        (st.c.id == rt.c.id) &
        (tt.c.test_id == rt.c.test_id)
        )
    rs = s.execute()
    ys = []
    for x in rs:
        if x.marks:
            ys.append((x.test_id, x.marks * 100.0 / x.max_marks))
        else:
            ys.append((x[0], '---'))
    return ys
 

def get_student(meta, id):
    '''
    get [(id, surname, given_names)] for a particular student
    '''
    st = meta.tables['students']
    s = sa.select([st.c.id, st.c.surname, st.c.given_names], id == st.c.id)
    s = s.order_by(st.c.surname)
    rs = s.execute()
    return list(rs)


def get_class_list(meta):
    '''
    return the full "students" table
    '''
    st = meta.tables['students']
    # s = sa.select([st.c.id, st.c.surname, st.c.given_names])
    s = st.select()
    s = s.order_by(st.c.surname)
    rs = s.execute()
    return list(rs)

### Other Functions -----------------------------------------------------------
def get_msg(msg_dir, id):
    '''
    Get all messages in msg_dir relevant to student with id=id
    '''
    msg_paths = ['%s/motd.txt'%msg_dir]
    msgs = []
    for path in msg_paths:
        f = open(path)
        msgs.append(f.read())
        f.close()
    return "\n".join(msgs)

def get_fnames(dir):
    '''
    Get all downloadable file names in dir
    '''
    return listdir(dir) 

def isSudo(id):
    if id == 'PETER':
        return True
    return False

#    def isStudent(self):
#        return True

#  main just for testing the module  ------------------------------------------`

if __name__ == '__main__':
    import sys
    db_file = sys.argv[1]
    engine = sa.create_engine('sqlite:///%s' % db_file)
    meta = meta_auto_load(engine)
    if len(sys.argv) > 2:
        students = get_student(meta, sys.argv[2])
    else:
        students = get_class_list(meta)

    for x in students:
        name = '%s, %s' % (x.surname, x.given_names)
        print '%s  %-22s' % (x.id, name),
        ys = get_results(meta, x.id)
        for y in ys:
            try:
                print ' %6.2f%%' % y[1],
            except TypeError:
                print ' %6s ' % y[1],
        print


# vim: ai ts=4 et sw=4 tw=80
