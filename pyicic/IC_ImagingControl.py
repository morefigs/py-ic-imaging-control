#!/usr/bin/env python
# -*- coding: utf-8 -*-

from IC_GrabberDLL import IC_GrabberDLL
from IC_Camera import IC_Camera
from IC_Exception import IC_Exception

class IC_ImagingControl(object):
    
    def init_library(self):
        """
        Initialise the IC Imaging Control library.
        """
        # remember list of unique device names
        self._unique_device_names = None
        
        # remember device objects by unique name
        self._devices = {}        
        
        # no license key needed anymore
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
        
        raise IC_Exception(-106)
    
    def close_library(self):
        """
        Close the IC Imaging Control library, and close and release all references to camera devices.
        """        
        # release handle grabber objects of cameras as they won't be needed again.
        # try to close & delete each known device, but only if we own the reference to it!
        for unique_device_name in self.get_unique_device_names():
            if unique_device_name in self._devices:
                # close camera device if open
                if self._devices[unique_device_name].is_open():
                    self._devices[unique_device_name].close()
                
                # release grabber of camera device
                IC_GrabberDLL.release_grabber(self._devices[unique_device_name]._handle)
        
        # kill refs
        self._unique_device_names = None
        self._devices = None
        
        # close lib        
        IC_GrabberDLL.close_library()
        
        
