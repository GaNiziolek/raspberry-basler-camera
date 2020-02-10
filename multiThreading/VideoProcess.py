from threading import Thread
import cv2
from pypylon import pylon

class VideoProcess:
    
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, unprocessed_img):
        self.unprocessed_img = unprocessed_img
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.final_img = 0
        self.stopped = False

    def start(self):
        Thread(target=self.process, args=()).start()
        return self

    def process(self):
        while not self.stopped:
            self.image = self.converter.Convert(self.unprocessed_img)
            self.final_img = self.image.GetArray()

        print('Video converter stoped')
    def stop(self):
        self.stopped = True