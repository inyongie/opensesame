import websocket
import thread
import time
import logging
import re
import json
import os
# from subprocess import call
# import RPi.GPIO as GPIO

#JSONification of Messages 
def createJSONMsg(source, typeval, message):
  retVal =  { "source" : source , "type" : typeval , "message" : message }
  return json.dumps(retVal)
#json.loads is decoder

def on_message(ws, message):
  # global dCVal
  # global pwmVal
  print message
  logging.info('Message: '+message)
  p = re.compile('.*Request.*')
  m = p.match(message)
  if m:
    reqID = re.search('.*Request:(.*)',message)
    print 'Open request received. Executing request and sending response ' + reqID.group(1)
    logging.info('Open request received. Executing request and sending response ' + reqID.group(1))
    ws.send(reqID.group(1))
    os.system("echo 5=200 > /dev/servoblaster")
    # call(["echo", "5=200 > /dev/servoblaster"])
    # pwmVal.ChangeDutyCycle(10)
    time.sleep(2)
    os.system("echo 5=100 > /dev/servoblaster")
    # call(["echo", "5=100 > /dev/servoblaster"])
    # pwmVal.ChangeDutyCycle(5)
    # dCVal = 1
    # time.sleep(2)
    # dCVal = 0.15
#       GPIO.output(17, True)
#       time.sleep(2)
#       GPIO.output(17, False)

def on_error(ws, error):
  print error
  logging.error(error)
  time.sleep(300)
  logging.info("Creating a new client thread")
  thread.start_new_thread(init, ())

def on_close(ws):
  # global pwmVal
  print "### Connection Closed ###"
  logging.info('Connection Closed')
  # pwmVal.stop()
  # GPIO.cleanup()

def on_open(ws):
  def wakeup(*args):
      var = 1
      while var==1:
        time.sleep(50)
        ws.send("raspiping")
        logging.info("sending ping")
  logging.info("Initializing Connection")
  ws.send("iamtheraspi")
  thread.start_new_thread(wakeup, ())

def init():
  logging.info("A new connection thread is being created.")
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("ws://inyongie.com:8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
  ws.on_open = on_open
  ws.run_forever()

# def dCycle(*args):
#   global dCVal
#   var = 1
#   while var==1:
#     dutyCycle = dCVal
#     GPIO.PWM(17, GPIO.HIGH)
#     time.sleep(dutyCycle)
#     GPIO.output(17, GPIO.LOW)
#     time.sleep(2-dutyCycle)

if __name__ == "__main__":
  # global pwmVal
  # GPIO.setmode(GPIO.BCM)
  # GPIO.setup(18, GPIO.OUT)
  # pwmVal = GPIO.PWM(18, 0.5)
  # pwmVal.start(5)
  # global dCVal
  # dCVal = 0.15
  # call(["echo", "5=100 > /dev/servoblaster"])
  os.system("echo 5=100 > /dev/servoblaster")
  logging.basicConfig(filename='doorControlLatestLog.log', 
		      filemode='w', 
		      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 
		      level=logging.DEBUG)
  thread.start_new_thread(init, ())
  # thread.start_new_thread(dCycle, ())
  # TODO: Find a better way to keep main thread alive.
  var = 1
  while var==1:
    time.sleep(1)

