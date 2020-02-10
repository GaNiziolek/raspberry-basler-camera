from threading import Thread
import cv2

class VideoRecorder:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, final_img=None, framerate=0, out_shape=0):
        self.final_img = final_img
        self.framerate = framerate
        self.out_shape = out_shape
        self.fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        self.out = cv2.VideoWriter('outpy-1.avi', -1 , self.framerate, self.out_shape)
        self.stopped = False
        
    def start(self):
        Thread(target=self.record, args=()).start()
        return self

    def record(self):
        while not self.stopped:
            self.out.write(self.final_img)
        
        print("Out realeased")
        self.out.release()
    def stop(self):
        self.stopped = True
