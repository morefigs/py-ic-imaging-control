#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import *

class GrabberHandle(Structure):
    pass
GrabberHandle._fields_ = [('unused', c_int)]

