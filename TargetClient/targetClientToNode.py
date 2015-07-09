import time
import logging
import re
import os

from socketIO_client import SocketIO, LoggingNamespace

STARTUP_TYPE = "startup"
REQUEST_TYPE = "request"
ACK_TYPE = "ack"
MISC_MSG_TYPE = "miscMsg"
DEBUG_TYPE = "debug"
DEVICE_ASK_TYPE = "areYouDevice"

socketIO = None

# class OSLoggingNamespace(LoggingNamespace):
#
#   def on_disconnect(self):
#     super(LoggingNamespace,self).on_disconnect()
#     init()


def on_request(*args):
  print ('Open request received. Executing request and sending response ',args)
  logging.info('Open request received. Executing request and sending response ')
  socketIO.emit(ACK_TYPE,args)
  os.system("echo 5=165 > /dev/servoblaster")
  time.sleep(5)
  os.system("echo 5=100 > /dev/servoblaster")

def on_misc(*args):
  print('Misc Message Received: ', args)
  # getting an ErrorType/string formatting error.
  # Figure out args structure later.
  # logging.info("Misc Message Received: '{0}'", args[0])

def on_server_start(*args):
  print('Server Startup Message Received: ', args)
  socketIO.wait(seconds=1)
  socketIO.emit(STARTUP_TYPE, 'frontDoor')

def init():
  global socketIO
  logging.info("A new connection thread is being created.")
  # socketIO = SocketIO('24.90.100.33', 3000, LoggingNamespace)
  socketIO = SocketIO('http://inyongie.com', 3000, LoggingNamespace)
  socketIO.on(REQUEST_TYPE, on_request)
  socketIO.on(MISC_MSG_TYPE, on_misc)
  socketIO.on(DEVICE_ASK_TYPE, on_server_start)
  socketIO.wait()

if __name__ == "__main__":
  os.system("echo 5=100 > /dev/servoblaster")
  logging.basicConfig(filename='doorControlToNodeLatestLog.log',
		      filemode='w',
		      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
		      level=logging.DEBUG)
  init()


