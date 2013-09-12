import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import uuid
import logging
import re
import json

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

class WSHandler(tornado.websocket.WebSocketHandler):
  clients = {}

  # removeKey
  # Completely Removes the key-value pair from the map
  # Params
  # d: map to remove key-value pair from 
  # key: the key to remove
  def removeKey(d, key):
    r = dict(d)
    del r[key]
    return r

  def sendMsgWrapper(session_to,session_from,typeval,message):
    buildMsg = ""
    if typeval == MISC_MSG_TYPE and not session_from == None:
      buildMsg = session_from.id.hex + ": " + message
    else:
      buildMsg = message
    session_to.write_message(createJSONMsg(session_from.id.hex,typeval, buildMsg))

  def open(self):
    self.id = uuid.uuid4()
    sendMsgWrapper(self,None,MISC_MSG_TYPE,"You are now connected to the OpenSesame Server. You are Client "+self.id.hex)
    for key in self.clients:
      sendMsgWrapper(self.clients[key],self,MISC_MSG_TYPE,"I have entered the server")
    self.clients[self.id.hex] = self
    logging.info('Connection '+self.id.hex+' was opened')

  def on_message(self, message):
    global target
    logging.info('Incoming message:' +  message)

    decodedMsg = json.loads(message)
    if decodedMsg["type"] == STARTUP_TYPE:
      target = self
      logging.info("Found the target, Client "+target.id.hex)
    elif decodedMsg["type"] == REQUEST_TYPE:
      sendMsgWrapper(target,self,REQUEST_TYPE,"")
    elif decodedMsg["type"] == ACK_TYPE:
      logging.info('Client ' + self.id.hex + ' has achieved interaction with the Target')
      sendMsgWrapper(self.clients[decodedMsg["id"]], None, MISC_MSG_TYPE, "The target has received your message")
    elif decodedMsg["type"] == MISC_MSG_TYPE:
      for key in self.clients:
        if not target == None and not self.clients[key].id.hex == target.id.hex and not self.id.hex == target.id.hex:
          sendMsgWrapper(self.clients[key], self, MISC_MSG_TYPE, message)
    elif decodedMsg["type"] == DEBUG_TYPE:
      sendMsgWrapper(target,self,DEBUG_TYPE,"Response ping from OpenSesame Server")

  def on_close(self):
    logging.info('Connection '+self.id.hex+' was closed...')
    del self.clients[self.id.hex]
    for key in self.clients:
      sendMsgWrapper(self.clients[key],None,MISC_MSG_TYPE,"A client has left the server")

application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  global target
  target = None
  logging.basicConfig(filename='pysocketLog.log', filemode='w', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
