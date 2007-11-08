'''
A module for the Course system
'''

import sqlalchemy as sa

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
        [tt.c.test_id, rt.c.marks, tt.c.max_marks, tt.c.date],
        (id == st.c.id) &
        (st.c.id == rt.c.id) &
        (tt.c.test_id == rt.c.test_id)
        ).order_by(tt.c.date)
    rs = s.execute()
    ys = []
    for x in rs:
        if x.marks != '':
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
    return the full "students" table without prof.
    '''
    st = meta.tables['students']
    # s = sa.select([st.c.id, st.c.surname, st.c.given_names])
    s = st.select()
    s = s.order_by(st.c.surname)
    rs = s.execute()
    lrs = list(rs)
    x = 0
    while x < len(lrs):
        if checkProf(lrs[x]):
            del lrs[x]
            continue
        x+=1
    return lrs

### Other Functions -----------------------------------------------------------
def isSudo(meta, id):
    st = meta.tables['students']
    s = st.select(whereclause=(id == st.c.id))
    s = s.order_by(st.c.surname)
    rs = s.execute()
    student = rs.fetchone()
    return checkProf(student)

def checkProf(student):
    if student.major == 'PROF' and student.program == 'PROF':
        return True
    return False


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
