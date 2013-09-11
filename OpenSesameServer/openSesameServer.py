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

  def removeKey(d, key):
    r = dict(d)
    del r[key]
    return r

  def open(self):
    self.id = uuid.uuid4()
    self.write_message("You are now connected to the OpenSesame Server. You are Client "+self.id.hex)
    for key in self.clients:
      self.clients[key].write_message("A new client has entered the server")
    self.clients[self.id.hex] = self
    logging.info('Connection '+self.id.hex+' was opened')

  def send_message_to_target(session_to,session_from,typeval,message):
    session_to.write_message(createJSONMsg(session_from.id.hex,typeval, session_from.id.hex + ": " + message))

  def on_message(self, message):
    global target
    logging.info('Incoming message:' +  message)

    # for identifying the raspi client
    decoded_msg = json.loads(message)
    # targ_p = re.compile('iamtheraspi')
    # targ_m = targ_p.match(message)
    # if(targ_m):
    if decoded_msg["typeval"] == STARTUP_TYPE:
      target = self
      logging.info("Found the target, Client "+target.id.hex)

    if decoded_msg["typeval"] == MISC_MSG_TYPE:
      for key in self.clients:
        if not target == None and not self.clients[key].id.hex == target.id.hex and not self.id.hex == target.id.hex:
          send_message_to_target(self.clients[key], self, MISC_MSG_TYPE, message)
          # self.clients[key].write_message(self.id.hex + " says: " + message)

    # ping_p = re.compile('raspiping')
    # ping_m = ping_p.match(message)
    # if (not target == None and not targ_m and self.id.hex == target.id.hex and not ping_m):
    if decoded_msg["typeval"] == ACK_TYPE:
      logging.info('Client ' + self.id.hex + ' has achieved interaction with the Target')
      # self.clients[message].write_message("The target has received your message")

    # if a message is sent by the target and it's not the initialization message, it's a
    # message acknowledgement message that contains the id of the client that sent the request
    # if (ping_m and self.id.hex == target.id.hex):
    if decoded_msg["typeval"] == DEBUG_TYPE:
      send_message_to_target(target,self,DEBUG_TYPE,"Response ping from OpenSesame Server")
      # self.clients[target.id.hex].write_message("Response ping from OpenSesame Server")

    # for identifying the open signal
    open_p = re.compile('open')
    open_m = open_p.match(message)
    if(open_m):
      send_message_to_target(target, self, REQUEST_TYPE, "")

  def on_close(self):
    logging.info('Connection '+self.id.hex+' was closed...')
    del self.clients[self.id.hex]
    for key in self.clients:
      self.clients[key].write_message("A client has left the server")

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
