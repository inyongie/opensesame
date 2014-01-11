import websocket
import thread
import time
import logging
import re
import json
import os

STARTUP_TYPE = "startup"
REQUEST_TYPE = "request"
ACK_TYPE = "ack"
MISC_MSG_TYPE = "miscMsg"
DEBUG_TYPE = "debug"

#JSONification of Messages
# createJSONMsg
# idval: UIUD value given to session
# typeval: type of message
# message: any misc. message
def createJSONMsg(idval, typeval, message):
  retVal =  { "id" : idval, "type" : typeval , "message" : message }
  return json.dumps(retVal)
#json.loads is decoder

def sendMsgWrapper(session_to,session_from,typeval,message):
  session_to.send(createJSONMsg(session_from, typeval, message))

def on_message(ws, message):
  logging.info('Message: '+message)
  decodedMsg = json.loads(message)
  if decodedMsg["type"] == REQUEST_TYPE:
    print 'Open request received. Executing request and sending response ' + decodedMsg["id"]
    logging.info('Open request received. Executing request and sending response ' + decodedMsg["id"])
    ws.send(createJSONMsg(decodedMsg["id"], ACK_TYPE, ""))
    os.system("echo 5=165 > /dev/servoblaster")
    time.sleep(5)
    os.system("echo 5=100 > /dev/servoblaster")
  else:
    print decodedMsg["message"]

def on_error(ws, error):
  print error
  logging.error(error)
  time.sleep(300)
  logging.info("Creating a new client thread")
  thread.start_new_thread(init, ())

def on_close(ws):
  print "### Connection Closed ###"
  logging.info('Connection Closed')

def on_open(ws):
  def wakeup(*args):
      var = 1
      while var==1:
        time.sleep(50)
	ws.send(createJSONMsg(None, DEBUG_TYPE, "raspiping"))
        logging.info("sending ping")
  logging.info("Initializing Connection")
  ws.send(createJSONMsg(None, STARTUP_TYPE, "iamtheraspi"))
  thread.start_new_thread(wakeup, ())

def init():
  logging.info("A new connection thread is being created.")
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("ws://inyongie.com:443/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
  ws.on_open = on_open
  ws.run_forever()

if __name__ == "__main__":
  os.system("echo 5=100 > /dev/servoblaster")
  logging.basicConfig(filename='doorControlLatestLog.log', 
		      filemode='w', 
		      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 
		      level=logging.DEBUG)
  thread.start_new_thread(init, ())

  # TODO: Find a better way to keep main thread alive.
  var = 1
  while var==1:
    time.sleep(1)

