"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from os import path, listdir

def get_msg(msg_dir):
    '''
    Get all messages in msg_dir relevant to student with id=id
    '''
    msg_paths = [path.join(msg_dir, x) for x in listdir(msg_dir)]
    msgs = []
    for p in msg_paths:
        f = open(p)
        msgs.append(f.read())
        f.close()
    return "\n".join(msgs)

def get_fnames(dir):
    '''
    Get all downloadable file names in dir
    '''
    return listdir(dir) 
