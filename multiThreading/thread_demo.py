from pypylon import pylon
import cv2
from VideoGet import VideoGet
from VideoRecorder import VideoRecorder
from VideoProcess import VideoProcess
from time import time, sleep
import numpy as np
import os
from subprocess import check_output

# Configure GPIOZERO lib to monitore the CPU TEMP
#os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')

framerate = 60
record_time = 20 # in seconds
out_shape = (1920,1080)

def threadBoth(source=0):

    video_getter = VideoGet(framerate, out_shape, record_time, virtual=True).start()
    #video_process = VideoProcess(video_getter.unprocessed_img).start()
    #video_recorder = VideoRecorder(video_getter.final_img, framerate, out_shape).start()
    sleep(1)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('outpyDIVXMultiThread.avi', fourcc , framerate, out_shape)
    while True:
        #print(video_getter.final_img)

        if not video_getter.final_img.any() == None:
            out.write(video_getter.final_img)

        if video_getter.stopped:
            print("VideoGet causes a stop")
            #video_getter.stop()
            #video_recorder.stop()
            break
        '''
        elif video_recorder.stopped:
            print("VideoRecorder causes a stop")
            video_getter.stop()
            video_recorder.stop()
            break
            '''
    out.release()

threadBoth()