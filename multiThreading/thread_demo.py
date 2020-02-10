from pypylon import pylon
import cv2
from VideoGet import VideoGet
from VideoRecorder import VideoRecorder
from VideoProcess import VideoProcess
from time import time
import numpy as np
import os
from subprocess import check_output

# Configure GPIOZERO lib to monitore the CPU TEMP
#os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')

framerate = 120
record_time = 5 # in seconds
out_shape = (1920,1080)

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(framerate, out_shape, record_time).start()
    video_process = VideoProcess(video_getter.unprocessed_img).start()
    video_recorder = VideoRecorder(video_process.final_img, framerate, out_shape).start()

    while True:
        if video_getter.stopped or video_process.stopped or video_recorder.stopped:
            video_getter.stop()
            video_process.stop()
            video_recorder.stop()
            break

threadBoth()