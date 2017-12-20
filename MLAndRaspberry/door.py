# RPi is used to controll the GPIO pins on raspberry pi
import RPi
import RPi.GPIO as GPIO
# Time is used for sleep
import time
import os

# Flask is a REST Api framework in python
from flask import Flask
from flask_restful import Resource, Api
#from time import sleep
from picamera import PiCamera

# initialize Flask
app = Flask(__name__)
api = Api(app)

# Class to lock the door using get
class Unlock(Resource):
    def get(self):
        # Set the raspberry pi to used the GPIO pins
        GPIO.setmode(GPIO.BOARD)
        # Setting pin 7 as the output pin - yellow wire
        GPIO.setup(7,GPIO.OUT)
        # Use channel 7 send signal with 50Hz
        p = GPIO.PWM(7, 50)
        # Corresponds to start position on the servo motor 0 degrees
        p.start(10.5)
        p.ChangeDutyCycle(10.5)
        # Sleep is needed for the command to work
        time.sleep(1)
        p.stop()
        GPIO.cleanup()
        return {'status': 'unlocked'}

class Lock(Resource):
     def get(self):
        # Set the raspberry pi to used the GPIO pins
        GPIO.setmode(GPIO.BOARD)
        # Setting pin 7 as the output pin - yellow wire
        GPIO.setup(7,GPIO.OUT)       
        # Use channel 7 send signal with 50Hz
        p = GPIO.PWM(7, 50)
        # Corresponds to start position on the servo motor 30 degrees
        p.start(7.5)
        p.ChangeDutyCycle(7.5)
        # Sleep is needed for the command to work
        time.sleep(1) 
        p.stop()
        GPIO.cleanup()
        return {'status': 'locked'}

class clickPhoto(Resource):
    def get(self):
        camera = PiCamera()
        camera.start_preview()
        for i in range(5):
            sleep(2)
            filepath = camera.capture('./image%s.jpg' % i)
            os.system("scp -i sneha.pem ./image%s.jpg ubuntu@50.112.13.135:unknown" %i) 
        camera.stop_preview()
        #s = pathos.core.execute('python deeplearning/recognize.py', host='54.186.191.119')


api.add_resource(Lock, '/lock')
api.add_resource(Unlock, '/unlock')
api.add_resource(clickPhoto, '/clickPhoto')

if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')
