#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import *

class GrabberHandle(Structure):
    pass
GrabberHandle._fields_ = [('unused', c_int)]

class FilterParameter(Structure):
    pass
FilterParameter._fields_ = [('Name', c_char * 30),
                            ('Type', c_int)]

class FrameFilterHandle(Structure):
    pass
FrameFilterHandle._fields_ = [('pFilter', c_void_p),
                              ('bHasDialog', c_int),
                              ('ParameterCount', c_int),
                              ('Parameters', POINTER(FilterParameter))]