from threading import Thread
import cv2

class VideoRecorder:

    def __init__(self, final_img, framerate=0, out_shape=0):
        self.final_img = final_img
        self.framerate = framerate
        self.out_shape = out_shape
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('outpyDIVXMultiThread.avi', self.fourcc , self.framerate, self.out_shape)
        self.stopped = False
        
    def start(self):
        Thread(target=self.record, args=(self.final_img)).start()
        return self

    def record(self, final_img):
        self.final_img = final_img
        while not self.stopped:
            if not self.final_img == None:
                    cv2.imshow('img', self.final_img)

                    cv2.waitKey(27)
                    
                    self.out.write(self.final_img)
        
        print("Out realeased")
        self.out.release()

    def stop(self):
        print('VideoRecorder will be stoped')
        self.stopped = True
