from imutils.video import VideoStream
import pysftp
import RPi.GPIO as GPIO
import os
import fileinput
import cv2
import datetime
import time
import calendar;

def takePicture():
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(0.5)
    frame = vs.read()
    ts = calendar.timegm(time.gmtime())
    # t = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d _%H-%M-%S')
    filename = 'picture_' +str(ts)
    p = os.path.sep.join(["pictures", "{}.png".format(filename)])
    cv2.imwrite(p, frame)
    print("[INFO] picture saved...")
    vs.stop()
    print("[INFO] closing video stream...")
    time.sleep(0.5)
    return filename


def uploadPicure():
    filename = takePicture() 

    if not filename:
        print("[ERROR] filename empty...")
        return

    myHostname = "home737842737.1and1-data.host"
    myUsername = "u93606195-iot"
    myPassword = "Dfs15@15"
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
        print("Connection succesfully stablished ... ")

        # Define the file that you want to upload from your local directorty
        # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
        localFilePath = './pictures/'+filename+'.png'

        # Define the remote path where the file will be uploaded
        remoteFilePath = '/pictures/'+filename+'.png'

        sftp.put(localFilePath, remoteFilePath)
    
    # connection closed automatically at the end of the with-block
    return
    

def button_callback():
    # TODO - call function + prendre photo
    print("button pressed")


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up
