#!/usr/bin/env python
# -*- coding: utf-8 -*-

# todo list
# color format type
# buffer

from IC_GrabberDLL import IC_GrabberDLL
from IC_Camera import IC_Camera
from IC_Exception import IC_Exception

class IC_ImagingControl(object):
    
    def __init__(self):
        
        # remember list of devices
        self._unique_device_names = None
        
        # remember device objects
        self._devices = {}
        
    def init_library(self):
        """
        Initialise the IC Imaging Control library.
        """        
        # no license key
        err = IC_GrabberDLL.init_library(None)
        if err != 1:
            raise IC_Exception(err)
    
    def get_unique_device_names(self):
        """
        Gets unique names (i.e. model + label + serial) of devices.
        
        :returns: list -- unique devices names.
        """
        if self._unique_device_names is None:
                   
            # make new list
            self._unique_device_names = []
            
            # get num devices, must be called before get_unique_name_from_list()!
            num_devices = IC_GrabberDLL.get_device_count()
            if num_devices < 0:
                raise IC_Exception(num_devices)
            
            # populate list
            for i in xrange(num_devices):
                self._unique_device_names.append(IC_GrabberDLL.get_unique_name_from_list(i))
        
        return self._unique_device_names
    
    def get_device(self, unique_device_name):
        """
        Gets camera device object based on unique name string.
        Will create one only if it doesn't already exist.

        :param device_name: string -- the unique name of the device.

        :returns: IC_Camera object -- the camera device object requested.	
        """
        # check name is valid
        if unique_device_name in self.get_unique_device_names():
            
            # check if already have a ref to device
            if unique_device_name not in self._devices:
                
                # if not, create one
                self._devices[unique_device_name] = IC_Camera(unique_device_name)
                
            return self._devices[unique_device_name]
        
        raise IC_Exception(todo)
    
    def close_library(self):
        """
        Close the IC Imaging Control library.
        """
        IC_GrabberDLL.close_library()
        
        
