import multiprocessing as mp

import cv2
from pypylon import pylon
from time import time
import numpy as np
import os

class VideoGet:

    def __init__(self, frameQueue, framerate, record_time, virtual=False):

        self.mean_fps = []

        self.running = mp.Queue()
        
        self.p = mp.Process(name='VideoGet', target=self.get, args=(frameQueue, self.running, record_time, framerate, virtual))

    def start(self):

        self.p.start()

        return self

    def stop(self):
        print('VideoGet will be stoped')
        self.running.put(False)

        print(np.mean(self.mean_fps))

        self.p.join()

    def get(self, frameQueue, running, recordTime, framerate, virtual=False):

        if virtual:
            os.environ["PYLON_CAMEMU"] = "1"

        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        if not virtual:
            print("Reading file back to camera's node map...")
            pylon.FeaturePersistence.Load('cameraFeatures.pfs', camera.GetNodeMap(), False)
            camera.AcquisitionFrameRateEnable.SetValue(True)
            camera.AcquisitionFrameRate.SetValue(framerate)
            camera.ExposureTime.SetValue(1000000/framerate)
            print("Camera capturing in: " + str(camera.AcquisitionFrameRate.GetValue()) + " fps.")
            print("Camera shape: " + str(camera.Width.GetValue()) + "x" + str(camera.Height.GetValue()))

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed

        counter = 0
        timerCounter = 0
        start_time = 0

        while camera.IsGrabbing or running.empty():
            counter += 1
            timerCounter += 1
            
            start_time = time()
            grabResult = camera.RetrieveResult(100000000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():

                image = converter.Convert(grabResult)

                frameQueue.put(image.GetArray())

                cv2.imshow('img', image.GetArray())
                cv2.waitKey(27)

                if timerCounter > (recordTime * framerate):
                    running.put(False)

            grabResult.Release()

            #if counter >= framerate:
            #    counter = 0
            #    self.mean_fps.append(round(1/(time()-start_time)))
            
        camera.StopGrabbing()
        print('O processo ' + str(mp.current_process().name) + ' foi interrompido com sucesso.')

if __name__ == '__main__':

    frameQueue = mp.Queue()
    VG = VideoGet(frameQueue, 10, 5, virtual=True)
    VG.start()
