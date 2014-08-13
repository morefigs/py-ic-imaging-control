# py-ic-imaging-control

py-ic-imaging-control is a Python wrapper for the IC Imaging Control SDK from The Imaging Source (TIS). It wraps the tisgrabber.dll file included in the IC Imaging Control C SDK installer. It supports most of the functionality exposed by the DLL file, including frame ready callbacks.

## Installation

Download the IC Imaging Control C SDK from here: http://www.theimagingsource.com/en_US/support/downloads/details/icimagingcontrolcwrapper/

Install to the default directory.

Add this directory to your Windows PATH system variable.

Install pyicic.

### Basic usage
    
    from ctypes import *
    from pyicic.IC_ImagingControl import IC_ImagingControl
    
    icic = IC_ImagingControl()
    icic.init_library()
    
    cam_names = icic.get_unique_device_names()
    cam_name = cam_names[0]
    cam = icic.get_device(cam_name)
    cam.open()
    
    print cam.list_property_names()         # ['gain', 'exposure', 'hue', etc...]
    cam.gain.auto = True                    # enable auto gain
    print cam.exposure.range                # e.g. (1, 10)
    cam.exposure.value = 5                  # disables auto exposure and sets value
    print cam.exposure.value                # e.g. 5
    
    cam.enable_trigger(True)                # camera will wait for trigger
    cam.set_video_format('RGB24 (640x480)')
    if not cam.callback_registered:
        cam.register_frame_ready_callback() # needed to wait for frame ready callback
    cam.enable_continuous_mode(True)        # image in continuous mode
    cam.start_live(show_display=True)       # start imaging
    
    for i in xrange(10):                        # take 10 shots
        cam.reset_frame_ready()                 # reset frame ready flag
        cam.wait_til_frame_ready(3000)          # wait up to 3 seconds for a trigger
        img_ptr = cam.get_buffer()              # pointer to image data
        img = cast(img_ptr, POINTER(c_ubyte * 640 * 480 * 3))
    cam.stop_live()
    
    icic.close_library()
    
