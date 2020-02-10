from threading import Thread
import cv2
from pypylon import pylon
from time import time
import numpy as np

class VideoGet:

    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, framerate, out_shape, record_time):
            self.framerate  = framerate
            self.out_shape  = out_shape
            self.record_time = record_time
            self.unprocessed_img = 0
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            print("Reading file back to camera's node map...")
            pylon.FeaturePersistence.Load('cameraFeatures.pfs', self.camera.GetNodeMap(), False)
            self.camera.AcquisitionFrameRateEnable.SetValue(True)
            self.camera.AcquisitionFrameRate.SetValue(self.framerate)
            self.camera.ExposureTime.SetValue(1000000/self.framerate)
            print("Camera capturing in: " + str(self.camera.AcquisitionFrameRate.GetValue()) + " fps.")
            print("Camera shape: " + str(self.camera.Width.GetValue()) + "x" + str(self.camera.Height.GetValue()))

            


            self.start_time = 0
            self.counter = 0
            self.counter2 = 0
            self.mean_fps = []

            print('FPS | Camera Temp. | CPU Temp | Core Volts')

            self.stopped = False
            
    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while self.camera.IsGrabbing and not self.stopped:
            self.counter += 1
            self.counter2 += 1
            self.start_time = time()
            self.grabResult = self.camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)

            if self.grabResult.GrabSucceeded():

                self.unprocessed_img = self.grabResult

                if self.counter2 > (self.record_time * self.framerate):
                    self.stop()

            self.grabResult.Release()

            if self.counter >= self.framerate:
                #cpu_temp  = CPUTemperature()
                self.cpu_temp  = 0
                #cpu_volts = str(check_output(['sudo', 'vcgencmd', 'measure_volts']))[7:-3] 
                self.cpu_volts = 0
                #print(' {:02d}'.format(round(1/(time()-start_time))) +
                #      ' | ' + str(camera.DeviceTemperature.GetValue()) + '°C' +
                #      '       | ' + str(round(cpu_temp.temperature, 1)) + '°C' +
                #      '   | ' + cpu_volts)
                print(' {:02d}'.format(round(1/(time()-self.start_time))) + 
                        ' | ' + str(self.camera.DeviceTemperature.GetValue()) + '°C')

                self.counter = 0
                self.mean_fps.append(round(1/(time()-self.start_time)))
        
        print('Camera Grabbing stoped')
        self.camera.StopGrabbing()

    def stop(self):
        self.stopped = True
        print(np.mean(self.mean_fps))