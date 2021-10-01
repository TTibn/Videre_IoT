import RPi.GPIO as GPIO
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
MyRequest = None

class RequestHandler_httpd (BaseHTTPRequestHandler):
    
    def do_GET(self):
        global MyRequest
        MyRequest = self.requestline
        MyRequest = MyRequest[5 : int(len(MyRequest) - 9)]
        print('You received this request')
        print(MyRequest)
    
        setup()
       
        try: 
           distance = loop() 
        except KeyboardInterrupt: # Press ctrl-c to end the program. 
           GPIO.cleanup() # release GPIO resource
           messagetosend = bytes(str(distance), "utf")
           self.send_response(200)
           self.send_header('Content-Type', 'text/plain')
           self.send_header('Content-Lenght', len(messagetosend))
           self.end_headers()
           self.wfile.write(messagetosend)
       
        return
   
trigPin = 16
echoPin = 18
MAX_DISTANCE = 220 # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60 # calculate timeout according to the maximum measuring distance

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime 

def getSonar(): # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH) # make trigPin output 10us HIGH level
    time.sleep(0.00001) # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0 # calculate distance with sound speed 340m/s
    return distance


def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT) # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN) # set echoPin to INPUT mode
    
def loop():
    while(True):
        distance = getSonar() # get distance
        print ("The distance is : %.2f cm"%(distance))
        time.sleep(1)
        
        return distance
    
if __name__ == '__main__': # Program entrance
    server_address_httpd = ('192.168.2.3', 8880)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    print('Starting server:')
    httpd.serve_forever()
