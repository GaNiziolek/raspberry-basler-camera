from threading import Thread
import cv2
from pypylon import pylon

class VideoProcess:

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
            if not self.unprocessed_img == None:
                print(self.unprocessed_img)
                self.image = self.converter.Convert(self.unprocessed_img)
                self.final_img = self.image.GetArray()
                print("Frame converted")
                #cv2.imshow('img', self.final_img)
                #cv2.waitKey(27)
        print('VideoProcess stoped')

    def stop(self):
        print('VideoProcess will be stoped')
        self.stopped = True