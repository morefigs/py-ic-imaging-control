# py-ic-imaging-control

py-ic-imaging-control provides control of The Imaging Source (TIS) cameras using only Python. It is a Python wrapper for the IC Imaging Control SDK and wraps the tisgrabber.dll file included in the IC Imaging Control C SDK installer using ctypes. The code currently supports most of the functionality exposed by the DLL file, including frame ready callbacks.

This module only works on Windows due to wrapping a DLL. Tested on Windows 7 with GigE and USB The Imaging Source cameras.

## Installation

Download the IC Imaging Control C SDK from here: http://www.theimagingsource.com/en_US/support/downloads/details/icimagingcontrolcwrapper/

Install to the default directory, ie:

`C:\Users\<USERNAME>\Documents\The Imaging Source Europe GmbH\TIS Grabber DLL`

Add the `\bin\win32` directory to your Windows PATH system variable, ie:

`C:\Users\<USERNAME>\Documents\The Imaging Source Europe GmbH\TIS Grabber DLL\bin\win32`

Install pyicic.

### Basic usage

A code example showing image capture with a camera using an external hardware trigger.

    from pyicic.IC_ImagingControl import *
    
    # open lib
    ic_ic = IC_ImagingControl()
    ic_ic.init_library()

    # open first available camera device
    cam_names = ic_ic.get_unique_device_names()
    cam = ic_ic.get_device(cam_names[0])
    cam.open()

    # change camera properties
    print cam.list_property_names()         # ['gain', 'exposure', 'hue', etc...]
    cam.gain.auto = True                    # enable auto gain
    print cam.exposure.range                # (0, 10)
    emin = cam.exposure.min                 # 0
    emax = cam.exposure.max                 # 10
    cam.exposure.value = (emin + emax) / 2  # disables auto exposure and sets value to half of range
    print cam.exposure.value                # 5
    
    # change camera settings
    formats = cam.list_video_formats()
    cam.set_video_format(formats[0])        # use first available video format
    cam.enable_continuous_mode(True)        # image in continuous mode
    cam.start_live(show_display=True)       # start imaging
    
    cam.enable_trigger(True)                # camera will wait for trigger
    if not cam.callback_registered:
        cam.register_frame_ready_callback() # needed to wait for frame ready callback
    
    for i in xrange(10):                        # take 10 shots
        cam.reset_frame_ready()                 # reset frame ready flag
        
        # send hardware trigger OR call cam.send_trigger() here
        cam.send_trigger()
        
        cam.wait_til_frame_ready()              # wait for frame ready due to trigger
        cam.save_image(''.join(['image-',       # save image
                                str(i),
                                '.jpg']), 1)
    
    cam.stop_live()
    cam.close()

    ic_ic.close_library()
    
