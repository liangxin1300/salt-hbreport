# -*- coding: utf-8 -*-
import os
import sys
from contextlib import contextmanager


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
