#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import *
import time

from IC_GrabberDLL import IC_GrabberDLL
from IC_Exception import IC_Exception
from IC_Structures import GrabberHandle
from IC_Property import IC_Property

# "typedefs"
IMG_FILETYPE = ['FILETYPE_BMP',
                'FILETYPE_JPG']
COLOR_FORMAT = ['Y800',
                'RGB24',
                'RGB32',
                'UYVY',
                'Y16',
                'NONE']

# c function type for frame callback
# outside of class so it can be called by unbound function
C_FRAME_READY_CALLBACK = CFUNCTYPE(None, GrabberHandle, POINTER(c_ubyte), c_ulong, c_void_p)

class IC_Camera(object):
    
    @property
    def callback_registered(self):
        return self._callback_registered
  
    def __init__(self, unique_device_name):
        
        self._unique_device_name = unique_device_name
        
        self._handle = IC_GrabberDLL.create_grabber()
        if not self._handle:
            raise IC_Exception(todo)
        
        self._callback_registered = False
        self._frame = {'num'    :   -1,
                       'ready'  :   False}
        
    def __getattr__(self, attr):
    
        if attr in IC_Property.get_all_property_names():
            return IC_Property(self._handle, attr)
        else:
            raise IC_Exception(-101)
        
    #def __setattr__(self, attr, val):
    #    
    #    if attr.startswith('_'):
    #        super(IC_Camera, self).__setattr__(attr, val)
    #
    #    # if it's an actual device property
    #    elif attr in self.get_all_property_names():
    #        IC_Property(self._handle, attr).value = val
    #
    #    # otherwise just set the attribute value as normal
    #    else:
    #        super(IC_Camera, self).__setattr__(attr, val)
        
    def open(self):
        """
        Open the camera device, required for most functions.
        """
        err = IC_GrabberDLL.open_device_by_unique_name(self._handle,
                                                       self._unique_device_name)
        if err != 1:
            raise IC_Exception(err)
    
    def is_open(self):
        """
        Check if the camera device is currently open.
        
        :returns: boolean -- True if camera is open.
        """
        return bool(IC_GrabberDLL.is_dev_valid(self._handle))
    
    def show_property_dialog(self):
        """
        Show property dialog for device.
        """
        err = IC_GrabberDLL.show_property_dialog(self._handle)
        if err != 1:
            raise IC_Exception(err)
    
    def list_property_names(self):
        return IC_Property.get_all_property_names()
    
    # use props instead, e.g. cam.gain.range
    #def get_property_range(self, property_name):
    #    return IC_Property(self._handle, property_name).range
    #
    #def is_property_available(self, property_name):
    #    return IC_Property(self._handle, property_name).is_available
    #
    #def is_property_auto_available(self, property_name):
    #    return IC_Property(self._handle, property_name).is_auto_available
    #
    #def get_property_type(self, property_name):
    #    return IC_Property(self._handle, property_name).type
    
    def list_video_formats(self):
        """
        :returns: list -- available video formats.
        """
        vf_list = ((c_char * 80) * 40)()
        num_vfs = IC_GrabberDLL.list_video_formats(self._handle, byref(vf_list), c_int(80))
        if num_vfs < 0:
            raise IC_Exception(num_vfs)
        return_list = []
        for vf in vf_list:
            if vf.value:
                return_list.append(vf.value)
        return return_list    
    
    def get_video_format_count(self):
        """
        :returns: int -- number of available video formats.
        """
        vf_count = IC_GrabberDLL.get_video_format_count(self._handle)
        if vf_count < 0:
            raise IC_Exception(vf_count)
        return vf_count
    
    def get_video_format(self, format_index):
        """
        Get video format of the device.
        """
        # DLL says need to call this first for it to work
        num_vfs = self.get_video_format_count()
        if format_index >= num_vfs:
            raise IC_Exception(todo)
        vf = IC_GrabberDLL.get_video_format(self._handle, c_int(format_index))
        if vf is None:
            raise IC_Exception(err)
        return vf
    
    def set_video_format(self, video_format):
        """
        Set a video format for the device. Must be supported.
        
        :param video_format: string -- video format to use.
        """
        err = IC_GrabberDLL.set_video_format(self._handle, c_char_p(video_format))
        if err != 1:
            raise IC_Exception(err)
    
    def get_video_format_width(self):
        """
        """
        return IC_GrabberDLL.get_video_format_width(self._handle)
        
    def get_video_format_height(self):
        """
        """
        return IC_GrabberDLL.get_video_format_height(self._handle)
        
    def get_format(self):
        """
        """
        return IC_GrabberDLL.get_format(self._handle)
    
    def set_format(self, format):
        """
        """
        err = IC_GrabberDLL.set_format(self._handle, c_int(value))
        if err != 1:
            raise IC_Exception(err)
            
    def is_triggerable(self):
        """
        """
        return bool(IC_GrabberDLL.is_trigger_available(self._handle))
        
    def get_frame_rate(self):
        """
        """
        return IC_GrabberDLL.get_frame_rate(self._handle)
    
    def set_frame_rate(self, frame_rate):
        """
        """
        err = IC_GrabberDLL.set_frame_rate(self._handle, c_float(value))
        if err != 1:
            raise IC_Exception(err)
    
    def enable_trigger(self, enable):
        """
        Enable or disable camera triggering.

        :param enable: boolean -- True to enable the trigger, False to disable.
        """
        err = IC_GrabberDLL.enable_trigger(self._handle, c_int(int(enable)))
        if err != 1:
            #raise IC_Exception(err)
            pass # todo, always raises false error for some reason...?
    
    def enable_continuous_mode(self, enable):
        """
        Enable or disable continuous mode.
        
        :param enable: boolean -- True to enable continuous mode, False to disable.
        """
        actual = not enable
        #print actual, enable, c_int(int(actual))
        err = IC_GrabberDLL.set_continuous_mode(self._handle, c_int(int(actual)))
        if err != 1:
            #raise IC_Exception(err)
            pass # todo, always raises false error for some reason...?

    def send_trigger(self):
        """
        Send a software trigger to fire the device when in triggered mode.
        """
        err = IC_GrabberDLL.software_trigger(self._handle)
        if err != 1:
            raise IC_Exception(err)
        
    def prepare_live(self, show_display=False):
        """
        Prepare the device for live video.
        """
        err = IC_GrabberDLL.prepare_live(self._handle, c_int(int(show_display)))
        if err != 1:
            raise IC_Exception(err)
            
    def start_live(self, show_display=False):
        """
        Start the live video.
        """
        err = IC_GrabberDLL.start_live(self._handle, c_int(int(show_display)))
        if err != 1:
            raise IC_Exception(err)
    
    def suspend_live(self):
        """
        Suspend the live video and put into a prepared state.
        """
        err = IC_GrabberDLL.suspend_live(self._handle)
        if err != 1:
            raise IC_Exception(err)
        
    def stop_live(self):
        """
        Stop the live video.
        """
        IC_GrabberDLL.stop_live(self._handle)
        
    def get_image_description(self):
        pass # todo
    
    def snap_image(self, timeout=1000):
        """
        Snap an image. Device must be set to live mode and a format must be set.
        
        :param timeout: int -- time out in milliseconds.
        """
        err = IC_GrabberDLL.snap_image(self._handle, c_int(timeout))
        if err != 1:
            raise IC_Exception(err)
    
    def get_buffer(self):
        """
        Get image buffer from camera.
        
        :returns: ctypes pointer -- pointer to image data. todo, return data.
        """
        img_ptr = IC_GrabberDLL.get_image_ptr(self._handle)
        if img_ptr is None:
            raise IC_Exception(todo)
        
        #img_data = cast(img_ptr, POINTER(c_ubyte * buffer_size))
        ####array = (c_ubyte * iheight * iwidth * 3).from_address(addressof(data.contents))
        #array = img_data.contents

        return img_ptr

    def save_image(self, filename, filetype=1, jpeq_quality=75):
        """
        Save the contents of the last snapped image into a file.
        
        :param filename: string -- filename to name saved file.
        :param filetype: int -- 0 = BMP, 1 = JPEG.
        :param jpeq_quality: int -- JPEG file quality, 0-100.
        """
        err = IC_GrabberDLL.save_image(self._handle,
                                       c_char_p(filename),
                                       c_int(filetype),
                                       c_long(jpeq_quality))
        if err != 1:
            raise IC_Exception(err)
    
    # generate callback function so it is not a bound method
    # (cb_func cannot have the self parameter)
    def _get_callback_func(self):
        def cb_func(handle, p_data, frame_num, data):
            self._frame['ready'] = True
            self._frame['num'] = frame_num
        return C_FRAME_READY_CALLBACK(cb_func)
    
    def register_frame_ready_callback(self):
        """
        Register the frame ready callback with the device.
        """
        # keep ref to prevent garbage collection
        self._rfrc_func = self._get_callback_func()
        
        # register callback function with DLL
        # instead of passing pointer to a variable (3rd param) we will set the flag ourselves
        IC_GrabberDLL.set_frame_ready_callback(self._handle, self._rfrc_func, None)
        
        self._callback_registered = True
        
    def reset_frame_ready(self):
        """
        Reset the frame ready flag to False, generally so
        that wait_til_frame_ready() can be called again.
        """
        self._frame['ready'] = False
        self._frame['num'] = -1
        
    def wait_til_frame_ready(self, timeout=0):
        """
        Wait until the devices announces a frame as being ready.
        Requires register_frame_ready_callback() being called.
        
        :param timeout: int -- timeout in milliseconds. Set to 0 for no timeout.
        
        :returns: int -- frame number that was announced as ready.
        """
        if timeout:        
            start = time.clock()
            elapsed = (time.clock() - start) * 1000
            while not self._frame['ready'] and elapsed < timeout:
                time.sleep(0.001)
                elapsed = (time.clock() - start) * 1000
        else:
            while not self._frame['ready']:
                time.sleep(0.001)

        return self._frame['num']
    
    
    
    
