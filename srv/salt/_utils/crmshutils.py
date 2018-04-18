# -*- coding: utf-8 -*-
import os
import sys
from contextlib import contextmanager


def to_ascii(s):
    """Convert the bytes string to a ASCII string
    Usefull to remove accent (diacritics)"""
    if s is None:
        return s
    if isinstance(s, str):
        return s
    try:
        return str(s, 'utf-8')
    except UnicodeDecodeError:
        import traceback
        traceback.print_exc()
        return s


def is_process(s):
    """
    Returns true if argument is the name of a running process.

    s: process name
    returns Boolean
    """
    from os.path import join, basename
    # find pids of running processes
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            cmdline = open(join('/proc', pid, 'cmdline'), 'rb').read()
            procname = basename(to_ascii(cmdline).replace('\x00', ' ').split(' ')[0])
            if procname == s:
                return True
        except EnvironmentError:
            # a process may have died since we got the list of pids
            pass
    return False


@contextmanager
def stdchannel_redirected(stdchannel=sys.stdout, dest_filename=os.devnull):
    """
    A context manager to temporarily redirect stdout or stderr
    """
    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())
        yield

    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()
