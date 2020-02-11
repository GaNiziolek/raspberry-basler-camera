from pypylon import pylon
import cv2
from time import time
import numpy as np
import os
#from gpiozero import CPUTemperature
from subprocess import check_output

# Configure GPIOZERO lib to monitore the CPU TEMP
#os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')

framerate = 120
record_time = 5 # in seconds
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
camera.ExposureTime.SetValue(1000000/framerate)
print("Camera capturing in: " + str(camera.AcquisitionFrameRate.GetValue()) + " fps.")
print("Camera shape: " + str(camera.Width.GetValue()) + "x" + str(camera.Height.GetValue()))

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
#converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (2448,2048)) # AVI Capture
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

#fourcc = cv2.VideoWriter_fourcc('H','2','6','4')

out = cv2.VideoWriter('outpyDIVX.avi', fourcc , framerate, out_shape)
start_time = 0
counter = 0
counter2 = 0
mean_fps = []
#cv2.namedWindow('title', cv2.WINDOW_NORMAL)

# Create the Header
print('FPS | Camera Temp. | CPU Temp | Core Volts')
while camera.IsGrabbing:
    counter += 1
    counter2 += 1
    start_time = time()
    grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        
        #cv2.imshow('title', img)
        out.write(img)

        #k = cv2.waitKey(1)
        if counter2 > (record_time*framerate):
            break

    grabResult.Release()

    if counter > framerate:
        #cpu_temp  = CPUTemperature()
        cpu_temp  = 0
        #cpu_volts = str(check_output(['sudo', 'vcgencmd', 'measure_volts']))[7:-3] 
        cpu_volts = 0
        #print(' {:02d}'.format(round(1/(time()-start_time))) +
        #      ' | ' + str(camera.DeviceTemperature.GetValue()) + '°C' +
        #      '       | ' + str(round(cpu_temp.temperature, 1)) + '°C' +
        #      '   | ' + cpu_volts)
        print(' {:02d}'.format(round(1/(time()-start_time))) + 
              ' | ' + str(camera.DeviceTemperature.GetValue()) + '°C')

        counter = 0
        mean_fps.append(round(1/(time()-start_time)))
# Releasing the resource    
camera.StopGrabbing()
print(np.mean(mean_fps))
out.release()
cv2.destroyAllWindows()
