from pypylon import pylon
import cv2
from time import time
import numpy as np

framerate = 24
record_time = 30 # in seconds
out_shape = (1920,1080)

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

print("Reading file back to camera's node map...")
pylon.FeaturePersistence.Load('cameraFeatures.pfs', camera.GetNodeMap(), False)

# Setting parameters
camera.AcquisitionFrameRateEnable.SetValue(True)
camera.AcquisitionFrameRate.SetValue(framerate)

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (2448,2048)) # AVI Capture
fourcc = cv2.VideoWriter_fourcc(*'H264')

#fourcc = cv2.VideoWriter_fourcc('H','2','6','4')

out = cv2.VideoWriter('outpyH264.mp4', fourcc , framerate, out_shape) # MP4 Capture
start_time = 0
counter = 0
counter2 = 0
mean_fps = []
#cv2.namedWindow('title', cv2.WINDOW_NORMAL)
while camera.IsGrabbing:
    counter += 1
    counter2 += 1
    start_time = time()
    grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()

        #print(img.shape[0])

        
        #cv2.imshow('title', img)
        out.write(img)

        #k = cv2.waitKey(1)
        if counter2 > (record_time*framerate):
            break

    grabResult.Release()

    if counter > framerate:
        print('Recording... FPS:' + str(round(1/(time()-start_time))) + '  Temp:' + str(camera.DeviceTemperature.GetValue()))
        counter = 0
        mean_fps.append(round(1/(time()-start_time)))

# Releasing the resource    
camera.StopGrabbing()
print(np.mean(mean_fps))
out.release()
cv2.destroyAllWindows()
